class Gesture:
    def __init__(self, type, direction, command, fingers=0, enabled=True):
        self.type = type
        self.direction = direction
        self.command = command
        self.fingers = fingers
        self.enabled = enabled

    def make(self):
        fingers = str(self.fingers) + " "
        if (self.fingers == 0):
            fingers = ""

        enabled = ""
        if not self.enabled:
            enabled = "#D: "
        return (enabled + "gesture " + self.type + " " + self.direction + " " + str(fingers) + self.command)
