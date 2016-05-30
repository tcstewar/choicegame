
class Action(object):
    def valid(self):
        return True

class FreeformAction(object):
    pass

class Game(object):
    def __init__(self):
        self.choices = []
        self.pending_choices = []
        self.loop = None

    def next_choice(self, text):
        if len(self.pending_choices) > 0:
            return self.pending_choices.pop(0)
        else:
            return raw_input(text)

    def reset(self, pending_choices=[]):
        self.pending_choices = pending_choices
        self.choices = []


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
                        c = self.next_choice(act.text)
                        act.perform(c)
                        self.choices.append(c)
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
                    try:
                        c = self.next_choice('Choose: ')
                    except EOFError:
                        # ctrl-Z
                        c = 'u'
                    if c == 'u':
                        self.reset(self.choices[:-1])
                        gen = self.start()
                        chosen = None
                        #import ipdb
                        #ipdb.set_trace()
                        break


                    try:
                        c = int(c) - 1
                    except ValueError:
                        continue
                    if 0 <= c < len(valid_actions):
                        chosen = valid_actions[c]
                        self.choices.append('%d' % (c+1))
                        break
                if chosen is not None:
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

