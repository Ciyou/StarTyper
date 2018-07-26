import tkinter as tk
import time
import random

class Rect:
    def __init__(self, canvas, x1, y1, x2, y2, shadow=5, force=lambda t:[0,0], **kwargs):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.density = 1
        self.mass = (x2-x1) * (y2-y1) * self.density
        self.canvas = canvas
        self.shadow=shadow
        self.kwargs = kwargs
        self.gravity = False
        self.velocity = [0,0]
        self.force = force
        self.lifetime = 0

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
        
        
        shadow = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2+self.shadow,fill=self.fill2, width=self.width)
        button = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=self.fill1, width=self.width)
        text = self.canvas.create_text((x2+x1)/2,(y2+y1)/2, text=self.text)

        self.item = [button, shadow, text]
        self.sub = []
    
    def bind(self, event, func):
        for item in self.item:
            self.canvas.tag_bind(item, event, func)

    def update(self):
        self.lifetime += 1
        print(self.item)
        for item in self.item:
            if self.gravity:
                g = 3.8
            else:
                g = 0
            print(self.force(self.lifetime))
            dis_x = self.velocity[0] + (self.force(self.lifetime)[0]/self.mass)/2 
            dis_y = self.velocity[1] + (self.force(self.lifetime)[1]/self.mass)/2 + (g/self.mass)/2
            self.velocity[0] += self.force(self.lifetime)[0]/self.mass 
            self.velocity[1] += self.force(self.lifetime)[1]/self.mass + (g/self.mass)/2
            self.canvas.move(item, dis_x, dis_y)
        for sub in self.sub:
            sub.update()
            print(1)

    def boom(self):
        cood = self.canvas.coords(self.item[0])
        self.destroy()
        print(self.item)
        for _ in range(random.randint(3,5)):
            x = random.randint(int(cood[0]),int(cood[2]))
            y = random.randint(int(cood[1]), int(cood[3]))
            size = random.randint(int((cood[3]-cood[1])/5),int((cood[3]-cood[1])/2))
            tmp = Rect(self.canvas, x,y,x+size, y+size, force=lambda t: [random.randint(-50,50), random.randint(-50,10)] if t < 10 else [0,0])
            tmp.gravity = True
            self.sub.append(tmp)

    def destroy(self):
        for item in self.item:
            self.canvas.delete(item)
        self.item.clear()

def test(event):
    print("happy")

main_window = tk.Tk()
main_window.title('Star Typer')
main_window.geometry('400x600')

canvas = tk.Canvas(main_window, bg='white', width=400, height=600)


#button = Rect(canvas, 100,350,300,400, text='Start')
#button.bind('<Button-1>', test)

cube = Rect(canvas, 100,100,150,150,text='c')
cube.gravity = True

canvas.pack()
flag=0
for i in range(5000):
    cube.update()  
    time.sleep(0.001)
    canvas.update()
    if flag!=1:
        if int(canvas.coords(cube.item[0])[3])>=400:
            print('Stop!')
            cube.boom()
            flag=1
 
print('DOne')
main_window.mainloop()
