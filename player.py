
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

class Hitter(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)

class Fielder(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)

class Catcher(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)

class Baserunner():
    def __init__(self, trackman_id):
        super().__init__(trackman_id)