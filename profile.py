#
# Contains recipe and system profile data
#

class SystemProfile():
    def __init__(self):
        self.mash_width = 8
        self.mash_length = 36
        self.mash_height = 16
        self.mash_sh = 0.30
        self.mash_max = 0
        self.mash_volume = 0

        self.kettle_base = 8
        self.kettle_height = 24
        self.kettle_sh = 0.12
        self.kettle_max = 0

        self.res_base = 8
        self.res_height = 24
        self.res_sh = 0.12
        self.res_max = 0

    def calibrate_system(self, recipe):
        self.mash_max = \
            self.mash_width * self.mash_length \
            * self.mash_height * 0.0104
        self.kettle_max = \
            self.kettle_base * self.kettle_height \
            * 0.00497
        self.res_max = \
            self.res_base * self.res_height \
            * 0.00497


        self.mash_volume = float(recipe.grain_weight)/2


class RecipeProfile():
    def __init__(self):
        self.strike_temp  = 60#165
        self.lauter_temp  = 60#175
        self.boil_temp    = 60#212
        self.grain_weight = 12
        self.grist_ratio  = 1.2
        self.lauter_time  = 0#20
        self.boil_time    = 0#60
        self.mash_temp    = 60#154
        self.mash_time    = 0#60

        # Hop additions from 1 - 4
        self.hops1        = 2#60
        self.hops2        = 2#30
        self.hops3        = 1#15
        self.hops4        = 0#5
