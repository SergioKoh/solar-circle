import math


from target_module import *

WIDTH, HEIGHT = 800, 600


class Shell:
    """Class of shells emitted from the gun"""
    def __init__(self, x0, y0, v0, event, window):
        """The shell appears at the tip of the barrel"""
        self.x0, self.y0 = x0, y0
        self.v0 = 5 * v0  # 5 selected coefficient of initial speed versus power
        self.x = self.x0
        self.y = self.y0
        self.r = 10
        self.color = choice(('red', 'blue', 'maroon', 'cyan', 'green', 'lime', 'purple'))
        self.event = event
        self.t = self.dt = 0.1
        self.cycle = 1
        self.initial_shell(window)
        self.flag_x = 0  # flag_x, flag_y - flags reflection from wall and ceiling
        self.flag_y = 0
        self.flag_x1 = 0  # flag_x1 - flag indicates when the projectile hits the wall during takeoff or fall.
        self.flag_hit = False



    def initial_shell(self, window):
        """Calculation of constants for the projectile flight formula."""
        self.not_zero = self.event.x - self.x0
        if self.not_zero == 0:  # So exclude the ZeroDivisionError, when calculating the angle.
            self.not_zero = 1

        self.angle = math.atan((self.event.y - self.y0) / self.not_zero)
        self.vx = self.v0 * math.cos(self.angle)
        self.vy = -self.v0 * math.sin(self.angle)
        self.t_ascent = self.vy / 9.8

        self.avatar = window.canvas.create_oval(self.x, self.y - 2 * self.r,
                                                self.x + 2 * self.r, self.y, fill=self.color, tag="bum")

    def move_shell(self, window, targets, shells):
        """Move the projectile after a unit of time.
        The velocities vx and vy take into account the force of gravity,
        and walls around the edges of the window.
        """
        self.id_after = window.after(30, self.move_shell, window, targets, shells)
        self.xx = self.x0 + self.vx * self.t
        self.y = self.y0 - (self.vy * self.t - 9.8 * self.t ** 2 / 2)
        if not self.flag_x and not self.flag_y:
            self.x = self.xx
        if self.flag_y and not self.flag_x:
            self.x = self.xx - self.x_1
        if self.flag_x and not self.flag_y:
            if not self.flag_x1:
                self.x = self.xx - 2 * (self.xx - WIDTH) - (self.x - WIDTH - self.r) / 2
            else:
                self.x = (self.xx - self.x_2 - 2 * (self.xx - self.x_2 - WIDTH) -
                          (self.x - WIDTH - self.r) / 2)

        if self.flag_x and self.flag_y:
            self.x = (self.xx - self.x_1 - 2 * (self.xx - self.x_1 - WIDTH) -
                      (self.x - WIDTH - self.r) / 2)

        if self.y <= 0 + self.r:
            self.flag_y = 1
            self.t = self.t + 2 * (self.t_ascent - self.t)
            self.x_1 = self.x0 + self.vx * self.t - self.x
        if self.x >= WIDTH - self.r:
            self.flag_x = 1
            if self.t_ascent - self.t > 0:
                self.t = self.t + 2 * (self.t_ascent - self.t)
                self.x_2 = self.x0 + self.vx * self.t - self.x
                self.flag_x1 = 1
        if self.x <= self.r:
            self.x = self.r

        self.t += self.dt

        window.canvas.coords(self.avatar, self.x, self.y - 2 * self.r,
                             self.x + 2 * self.r, self.y)
        if self.y >= HEIGHT:
            window.after_cancel(self.id_after)

        self.bum = self.hittest(targets, shells, window)

    def hittest(self, targets, shells, window):
        """The function checks if the given object collides with the target.
        """
        for shell in shells:
            self.flag_hit = self.flag_hit or shell.flag_hit
        for target in targets:
            if (target.r + self.r) ** 2 >= ((target.x + target.r - (self.x + self.r)) ** 2 +
                                            (target.y + target.r - (self.y + self.r)) ** 2):
                if not self.flag_hit:
                    self.flag_hit = True
                    window.drawing_hit(target)
                    targets.remove(target)
                else:
                    self.flag_hit = False
                    window.drawing_hit(target)
                    self.namber = len(shells)
                    shells.clear()
                    targets.remove(target)
                    window.drawing_text(self.namber)
                    window.after(3000, target.new_targets, targets, window)
                window.after_cancel(self.id_after)
