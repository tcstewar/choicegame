
class Action(object):
    def valid(self):
        return True

class FreeformAction(object):
    pass

class Game(object):
    def __init__(self):
        self.choices = []
        self.loop = None

    def run(self):

        gen = self.start()

        while True:
            try:
                act = next(gen)
            except StopIteration:
                if self.loop is not None:
                    gen = self.loop()
                    act = next(gen)

            print self.text()

            if isinstance(act, FreeformAction):
                while True:
                    try:
                        c = raw_input(act.text)
                        act.perform(c)
                        break
                    except:
                        pass
            else:
                valid_actions = []
                for a in act:
                    if a.valid():
                        valid_actions.append(a)

                while True:
                    for i, a in enumerate(valid_actions):
                        print('%2d: %s' % (i+1, a.text()))
                    c = raw_input('Choose: ')
                    try:
                        c = int(c) - 1
                    except ValueError:
                        continue
                    if 0 <= c < len(valid_actions):
                        chosen = valid_actions[c]
                        break
                chosen.perform()




    def freeform(self, text):
        if len(self.choices) > self.choice_index:
            c = self.choices[self.choice_index]
            self.choice_index += 1
            return c
        else:
            c = raw_input(text)
            self.choices.append(c)
            return c

