import string
import subprocess as sp
from controller.controller import Controller

#####################################################################################
# ██████╗ ███████╗██████╗ ██████╗ ███████╗ ██████╗ █████╗ ████████╗███████╗██████╗  #
# ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗ #
# ██║  ██║█████╗  ██████╔╝██████╔╝█████╗  ██║     ███████║   ██║   █████╗  ██║  ██║ #
# ██║  ██║██╔══╝  ██╔═══╝ ██╔══██╗██╔══╝  ██║     ██╔══██║   ██║   ██╔══╝  ██║  ██║ #
# ██████╔╝███████╗██║     ██║  ██║███████╗╚██████╗██║  ██║   ██║   ███████╗██████╔╝ #
#####################################################################################

class ViewCLI:
  def __init__(self,controller):
    self.controller = controller

  def start(self):
    all_commands =[
      'exit',
      'load_world_from_file'
    ]
    cmd_num = -1
    while cmd_num != 0:
      tmp = sp.call('clear')
      self.print_menu(all_commands)
      print('Enter number: ')
      in_text = input()
      try:
        cmd_num = int(in_text)
        command_name = all_commands[cmd_num]
        command = getattr(self, command_name)
        command()
        input()
      except ValueError as e:
        print('Not a Number! try again')
      except IndexError as e:
        print('Not a valid command try num between 0-%d' % (len(all_commands) - 1) )
  def print_menu(self,all_commands):
    print("---------------------------------------------")
    print("Menu: ")
    for i,cmd in enumerate(all_commands):
      print('{0}. {1}'.format(i,cmd.replace('_',' ').capitalize()))
    print("--------------------------------------------- ")

  def exit(self):
    print('Goodbye!')

  def load_world_from_file(self):
    print("Enter path: ")
    path = input()
    success,error_msg = self.controller.load_world_from_file(path)
    if success:
      print("success!")
    else:
      print(error_msg)