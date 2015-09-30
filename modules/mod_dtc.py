from modules.module_last_random import ModuleBaseLastRandom
from tools.dtc import Dtc

class ModuleDtc(ModuleBaseLastRandom):

    def __init__(self, bot):
        ModuleBaseLastRandom.__init__(self, bot, "ModuleDtc", "dtc", Dtc())

    def get_commands(self):
        return [
            ("dtc", "DTC. Keywords : <last/random>"),
        ]
