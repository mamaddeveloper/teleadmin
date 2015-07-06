from modules.module_last_random import ModuleBaseLastRandom
from tools.vdm import Vdm

class ModuleVdm(ModuleBaseLastRandom):

    def __init__(self, bot):
        ModuleBaseLastRandom.__init__(self, bot, "ModuleVdm", "vdm", Vdm())
