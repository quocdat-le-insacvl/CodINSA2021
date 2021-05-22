class Case:

    def __init__(self, info):
        s = info.split(";")
        self.tiles_type = s[0]
        self.build_type = s[1] if len(s) != 1 else ""
        self.life_point = s[2] if len(s) != 1 else ""


    def __str__(self):
        return "{0};{1};{2}".format(self.tiles_type, self.build_type, self.life_point)

    def __repr__(self):
        return "{0};{1};{2}".format(self.tiles_type, self.build_type, self.life_point)