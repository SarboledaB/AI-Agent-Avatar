from mesa import Agent,Model

class Agent_Avatar(Agent):
    def __init__(self):
        print('Hello human, I am your avatar, you can configure me to be as similar to you as possible, my creators are Anthony Garcia, Sebastian Arboleda and Katherin Valencia.')

class Model_Avatar(Model):
    def __init__(self):
        agent = Agent_Avatar()

Avatar = Model_Avatar()