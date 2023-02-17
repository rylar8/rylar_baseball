
class Player():
    def __init__(self, trackman_id):
        self.trackman_id = trackman_id
        self.name = ''
        self.player_id = ''
        self.batter_side = ''
        self.throws = ''
        self.team = ''
    pass

class Pitcher(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
    pass

class Hitter(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
    pass

class Catcher(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
    pass