import string
import subprocess as sp
import re
import datetime
import os
import csv
import numpy
from pathlib import Path
from controller.controller import Controller
from view.gui.screens.scenerioDisplayer import ScenerioDisplayer as ScenerioDisplayer

from model.utils.constants import CONSTANTS


class ViewInterpreter:

    def __init__(self, controller):
        self.controller = controller

    def prestart(self, script_file=None):
        self.all_commands = {
            'exit': self.exit,
            'cmdlist': self.print_cmd_list,
            'loadworld': self.load_world,
            'runalgo': self.run_algorithm,
            'showscenerio': self.show_scenerio,
            'infoscenerio': self.print_scenerio_info,
            'changeconst': self.change_constant,
            'generateworld': self.generate_world,
            'statsscript': self.stats_script,
            'statscsv': self.stats_csv,
            'workondataset': self.work_on_dataset,
            'populatedataset': self.populate_dataset
        }
        if script_file:
            self.load_scripts_from_file(script_file)

    def start(self):
        self.print_opening_message()

        try_to_exit = False
        interrupted = False

        while not interrupted:
            try:
                user_input = input(">>> ")
            # Catch if user type Ctrl+C twice in arrow (Like in Node.JS console). Not more than a gimmick :)
            except KeyboardInterrupt:
                if try_to_exit:
                    print("")
                    interrupted = True
                else:
                    print("\n(To exit, press ^C again)")
                    try_to_exit = True
                continue

            try_to_exit = False
            self.handle_input(user_input)

    def load_scripts_from_file(self, file_path):
        try:
            with open(file_path) as f:
                lines = f.readlines()
            for line in lines:
                # clear unnecessery characters at the end of the line (e.g: New-Line, Tabs, spaces, etc..)
                fixed_line = line.rstrip()
                print(">>>", fixed_line)
                succeed_to_execute = self.handle_input(fixed_line)
                if not succeed_to_execute:  # stop script file from running if line was broken
                    break
        except FileNotFoundError as e:
            print(
                "Script file not found in path {}, continues as usual".format(file_path))

    def handle_input(self, user_input):
        command_name, args = self.parse_input(user_input)
        if command_name in self.all_commands:
            self.all_commands[command_name](args)
            return True
        else:
            print("the command '{}' doesn't exist.".format(command_name))
            return False

    def parse_input(self, user_input):
        user_input = re.sub(" +", " ", user_input)
        strs = user_input.split(" ")
        args_strs = strs[1:]
        command = strs[0]
        args = {}
        i = 0
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

    def print_opening_message(self):
        print("")
        print("Welcome to the Simulator Interpreter!")
        print("To start just enter the command you want to execute.")
        print(
            "If you want to use specific command just type: [COMMAND] -? (TBC)")
        print("If you want to know what commands do you have just type: cmdlist")
        print("")

    def exit(self, args):
        exit()

    def print_cmd_list(self, args):
        for cmdname in self.all_commands:
            print(cmdname)

    def load_world(self, args):
        path = args['f']['default']
        success, error_msg = self.controller.load_world_from_file(path)
        if success:
            print("World loaded successfully!")
        else:
            print(error_msg)

    def run_algorithm(self, args):
        algo = args['a']['default']
        algo_args = args['a']
        tpd = int(args['t']['default'])
        success, error_msg = self.controller.run_algorithm_on_world(
            algo, algo_args, tpd)
        if success:
            print(
                "Algorithm run complete.\nrun 'infoscenerio' for details or 'showscenerio' for GUI view")
        else:
            print(error_msg)

    def generate_world(self, args):
        success, error_msg = self.controller.generate_world(args)
        if success:
            print(
                args['name']['default'] + " generated successfully")
        else:
            print(error_msg)

    def show_scenerio(self, args):
        response = self.controller.get_scenerio_for_gui()
        success = response[0]
        if success:
            scenerio = response[1]
            ScenerioDisplayer(scenerio)
            print("OUTPUT: ", scenerio['output'])
        else:
            error_msg = response[1]
            print(error_msg)

    def print_scenerio_info(self, args):
        details = self.controller.get_scenerio_info()
        text_lines = [" {}: {} ".format(k, v) for k, v in details.items()]
        size = max([len(tl) for tl in text_lines])
        print("#" + size*"#" + "#")
        for tl in text_lines:
            print("#" + tl.ljust(size) + "#")
        print("#" + size*"#" + "#")

    def change_constant(self, args):
        const_name = args['n']['default']
        new_value = args['v']['default']
        success, error_msg = self.controller.set_const(const_name, new_value)
        if success:
            print('Set {} to "{}"'.format(const_name, new_value))
        else:
            print(error_msg)

        print(CONSTANTS)

    def stats_script(self, args):
        with open(".\_data\scripts\scriptagls.txt", "r") as alg_script:
            algs = alg_script.readlines()
        with open(".\_data\scripts\scriptworlds.txt", "r") as world_script:
            worlds = world_script.readlines()

        timedir = self.create_time_dir()

        alg_times = [0]*len(algs)
        for world in worlds:
            if world[-1] == '\n':
                world = world[:-1]
            self.handle_input("loadworld "+world)
            for i, alg in enumerate(algs):
                if alg[-1] == '\n':
                    alg = alg[:-1]
                self.handle_input("runalgo "+alg)
                alg_times[i] += self.fprint_scenerio_info(timedir, world, alg)
        with open(os.path.join(timedir, "overall stats.txt"), "a") as f:
            for i, alg in enumerate(algs):
                if alg[-1] == '\n':
                    alg = alg[:-1]
                f.write(alg+"\n\toverall score: "+str(alg_times[i])+"\n")

    def create_time_dir(self):

        dirpath = os.path.join(".\_data\statistics", str(datetime.datetime.now().date()))
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        time = datetime.datetime.now().time()
        dirpath = os.path.join(dirpath, str("-".join((str(time.hour), str(time.minute), str(time.second)))))
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath

    def fprint_scenerio_info(self, path, world, alg):
        m = re.search("\/[^\/]+\.world$", world)
        if m:
            worlddir = m.group(0)[1:-6]
        worldpath = os.path.join(path, worlddir)
        if not os.path.exists(worldpath):
            os.makedirs(worldpath)
        m = re.search("^-a [^ ]+", alg)
        if m:
            algfile = m.group(0)[3:]+".txt"
        path = os.path.join(worldpath, algfile)

        with open(path, "a") as f:
            details = self.controller.get_scenerio_info()
            text_lines = [" {}: {} ".format(k, v) for k, v in details.items()]
            size = max([len(tl) for tl in text_lines])
            f.write(alg[len(algfile)-1:]+'\n')
            f.write("#" + size*"#" + "#"+'\n')
            for tl in text_lines:
                f.write("#" + tl.ljust(size) + "#"+'\n')
            f.write("#" + size*"#" + "#"+'\n\n')
        return details['total_price']

    def stats_csv(self, args):
        with open(".\_data\scripts\scriptagls.txt", "r") as alg_script:
            algs = alg_script.readlines()
        with open(".\_data\scripts\scriptworlds.txt", "r") as world_script:
            worlds = world_script.readlines()

        timedir = self.create_time_dir()
        dataset = [[0 for _ in range(len(worlds))] for _ in range(len(algs))]

        for j, world in enumerate(worlds):
            if world[-1] == '\n':
                world = world[:-1]
            self.handle_input("loadworld "+world)
            for i, alg in enumerate(algs):
                if alg[-1] == '\n':
                    algs[i] = alg[:-1]
                self.handle_input("runalgo "+algs[i])
                dataset[i][j] = self.controller.get_scenerio_info()['total_price']
        with open(os.path.join(timedir, "dataset.csv"), "a", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            world_names = []
            world_names.append(args['name']['default'] if 'name' in args else 'dataset')
            alg_names = []
            for alg in algs:
                alg_names.append(alg[3:])
            for world in worlds:
                m = re.search("\/[^\/]+\.world$", world)
                if m:
                    world_names.append(m.group(0)[1:-6])
            world_names.insert(1, "Sum")
            if 'avg' in args:
                world_names.insert(1, "Average")
            writer.writerow(world_names)
            for i, row in enumerate(dataset):
                size = len(row)
                row.insert(0, sum(row[len(row)-size:]))
                if 'avg' in args:
                    row.insert(0, (numpy.average(row[len(row)-size:])))
                row.insert(0, alg_names[i])
                writer.writerow(row)

    def work_on_dataset(self, args):
        name = args['d']['default']
        self.controller.work_on_dataset(name)

    def populate_dataset(self, args):
        self.controller.populate_dataset(args)
