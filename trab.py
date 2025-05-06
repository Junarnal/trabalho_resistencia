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
        self.mouse_press = None
        self.xlim_on_press = None
        self.ylim_on_press = None

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.mouse_press = event
            self.xlim_on_press = self.ax.get_xlim()
            self.ylim_on_press = self.ax.get_ylim()
            self.press = True

    def on_motion(self, event):
        if self.press and event.xdata is not None and event.ydata is not None:
            dx = event.xdata - self.mouse_press.xdata
            dy = event.ydata - self.mouse_press.ydata

            # Atualiza os limites dos eixos
            new_xlim = (self.xlim_on_press[0] - dx, self.xlim_on_press[1] - dx)
            new_ylim = (self.ylim_on_press[0] - dy, self.ylim_on_press[1] - dy)

            self.ax.set_xlim(new_xlim)
            self.ax.set_ylim(new_ylim)
            self.fig.canvas.draw_idle()

    def on_release(self, event):
        self.press = False

    def run(self):
        plt.show()

plano = Plano_Cartesiano()
plano.run()

