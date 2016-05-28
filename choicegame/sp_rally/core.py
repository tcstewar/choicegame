import choicegame

class MoveForward(choicegame.Action):
    def __init__(self, player, steps):
        self.player=player
        self.steps=steps
    def perform(self):
        self.player.position += self.steps
    def text(self):
        return 'Move Player %d forward %d spaces' % (self.player.index,
                                                     self.steps)

class Player(object):
    def __init__(self, game, index):
        self.index = index
        self.game = game
        self.position = 0


class ChooseNumberPlayers(choicegame.FreeformAction):
    text = 'Number of players (1-6):'
    def __init__(self, game):
        self.game = game
    def perform(self, choice):
        n_players = int(choice)
        assert 1 <= n_players <=6
        self.game.n_players = n_players

class SteampunkRally(choicegame.Game):
    def __init__(self):
        super(SteampunkRally, self).__init__()
        self.started = False

    def start(self):
        yield ChooseNumberPlayers(self)

        self.players = [Player(self, i+1) for i in range(self.n_players)]

        self.started = True

        self.loop = self.move

    def move(self):
        actions = []
        for p in self.players:
            actions.append(MoveForward(p, 1))
            actions.append(MoveForward(p, 2))
        yield actions

    def text(self):
        if not self.started:
            return 'Welcome to Steampunk Rally'

        tracks = []
        for p in self.players:
            track = ['.' for i in range(80)]
            track[60] = '|'
            track[p.position] = '%d' % p.index
            tracks.append(''.join(track))
        return '\n'.join(tracks)


if __name__ == '__main__':
    g = SteampunkRally()
    g.run()
