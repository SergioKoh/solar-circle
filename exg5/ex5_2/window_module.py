import tkinter as tk

WIDTH, HEIGHT = 800, 600

class Window(tk.Tk):
    """Displaying objects on the canvas"""

    def __init__(self, w, h):
        super().__init__()
        self.title("Cannon Game OOP")
        x, y = self.center_screen()
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def center_screen(master):
        """Centering the window."""
        w = (master.winfo_screenwidth() - WIDTH) // 2
        h = (master.winfo_screenheight() - HEIGHT) // 2
        return w, h



    def drawing_guns(self, guns):
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

    def drawing_hit(self, target):
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
        self.canvas.delete(target.avatar)

    def drawing_text(self, namber):

        if namber > 1:
            self.canvas.create_text(WIDTH / 2, HEIGHT / 3, text=f"You destroyed two targets in {namber} shots",
                                    font=("Lucida Sans Unicode", 12, "bold"), tag='text')
        else:
            self.canvas.create_text(WIDTH / 2, HEIGHT / 3, text=f"You destroyed two targets in {namber} shot",
                                    font=("Lucida Sans Unicode", 12, "bold"), tag='text')