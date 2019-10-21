import json
import os
import model.utils.parser as parser
import model.utils.dispatcher as dispatcher
import pprint
import csv
import numpy
import re
from model.world_generator import World_generator
from model.utils.constants import CONSTANTS
import random
import shutil
from model.utils.world_utils import calc_entropy
from model.utils.world_utils import standard_deviation


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.dataset = None
        self.current_world = None
        self.current_world_path = None
        self.current_scenerio = None

    def load_world_from_file(self, path):
        try:
            world_json = open(path).read()
            world_data = json.loads(world_json)
            self.current_world = parser.json_to_world(world_data)
            self.current_world_path = path
        except FileNotFoundError:
            return False, "File not found"
        except Exception as e:
            return False, e
        return True, ""

    def generate_world(self, args):
        return World_generator().generate_world(args)

    def run_algorithm_on_world(self, algo, algo_args, tpd):
        try:
            if self.current_world is None:
                return False, "No world loaded"
            self.current_scenerio = dispatcher.run_algorithm_on_world(
                self.current_world, algo, algo_args, tpd)
        except FileNotFoundError as e:
            return False, e
        except NameError as e:
            return False, e
        return True, ""

    def get_scenerio_for_gui(self):
        if self.current_scenerio is None:
            return False, "No scenerio have been created"
        return True, self.current_scenerio

    def get_scenerio_info(self):
        return self.current_scenerio['statistic']

    def set_const(self, const_name, new_value):
        if const_name in CONSTANTS:
            try:
                converted_value = float(new_value)
            except ValueError:
                try:
                    converted_value = int(new_value)
                except ValueError:
                    converted_value = new_value

            CONSTANTS[const_name] = converted_value
            return True, ""
        else:
            return False, "Constant '{}' not found".format(const_name)

    def work_on_dataset(self, name):
        dataset_path = os.path.join('./_data/datasets', name)
        if not os.path.exists(dataset_path):
            if(input("dataset does not exist, do you with to create it? Y/N: ").lower() == 'n'):
                return
            os.makedirs(dataset_path)
            os.makedirs(os.path.join(dataset_path, 'generated_worlds'))
            with open(os.path.join(dataset_path, "statistics.csv"), "a", newline=''):
                pass
            with open(os.path.join(dataset_path, "algorithms.txt"), "a"):
                pass
        self.dataset = dataset_path
        print("Dataset loaded")

    def populate_dataset(self, args):
        if not self.dataset:
            print('Dataset not chosen')
            return
        args['path'] = {}
        args['path']['default'] = os.path.join(self.dataset, "generated_worlds")
        number_worlds = int(args['num']['default'])
        origin_name = args['name']['default']
        worlds = []
        path = os.path.join(self.dataset, 'generated_worlds')
        generator = World_generator()
        for i in range(number_worlds):
            world_name = origin_name+'_'+str(i)
            j = 0
            while os.path.isfile(os.path.join(path, world_name+'.world')):
                j += 1
                if j != 1:
                    world_name = world_name[:-2]
                world_name += '_'+str(j)
            worlds.append(world_name)
            args['name']['default'] = world_name
            generator.generate_world(args)
        print('worlds generated succesfully')
        args['name']['default'] = origin_name
        self.stats_csv(args, worlds)
        print("Run complete")

    def stats_csv(self, args, worlds):
        with open(os.path.join(self.dataset, "algorithms.txt"), "r") as alg_script:
            algs = alg_script.readlines()

        dataset = [[0 for _ in range(len(worlds))] for _ in range(len(algs))]
        total_runs = len(worlds)*len(algs)
        count_runs = 0
        runtime_arr = [0]*len(algs)
        entropies = ['Entropy', '', '', '']
        p_sd = ['p_sd', '', '', '']
        st_sd = ['st_sd', '', '', '']
        # read data worlds for statistics
        for j, world in enumerate(worlds):
            if world[-1] == '\n':
                world = world[:-1]
            print("loading world: ", world)
            self.load_world_from_file(os.path.join(self.dataset, 'generated_worlds', world+'.world'))
            p_deviation, st_deviation = standard_deviation(self.current_world)
            p_sd.append(p_deviation)
            st_sd.append(st_deviation)
            entropies.append(calc_entropy(self.current_world))
            for i, alg in enumerate(algs):
                if alg[-1] == '\n':
                    algs[i] = alg[:-1]
                _, args2 = self.parse_input("runalgo "+algs[i])
                count_runs += 1
                print("completed: ", count_runs, '/', total_runs)
                algo = args2['a']['default']
                algo_args = args2['a']
                tpd = int(args['t']['default'])
                print("running algorithm: ", algo)
                self.run_algorithm_on_world(algo, algo_args, tpd)
                stat_obj = self.get_scenerio_info()
                dataset[i][j] = stat_obj['total_price']
                runtime_arr[i] += int(stat_obj['runtime'])
        with open(os.path.join(self.dataset, "statistics.csv"), "a", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            world_names = []
            world_names.append((args['name']['default'] if 'name' in args else 'dataset')+':'+args['t']['default'])
            alg_names = []
            for alg in algs:
                alg_names.append(alg[3:])
            for world in worlds:
                world_names.append(world)
            world_names.insert(1, "Average runtime")
            world_names.insert(1, "Median")
            world_names.insert(1, "Average")
            writer.writerow(world_names)
            writer.writerow(entropies)
            writer.writerow(p_sd)
            writer.writerow(st_sd)
            for i, row in enumerate(dataset):
                size = len(row)
                ordered_row = sorted(row)
                mean = ordered_row[int(size/2)] if size % 2 == 1 else (ordered_row[int(size/2)] + ordered_row[int(size/2)-1])/2
                row.insert(0, int(runtime_arr[i]/len(worlds)))
                row.insert(0, mean)
                row.insert(0, (numpy.average(row[len(row)-size:])))
                row.insert(0, alg_names[i])
                writer.writerow(row)
            writer.writerows(['', ''])

    def parse_input(self, user_input):
        print(user_input)
        user_input = re.sub(" +", " ", user_input)
        strs = user_input.split(" ")
        args_strs = strs[1:]
        command = strs[0]
        args = {}
        i = 0
        # remove falsy values
        for val in args_strs:
            if val == '':
                args_strs.remove(val)
        while i < len(args_strs):
            arg = args_strs[i]
            next_arg = ""
            if i < len(args_strs) - 1:
                next_arg = args_strs[i+1]
            if "-" == arg[0]:
                if ":" in arg:
                    arg, subarg = arg[1:].split(':')
                    if next_arg:
                        if "-" == next_arg[0]:
                            args[arg][subarg] = True
                            i += 1
                        else:
                            args[arg][subarg] = next_arg
                            i += 2
                    else:
                        args[arg][subarg] = True
                        i += 1
                else:
                    arg = arg[1:]
                    args[arg] = {}
                    if next_arg:
                        if "-" == next_arg[0]:
                            args[arg]['default'] = True
                            i += 1
                        else:
                            args[arg]['default'] = next_arg
                            i += 2
                    else:
                        args[arg]['default'] = True
                        i += 1
        return command, args

    def dump_dataset(self):
        if not os.path.exists(self.dataset):
            return False, 'no dataset is loaded'
        path = os.path.join(self.dataset, 'generated_worlds')
        for file_name in os.listdir(path):
            if file_name[-6:] == '.world':
                os.unlink(os.path.join(path, file_name))
        return True, ''

    def delete_dataset(self, name):
        path = os.path.join('./_data/datasets/', name)
        if not os.path.exists(path):
            return False, f"Failed to delete dataset, \'{name}\' does not exist."
        try:
            shutil.rmtree(path)
        except Exception as e:
            return False, e
        if os.path.exists(path):
            return False, f"{name} could not be deleted, make sure no files or folders of the dataset are open"
        if self.dataset == path:
            self.dataset == None
        return True, ''
