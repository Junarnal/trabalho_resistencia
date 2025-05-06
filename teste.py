import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


def make_error_boxes(ax, x, y, base, altura, facecolor='g',
                     edgecolor='none', alpha=0.75):

    # Loop over data points; create box from errors at each point
    errorboxes = [Rectangle((x-base/2, y-altura/2), base, altura)]

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(errorboxes, facecolor=facecolor, alpha=alpha,
                         edgecolor=edgecolor)

    # Add collection to Axes
    ax.add_collection(pc)

    # Plot errorbars
    artists = errorboxes

    return artists



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

    def on_scroll(self,event):
        base_scale = 1.1
        if event.button == 'up':
          scale_factor = 1 / base_scale
        elif event.button == 'down':
          scale_factor = base_scale
        else:
          scale_factor = 1

        curr_xlim = self.ax.get_xlim()
        curr_ylim = self.ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata

        if xdata is None or ydata is None:
          return

        new_xlim = [xdata - (xdata - curr_xlim[0]) * scale_factor,xdata + (curr_xlim[1] - xdata) * scale_factor]
        new_ylim = [ydata - (ydata - curr_ylim[0]) * scale_factor,ydata + (curr_ylim[1] - ydata) * scale_factor]

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.fig.canvas.draw_idle()

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
        _ = make_error_boxes(self.ax,2,2,1,2)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        plt.show()

plano = Plano_Cartesiano()
plano.run()

