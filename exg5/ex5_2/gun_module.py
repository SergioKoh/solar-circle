


from shell_module import *


WIDTH, HEIGHT = 800, 600



class Gun:
    """Gun class"""

    def __init__(self):
        """Gun initialization.
        x, y - initial position of the gun on the canvas,
        r - tower radius, power - shot force.
        """
        self.x = 0
        self.y = HEIGHT // 1.3
        self.r = 20
        self.color = 'black'
        self.length_barrel = 20
        self.flag_aiming = 0
        self.flag_fire = 0
        self.power = 1
        self.initial_gun()

    def initial_gun(self):
        """Sets the initial state of the gun"""
        self.color = 'black'
        self.length_barrel = 20
        self.flag_fire = 0
        self.power = 1
        self.x0_b = self.r
        self.y0_b = self.y
        self.x1_b = self.r + self.length_barrel
        self.y1_b = self.y

    def barrel_movement(self, event, guns, window):
        """Calculation of coordinates when changing the direction of the gun barrel."""
        if event.x <= 0:  # So exclude the ZeroDivisionError, when calculating the angle.
            event.x = 1
        self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        self.x0_b = self.r * math.cos(self.angle)
        self.y0_b = self.y + self.r * math.sin(self.angle)
        self.x1_b = (self.r + self.length_barrel +
                     self.flag_fire * self.power) * math.cos(self.angle)
        self.y1_b = self.y + (self.r + self.length_barrel +
                              self.flag_fire * self.power) * math.sin(self.angle)
        window.drawing_guns(guns)

    def power_gain(self, event, guns, window, flag_after=0):
        """Increases the power of the shot depending on the duration of the mouse button press.
        flag_after - flag to define: the event from a loop or from real time."""
        if self.power == 1:
            flag_after = 1
            self.event_button1 = event
        if not flag_after:
            self.barrel_movement(event, guns, window)
            self.event_button1.x = event.x  # changing the x,y coordinates of the event from the loop
            self.event_button1.y = event.y  # in accordance with the real position
        elif self.flag_fire == 1 and self.power < 30:
            self.power += 1
            self.barrel_movement(event, guns, window)
            window.after(30, self.power_gain, event, guns, window, 1)

    def aiming(self, event, guns, window):
        """Direction of the gun on the mouse cursor."""
        self.flag_aiming = 1
        self.barrel_movement(event, guns, window)

    def preparing(self, event, guns, window):
        """Preparing the gun for firing."""
        self.flag_fire = 1
        self.power_gain(event, guns, window)

    def fire(self, event, guns, shells, targets, window):
        """Cannon shot."""
        shell = Shell(self.x1_b, self.y1_b, self.power, event, window)
        shells.append(shell)
        shell.move_shell(window, targets, shells)
        self.initial_gun()
        self.barrel_movement(event, guns, window)