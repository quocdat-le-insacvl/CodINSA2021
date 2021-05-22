class Case:

    def __init__(self, tiles_type, build_type, life_point):
        self.tiles_type = tiles_type
        self.build_type = build_type
        self.life_point = life_point

    def __str__(self):
        return "{0};{1};{2}".format(self.tiles_type, self.build_type, self.life_point)

    def __repr__(self):
        return "{0};{1};{2}".format(self.tiles_type, self.build_type, self.life_point)