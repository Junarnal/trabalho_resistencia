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
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.press = False
        self.mouse_press = None
        self.last_mouse_pos = None
        self.scale = 1.0

    def on_press(self, event):
        inv = self.ax.transData.inverted()
        self.last_mouse_data = inv.transform((event.x, event.y))
        self.press = True

    def on_motion(self, event):
        if(self.press):
            inv = self.ax.transData.inverted()
            current_mouse_data = inv.transform((event.x, event.y))
            dx = current_mouse_data[0] - self.last_mouse_data[0]
            dy = current_mouse_data[1] - self.last_mouse_data[1]

            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
            self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
            self.fig.canvas.draw()

    def on_release(self, event):
        self.press = False

    def on_scroll(self, event):
        base_escala = 1.2
        if(event.button == 'up'):
            self.scale *= base_escala
        else:
            self.scale /= base_escala

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        self.ax.set_xlim(xlim[0] * self.scale, xlim[1] * self.scale)
        self.ax.set_ylim(ylim[0] * self.scale, ylim[1] * self.scale)
        self.fig.canvas.draw()

    def run(self):
        plt.show()

plano = Plano_Cartesiano()
plano.run()
