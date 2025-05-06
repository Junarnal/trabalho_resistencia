import matplotlib.pyplot as plt

class Plano_Cartesiano:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.press = False
        self.last_mouse_data = None

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.x is not None and event.y is not None:
            inv = self.ax.transData.inverted()
            self.last_mouse_data = inv.transform((event.x, event.y))
            self.press = True

    def on_motion(self, event):
        if self.press and event.x is not None and event.y is not None:
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

    def run(self):
        plt.show()

plano = Plano_Cartesiano()
plano.run()

