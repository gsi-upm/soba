class Agent():

    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.model.schedule.add(self)
        self.color = 'orange'
        self.shape = 'circle'

    def step(self):
        pass