class Item:
    def __init__(self, *args, **kwargs):
        self.controllers = []

    def __hash__(self):
        raise NotImplementedError

    def add_controller(self, controller):
        self.controllers.append(controller)