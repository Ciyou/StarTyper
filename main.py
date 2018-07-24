import tkinter as tk


class Rect:
    def __init__(self, x1, y1, x2, y2, shadow=5, **kwargs):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.shadow=shadow
        self.kwargs = kwargs

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
        
        self.item = []
    
    def draw(self, canvas):
        button = canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=self.fill1, width=self.width)
        shadow = canvas.create_rectangle(self.x1,self.y2,self.x2,self.y2+self.shadow,fill=self.fill2, width=self.width)

        


def button(canvas, x1, y1, x2, y2, shadow=5, fill1='#FFC32E', fill2='#F09B18', width=0, text=''):
    canvas.create_rectangle(x1,y1,x2,y2,fill=fill1, width=width)
    canvas.create_rectangle(x1,y2,x2,y2+shadow,fill=fill2, width=width)


main_window = tk.Tk()
main_window.title('Star Typer')
main_window.geometry('400x600')

canvas = tk.Canvas(main_window, bg='white', width=400, height=600)


button(canvas, 100,100,200,200)
canvas.pack()

main_window.mainloop()
