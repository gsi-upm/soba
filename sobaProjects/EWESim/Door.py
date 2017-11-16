class Door():

    def __init__(self, x, y, associated_control_access = False, put_always_open = False):
        self.always_open = put_always_open
        self.state = False
        if (self.always_open == True):
            self.state = True
        self.control_access = associated_control_access
        self.x = x
        self.y = y
        
    def open(self, agent = 0):
        if self.control_access == False:
            self.state = True
        else:
            if agent == True:
                self.state = True

    def close(self):
        if self.always_open == False:
            self.state = False
        else:
            pass
