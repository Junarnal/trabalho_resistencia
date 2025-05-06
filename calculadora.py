import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Retangulo:
    def __init__(self, base, altura, cx, cy, subtrair=False):
        self.base = base
        self.altura = altura
        self.centroide_x = cx
        self.centroide_y = cy
        self.subtrair = subtrair
        self.area = self.area()

    def area(self):
        if not (self.subtrair):
            return self.base * self.altura
        else:
            return self.base * self.altura * (-1)

    def momento_centroide_x(self):
       return (self.base * (self.altura ** 3)) / 12

    def momento_centroide_y(self):
       return ((self.base ** 3) * self.altura) / 12

    def momento_polar_centroide(self):
       return 0

    def momento_eixo_x(self):
       return (self.base * (self.altura ** 3)) / 3

    def momento_eixo_y(self):
       return ((self.base ** 3) * self.altura) / 3

    def momento_polar_origem(self):
       return (momento_eixo_x + momento_eixo_y)

class Plano_Cartesiano:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        #fig.patch.set_facecolor('#ffffff')      
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.press = False
        self.mouse_press = None
        self.xlim_press = None
        self.ylim_press = None

    def on_press(self, event):
        self.mouse_press = event
        self.xlim_press = self.ax.get_xlim()
        self.ylim_press = self.ax.get_ylim()
        self.press = True

    def on_motion(self, event):
        if(self.press):
            delta_x = event.xdata - self.mouse_press.xdata
            delta_y = event.ydata - self.mouse_press.ydata
            new_xlim = (self.xlim_press[0] - delta_x, self.xlim_press[1] - delta_x)
            new_ylim = (self.ylim_press[0] - delta_x, self.ylim_press[1] - delta_y)

            self.ax.set_xlim(new_xlim)
            self.ax.set_ylim(new_ylim)
            print(f'new_xlim: {new_xlim}, new_ylim: {new_ylim}')
            self.fig.canvas.draw()
            #print(delta_x, delta_y)

    def on_release(self, event):
        self.press = False

    def run(self):
        plt.show()

plano = Plano_Cartesiano()
plano.run()
