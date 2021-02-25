from random import randint
from random import choice
import tkinter as tk
import math

WIDTH, HEIGHT = 800, 600


class Window(tk.Tk):
    """Displaying objects on the canvas"""

    def __init__(self):
        super().__init__()
        self.title("Cannon Game OOP")
        x, y = self.center_screen(self)
        self.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def center_screen(self, master):
        """Centering the window."""
        w = (master.winfo_screenwidth() - WIDTH) // 2
        h = (master.winfo_screenheight() - HEIGHT) // 2
        return w, h

    def drawing_targets(self):
        """Drawing goals."""
        self.canvas.delete("text")
        self.canvas.delete("bum")
        for target in targets:
            x, y = target.x, target.y
            r, color = target.r, target.color
            target.id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)

    def drawing_guns(self):
        """Drawing of guns."""
        for gun in guns:
            if gun.flag_aiming == 0:
                self.canvas.create_arc(gun.x - gun.r, gun.y - gun.r, gun.x + gun.r, gun.y + gun.r,
                                       start=270, extent=180, style=tk.CHORD, fill=gun.color, tag="gun")

                self.barrel = self.canvas.create_line(gun.x0_b, gun.y0_b,
                                                      gun.x1_b, gun.y1_b, fill=gun.color, width=7, tag="gun")

            if gun.flag_aiming == 1:
                self.canvas.itemconfig("gun", fill='black')
                self.canvas.coords(self.barrel, gun.x0_b, gun.y0_b, gun.x1_b, gun.y1_b)

            if gun.flag_fire == 1:
                self.canvas.itemconfig("gun", fill='orange')
                self.canvas.coords(self.barrel, gun.x0_b, gun.y0_b, gun.x1_b, gun.y1_b)

    def drawing_hit(self, target, namber):
        """The function draws an explosion and writes text"""
        self.detonation = [(target.x - 3, target.y)]
        for i in range(7):
            self.x = target.x + 2 * i * target.r / 8 - target.r
            self.y = target.y - 2 * target.r
            self.xx = target.x - 3 + i
            self.yy = target.y
            self.detonation.extend(((self.x, self.y), (self.xx, self.yy)))

        self.canvas.create_polygon(self.detonation, outline=target.color, tag='text')

        self.canvas.create_arc(target.x - 1.5 * target.r, target.y - 2.5 * target.r,
                               target.x, target.y + target.r / 3,
                               start=160, extent=-80, style=tk.ARC, outline=target.color,
                               width=2, tag='text')
        self.canvas.create_arc(target.x - target.r, target.y - 3 * target.r,
                               target.x + target.r, target.y,
                               start=140, extent=-100, style=tk.ARC, outline=target.color,
                               width=2, tag='text')
        self.canvas.create_arc(target.x, target.y - 2.5 * target.r,
                               target.x + 1.3 * target.r, target.y + target.r / 3,
                               start=100, extent=-80, style=tk.ARC, outline=target.color,
                               width=2, tag='text')

        self.canvas.delete("bum")
        self.canvas.delete(target.id)
        if namber > 1:
            self.canvas.create_text(WIDTH / 2, HEIGHT / 3, text=f"You destroyed the target in {namber} shots",
                                    font=("Lucida Sans Unicode", 12, "bold"), tag='text')
        else:
            self.canvas.create_text(WIDTH / 2, HEIGHT / 3, text=f"You destroyed the target in {namber} shot",
                                    font=("Lucida Sans Unicode", 12, "bold"), tag='text')


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

    def barrel_movement(self, event):
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
        window.drawing_guns()

    def power_gain(self, event, flag_after=0):
        """Increases the power of the shot depending on the duration of the mouse button press.
        flag_after - flag to define: the event from a loop or from real time."""
        if self.power == 1:
            flag_after = 1
            self.event_button1 = event
        if not flag_after:
            self.barrel_movement(event)
            self.event_button1.x = event.x  # changing the x,y coordinates of the event from the loop
            self.event_button1.y = event.y  # in accordance with the real position
        elif self.flag_fire == 1 and self.power < 30:
            self.power += 1
            self.barrel_movement(event)
            window.after(30, self.power_gain, event, 1)

    def aiming(self, event):
        """Direction of the gun on the mouse cursor."""
        self.flag_aiming = 1
        self.barrel_movement(event)

    def preparing(self, event):
        """Preparing the gun for firing."""
        self.flag_fire = 1
        self.power_gain(event)

    def fire(self, event):
        """Cannon shot."""
        shell = Shell(self.x1_b, self.y1_b, self.power, event)
        shells.append(shell)
        shell.move_shell()
        self.initial_gun()
        self.barrel_movement(event)


class Shell:
    """Class of shells emitted from the gun"""

    def __init__(self, x0, y0, v0, event):
        """The shell appears at the tip of the barrel"""
        self.x0, self.y0 = x0, y0
        self.v0 = 5 * v0  # 5 selected coefficient of initial speed versus power
        self.x = self.x0
        self.y = self.y0
        self.r = 10
        self.color = choice(('blue', 'green', 'red', 'brown'))
        self.event = event
        self.t = self.dt = 0.1
        self.cycle = 1
        self.initial_shell()
        self.flag_x = 0  # flag_x, flag_y - flags reflection from wall and ceiling
        self.flag_y = 0
        self.flag_x1 = 0  # flag_x1 - flag indicates when the projectile
                            # hits the wall during takeoff or fall.

    def initial_shell(self):
        """Calculation of constants for the projectile flight formula."""
        self.not_zero = self.event.x - self.x0
        if self.not_zero == 0:  # So exclude the ZeroDivisionError, when calculating the angle.
            self.not_zero = 1

        self.angle = math.atan((self.event.y - self.y0) / self.not_zero)
        self.vx = self.v0 * math.cos(self.angle)
        self.vy = -self.v0 * math.sin(self.angle)
        self.t_ascent = self.vy / 9.8

        self.shell_avatar = window.canvas.create_oval(self.x, self.y - 2 * self.r,
                                                      self.x + 2 * self.r, self.y, fill=self.color, tag="bum")

    def move_shell(self):
        """Move the projectile after a unit of time.
        The velocities vx and vy take into account the force of gravity,
        and walls around the edges of the window.
        """
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

        window.canvas.coords(self.shell_avatar, self.x, self.y - 2 * self.r,
                             self.x + 2 * self.r, self.y)
        self.id_after = window.after(30, self.move_shell)
        if self.y >= HEIGHT:
            window.after_cancel(self.id_after)

        self.bum = self.hittest(targets)

    def hittest(self, targets):
        """The function checks if the given object collides with the target.
        """
        for target in targets:
            if (target.r + self.r) ** 2 >= ((target.x + target.r - (self.x + self.r)) ** 2 +
                                            (target.y + target.r - (self.y + self.r)) ** 2):
                self.namber = len(shells)
                window.drawing_hit(target, self.namber)
                shells.clear()
                targets.remove(target)
                window.after(3000, target.new_target)


class Target:
    def __init__(self):
        """Coordinates, radius and color of the target are random."""
        self.x = randint(WIDTH // 1.3, WIDTH // 1.1)
        self.y = randint(HEIGHT // 16, HEIGHT // 1.1)
        self.r = randint(8, 25)
        self.color = choice(('gray', 'blue', 'red', 'cyan', 'green'))

    def new_target(self):
        """Creating a new goal"""
        target = Target()
        targets.append(target)
        window.drawing_targets()


targets = []
guns = []
shells = []
window = Window()
gun = Gun()
guns.append(gun)
window.drawing_guns()
target = Target()
targets.append(target)
window.drawing_targets()
window.bind('<Motion>', gun.aiming)
window.bind('<Button-1>', gun.preparing)
window.bind('<B1-Motion>', gun.preparing)
window.bind('<ButtonRelease-1>', gun.fire)
window.mainloop()
