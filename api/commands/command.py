import importlib
from random import random
from numpy.random import choice

class CommandInvoker:
    """
    The command interface that declares a method (execute) for a particular
    action.
    """
    
    def __init__(self):
        pass

    def get_command(self, name:str):
        class_name = f"Cmd___{name}"
        module = importlib.import_module("api.commands.command")
        class_ = getattr(module, class_name)
        instance = class_(name)
        return instance

    def run(self, cmd_name:str, args:dict, player:dict):
        instance = self.get_command(cmd_name)
        if not instance.requires({}, player, args):
            print(f"ERROR MESSAGE: {instance.error_msg}")
            return
        return instance.execute(player, args)


class Command:
    """
    The command interface that declares a method (execute) for a particular
    action.
    """
    
    def __init__(self, name):
        self.name = name
        self.error_msg = ""
        self._args = {
            "duration": 0,
            "success_prob": 1.0,
            "async": True,  
            "requires": self.requires,
        }
    
    def requires(self, game, player, args):
        self.error_msg = "Can't execute abstract command"
        return False

    def get_arg(self, key):
        return self._args[key]

    def set_arg(self, key, val):
        if key not in self._args:
            raise IndexError
        self._args[key] = val




class Cmd___explore_near_space(Command):
    def __init__(self, name):
        super().__init__(name)
        self.set_arg("duration", 15)
        self.set_arg("success_prob", 1.0)
        self.set_arg("async", False)

    def requires(self, game, player, args):
        self.error_msg = ""
        return True

    def execute(self, player:dict, args:dict):
        if self.get_arg("success_prob") >= random():
            message = "SUCCESS: Near Space Exploration Complete"
            candidates = {
                "asteroid": 0.30,
                "planet": 0.20,
                "star": 0.40,
                "space debris": 0.05,
                "de-energized satellite": 0.04,
                "worm-hole": 0.01 
            }
            
            found = choice(len(candidates.keys()), 1, p=list(candidates.values()))[0]
            return True, message, list(candidates.keys())[found]
        
        message = "FAIL: Near Space Exploration Complete without results"
        return True, message, None    

class Cmd___explore_deep_space(Command):
    def __init__(self, name):
        super().__init__(name)
        self.set_arg("duration", 30)
        self.set_arg("success_prob", 0.3)

class Cmd___colonize_planet(Command):
    def __init__(self, name):
        super().__init__(name)
        self.set_arg("duration", 60)
        self.set_arg("success_prob", 0.8)




