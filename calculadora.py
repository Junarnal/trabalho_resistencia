import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

    def desenha(self):
        return 


class Plano_Cartesiano:
    def __init__(self) -> None:
        #inicializa o plano
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        
        #define os limites iniciais dos eixos
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        
        #configura o visual do plano
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        #define as funcoes que receberam os eventos do mouse
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.fig.canvas.mpl_connect('button_release_event', self.mouse_release)
        self.fig.canvas.mpl_connect('scroll_event', self.mouse_scroll)
        self.press = False
        self.last_mouse_pos = None

        self.rect = patches.Rectangle((0, 0), 2, 3, linewidth=1, edgecolor='r', facecolor="none")
        self.ax.add_patch(self.rect)

    def mouse_press(self, event) -> None:
        inv = self.ax.transData.inverted()
        self.last_mouse_data = inv.transform((event.x, event.y))
        self.press = True

    def mouse_move(self, event) -> None:
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

    def mouse_release(self, event) -> None:
        self.press = False

    def mouse_scroll(self, event) -> None:
        if event.xdata is None or event.ydata is None:
            return

        base_scale = 1.1
        if event.button == 'up':
          scale_factor = 1 / base_scale
        elif event.button == 'down':
          scale_factor = base_scale
        else:
          scale_factor = 1

        curr_xlim = self.ax.get_xlim()
        curr_ylim = self.ax.get_ylim()

        new_xlim = [event.xdata - (event.xdata - curr_xlim[0]) * scale_factor, event.xdata + (curr_xlim[1] - event.xdata) * scale_factor]
        new_ylim = [event.ydata - (event.ydata - curr_ylim[0]) * scale_factor, event.ydata + (curr_ylim[1] - event.ydata) * scale_factor]

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.fig.canvas.draw()

    def run(self):
        plt.show()

plano = Plano_Cartesiano()
plano.run()
