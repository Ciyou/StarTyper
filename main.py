import tkinter as tk
import time
import random


class Rect:
    def __init__(self, canvas, x1, y1, x2, y2, shadow=5, force=lambda t: [0, 0], **kwargs):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.density = 1
        self.mass = (x2-x1) * (y2-y1) * self.density
        self.canvas = canvas
        self.shadow = shadow
        self.kwargs = kwargs
        self.gravity = False
        self.velocity = [0, 0]
        self.force = force
        self.lifetime = 0

        if 'font' in self.kwargs:
            self.font = self.kwargs['font']
        else:
            self.font = 'Hawaiian-Kids'

        if 'size' in self.kwargs:
            self.size = self.kwargs['size']
        else:
            self.size = 20

        if 'fill1' in self.kwargs:
            self.fill1 = self.kwargs['fill1']
        else:
            self.fill1 = '#FFC32E'

        if 'fill2' in self.kwargs:
            self.fill2 = self.kwargs['fill2']
        else:
            self.fill2 = '#F09B18'

        if 'width' in self.kwargs:
            self.width = self.kwargs['width']
        else:
            self.width = 0

        if 'text' in self.kwargs:
            self.text = self.kwargs['text']
        else:
            self.text = ''

        shadow = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2+self.shadow, fill=self.fill2, width=self.width)
        button = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, fill=self.fill1, width=self.width)
        text = self.canvas.create_text(
            (x2+x1)/2, (y2+y1)/2, text=self.text, font=self.font+" "+str(self.size))

        self.item = [button, shadow, text]
        self.sub = []

    def bind(self, event, func):
        for item in self.item:
            self.canvas.tag_bind(item, event, func)

    def update(self):
        self.lifetime += 1
        for item in self.item:
            if self.gravity:
                g = 0.15
            else:
                g = 0
            force = self.force(self.lifetime)
            dis_x = self.velocity[0] + \
                (force[0]/self.mass)/2
            dis_y = self.velocity[1] + (force
                                        [1]/self.mass)/2 + g/2
            self.velocity[0] += force[0]/self.mass
            self.velocity[1] += force[1] / \
                self.mass + g
            self.canvas.move(item, dis_x, dis_y)

        for sub in self.sub:
            sub.update()

    def boom(self, **kwargs):
        cood = self.canvas.coords(self.item[0])
        self.destroy()
        for _ in range(random.randint(3, 5)):
            x = random.randint(int(cood[0]), int(cood[2]))
            y = random.randint(int(cood[1]), int(cood[3]))
            size = random.randint(
                int((cood[3]-cood[1])/5), int((cood[3]-cood[1])/3))
            tmp = Rect(self.canvas, x, y, x+size, y+size, force=lambda t: [
                       random.randint(-1500, 1500), random.randint(-1000, 500)] if t <= 1 else [0, 0], **kwargs)
            tmp.gravity = True
            self.sub.append(tmp)

    def destroy(self):
        for item in self.item:
            self.canvas.delete(item)
        for sub in self.sub:
            for item in sub.item:
                self.canvas.delete(item)
        self.item.clear()
        self.sub.clear()


main_window = tk.Tk()
main_window.title('Star Typer')
main_window.geometry('400x600')


def game_scene():
    canvas = tk.Canvas(main_window, bg=None, width=400, height=600)
    canvas.pack()
    a = Rect(canvas, 0, 0, 100, 100)
    a.gravity = True
    for _ in range(200):
        a.update()
        canvas.update()
        time.sleep(0.01)
    global state
    canvas.destroy()
    start_scene()


def start_scene():
    bg_cube = []
    bg_fragment = []
    global state
    state = 'keep'
    canvas = tk.Canvas(main_window, bg=None, width=400, height=600)

    def game_start(event):
        global state
        state = 'start'

    def game_about(event):
        for item in bg_cube:
            if item.text != '':
                return
        cube = [Rect(canvas, -3+5, -50, -3+40, -15, fill1='#B9B9B9', fill2='#E0E0E0', text='c'),
                Rect(canvas, -3+45, -40, -3+80, -5,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='i'),
                Rect(canvas, -3+85, -50, -3+120, -15,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='l'),
                Rect(canvas, -3+125, -40, -3+160, -5,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='o'),
                Rect(canvas, -3+165, -50, -3+200, -15,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='v'),
                Rect(canvas, -3+205, -40, -3+240, -5,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='e'),
                Rect(canvas, -3+245, -50, -3+280, -15,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='y'),
                Rect(canvas, -3+285, -40, -3+320, -5,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='o'),
                Rect(canvas, -3+325, -50, -3+360, -15,
                     fill1='#B9B9B9', fill2='#E0E0E0', text='y'),
                Rect(canvas, -3+365, -40, -3+400, -5, fill1='#B9B9B9', fill2='#E0E0E0', text='o')]
        for item in cube:
            #item.gravity = True
            item.force = lambda t: [0, 800 if t <= 1 else 0]
            bg_cube.append(item)

    def game_quit(event):
        global state
        state = 'quit'

    def new_cube():
        x = random.randint(10, 570)
        y = random.randint(10, 250)
        cube = Rect(canvas, x, y, x+30, y+30, fill1='#B9B9B9', fill2='#E0E0E0')
        cube.force = lambda t: [0, random.randint(500, 1000) if t <= 1 else 0]
        return cube

    def new_cube_out():
        x = random.randint(10, 360)
        y = random.randint(-250, -30)
        cube = Rect(canvas, x, y, x+30, y+30, fill1='#B9B9B9', fill2='#E0E0E0')
        cube.force = lambda t: [0, random.randint(500, 1000) if t <= 1 else 0]
        return cube

    for _ in range(5):
        bg_cube.append(new_cube())

    canvas.place(x=0, y=0, anchor='nw')

    button_canvas_2 = tk.Canvas(main_window, width=200, height=55)
    button_canvas_3 = tk.Canvas(main_window, width=200, height=55)
    button_canvas_1 = tk.Canvas(main_window, width=200, height=55)

    button_canvas_1.configure(highlightthickness=0)
    button_canvas_2.configure(highlightthickness=0)
    button_canvas_3.configure(highlightthickness=0)

    button_canvas_1.place(x=100, y=330, anchor="nw")
    button_canvas_2.place(x=100, y=410, anchor="nw")
    button_canvas_3.place(x=100, y=490, anchor="nw")

    button = Rect(button_canvas_1, 0, 0, 200, 50, text='Start')
    button.bind('<Button-1>', game_start)

    button = Rect(button_canvas_2, 0, 0, 200, 50, text='About')
    button.bind('<Button-1>', game_about)

    button = Rect(button_canvas_3, 0, 0, 200, 50, text='Quit')
    button.bind('<Button-1>', game_quit)

    random.seed(time.clock())
    limit = random.randint(400, 600)

    while 1:
        if state == 'quit':
            break
        if state == 'start':
            canvas.destroy()
            button_canvas_1.destroy()
            button_canvas_2.destroy()
            button_canvas_3.destroy()
            game_scene()
        for cube in bg_cube:
            cube.update()
            if cube.text != '':
                if int(canvas.coords(cube.item[0])[1]) >= 600:
                    cube.destroy()
                    bg_cube.remove(cube)
            else:
                if int(canvas.coords(cube.item[0])[3]) >= limit:
                    cube.boom(fill1='#B9B9B9', fill2='#E0E0E0')
                    bg_fragment.append(cube)
                    bg_cube.remove(cube)
                    bg_cube.append(new_cube_out())
                    limit = random.randint(400, 600)
        for frag in bg_fragment:
            for sub in frag.sub:
                sub.update()
                if canvas.coords(sub.item[0])[1] >= 600:
                    sub.destroy()
                    frag.sub.remove(sub)
            if not frag.sub:
                frag.destroy()
                bg_fragment.remove(frag)

        canvas.update()
        button_canvas_1.update()
        button_canvas_2.update()
        button_canvas_3.update()
        time.sleep(0.01)


start_scene()
# cube = Rect(canvas, 100, 100, 150, 150, text='c')
# # cube.gravity = True
# cube.force = lambda t: [0, 1500 if t <= 1 else 0]


# flag = 0
# for i in range(500):
#     cube.update()
#     time.sleep(0.01)
#     canvas.update()
#     if flag != 1:
#         if int(canvas.coords(cube.item[0])[3]) >= 400:
#             print('Stop!')
#             cube.boom()
#             flag = 1

# print('Done')
# main_window.mainloop()
