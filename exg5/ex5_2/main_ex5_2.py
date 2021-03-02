
from gun_module import *


WIDTH, HEIGHT = 800, 600




guns = []
shells = []
targets = []
window = Window(WIDTH, HEIGHT)
gun = Gun()
guns.append(gun)
window.drawing_guns(guns)
for i in range(2):
    target = Target()
    targets.append(target)
    target.drawing_target(window)
    target.move_target(targets, window)
window.bind('<Motion>', lambda event: gun.aiming(event, guns, window))
window.bind('<Button-1>', lambda event: gun.preparing(event, guns, window))
window.bind('<B1-Motion>', lambda event: gun.preparing(event, guns, window))
window.bind('<ButtonRelease-1>', lambda event: gun.fire(event, guns, shells, targets, window))
window.mainloop()
