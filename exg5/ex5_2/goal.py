from random import randint
from random import choice
from screen import *

WIDTH, HEIGHT = 800, 600

class Target:
    def __init__(self):
        """Coordinates, radius and color of the target are random."""
        self.x = randint(WIDTH // 2, WIDTH // 1.1)
        self.y = randint(HEIGHT // 16, HEIGHT // 1.1)
        self.r = randint(8, 25)
        self.color = choice(('yellow', 'blue', 'red', 'cyan', 'green', 'lime', 'purple'))
        self.dx = 0
        self.dy = choice((-2, -1, 1, 2))

    @staticmethod
    def new_targets(targets, window):
        """Creating a new goal"""
        for i in range(2):
            target = Target()
            targets.append(target)
            target.drawing_target(window)
            target.move_target(targets, window)

    def drawing_target(self, window):
        """Drawing goals."""
        window.canvas.delete("text")
        window.canvas.delete("bum")
        self.avatar = window.canvas.create_oval(self.x - self.r, self.y - self.r,
                                                  self.x + self.r, self.y + self.r, fill=self.color)


    def move_target(self, targets, window):
        """Drawing moving targets"""
        id_after = window.after(30, self.move_target, targets, window)
        if not self in targets:
            window.after_cancel(id_after)
        window.canvas.move(self.avatar, self.dx, self.dy)
        self.y += self.dy
        if self.y >= HEIGHT - self.r or self.y <= 0 + self.r:
            self.dy = - self.dy
