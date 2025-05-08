import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Retangulo:
    def __init__(self, base, altura, cx, cy, subtrair=False):
        self.base = base
        self.altura = altura
        self.centroide_x = cx
        self.centroide_y = cy
        self.subtrair = subtrair
        self.area = self.base * self.altura if not subtrair else self.base * self.altura * (-1)

    def desenha(self):
        x = self.centroide_x - (self.base/2)
        y = self.centroide_y - (self.altura/2)
        cor_ret = 'cyan' if not self.subtrair else 'red'
        
        return patches.Rectangle((x, y), self.base, self.altura, linewidth=1, edgecolor='black', facecolor=cor_ret, alpha= 0.5)
        
class Plano:
    def __init__(self, frame_tk) -> None:
        #inicializa o plano
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_tk)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        self.press = False
        self.last_mouse_pos = None
        self.retangulos = []

        self.fig.canvas.mpl_connect('button_press_event', self.mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.fig.canvas.mpl_connect('button_release_event', self.mouse_release)
        self.fig.canvas.mpl_connect('scroll_event', self.mouse_scroll)

    def adicionar_retangulos(self, altura, base, centroide_x, centroide_y, subtrair = False):
        retangulo = Retangulo(altura, base, centroide_x, centroide_y, subtrair)
        desenho = retangulo.desenha()
        self.retangulos.append((retangulo, desenho))
        self.ax.add_patch(desenho)

    def atualizar_retangulos(self):
        ret, patch = self.retangulos[0]
        patch.remove()  # Remove o patch antigo do gráfico

        # Atualiza o objeto
        ret.subtrair = True
        ret.centroide_x = -2
        # Cria novo patch com nova cor
        novo_patch = ret.desenha()
        self.ax.add_patch(novo_patch)  # Adiciona o novo patch ao gráfico

        self.retangulos[0] = (ret, novo_patch)  # Atualiza a lista
        self.canvas.draw()

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

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Momento de Inércia")

        self.interface = tk.Frame(root)
        self.interface.grid(row=0, column=0, padx=10, pady=10)
        self.tree = ttk.Treeview(self.interface, columns=("Base", "Altura", "Cx", "Cy", "Subtrair"), show="headings", height=7)
        self.tree.grid(row=4, column=0, columns=2, pady=10)

        self.tree.heading("Base", text="Base")
        self.tree.heading("Altura", text="Altura")
        self.tree.heading("Cx", text="Cx")
        self.tree.heading("Cy", text="Cy")
        self.tree.heading("Subtrair", text="Subtrair Área")

        self.label_centroide_x = tk.Label(self.interface, text="Centroide x:")
        self.label_centroide_x.grid(row=0, column=0)
        self.label_centroide_y = tk.Label(self.interface, text="Centroide y:")
        self.label_centroide_y.grid(row=1, column=0)
        self.label_base = tk.Label(self.interface, text="Base:")
        self.label_base.grid(row=2, column=0)
        self.label_altura = tk.Label(self.interface, text="Altura:")
        self.label_altura.grid(row=3, column=0)

        self.entrada_centroide_x = tk.Entry(self.interface)
        self.entrada_centroide_x.grid(row=0, column=1, padx=5)
        self.entrada_centroide_y = tk.Entry(self.interface)
        self.entrada_centroide_y.grid(row=1, column=1, padx=5)
        self.entrada_base = tk.Entry(self.interface)
        self.entrada_base.grid(row=2, column=1, padx=5)
        self.entrada_altura = tk.Entry(self.interface)
        self.entrada_altura.grid(row=3, column=1, padx=5)

        self.checkbox_subtrair = tk.BooleanVar()
        checkbox_subtrair = tk.Checkbutton(self.interface, text = "Subtrair área", variable = self.checkbox_subtrair, onvalue = True, offvalue = False)
        checkbox_subtrair.grid(row = 5, column = 3)

        botao_adicionar = tk.Button(self.interface, text="Adicionar", command=self.adicionar_retangulo)
        botao_adicionar.grid(row=5, column=0, columnspan=2, pady=5)

        botao_atualizar = tk.Button(self.interface, text="Atualizar", command=self.atualizar_retangulo)
        botao_atualizar.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

        botao_remover = tk.Button(self.interface, text="Remover", command=self.remover_retangulo)
        botao_remover.grid(row=5, column=2, padx=10, pady=5)

        self.frame_grafico = tk.Frame(root)
        self.frame_grafico.grid(row=0, column=1)
        self.plano = Plano(self.frame_grafico)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def adicionar_retangulo(self):
        try:
            centroide_x = float(self.entrada_centroide_x.get())
            centroide_y = float(self.entrada_centroide_y.get())
            base = float(self.entrada_base.get())
            altura = float(self.entrada_altura.get())
        except ValueError:
            return

        self.plano.adicionar_retangulos(altura, base, centroide_x, centroide_y, self.checkbox_subtrair.get())
        self.tree.insert("", "end", values=(base, altura, centroide_x, centroide_y, self.checkbox_subtrair.get()))
        self.plano.canvas.draw()

    def atualizar_retangulo(self):
        try:
            centroide_x = float(self.entrada_centroide_x.get())
            centroide_y = float(self.entrada_centroide_y.get())
            base = float(self.entrada_base.get())
            altura = float(self.entrada_altura.get())
        except ValueError:
            return


        item = self.tree.selection()[0]
        index = self.tree.index(item)

        valores = self.tree.item(item, "values")

        self.entrada_base.delete(0, tk.END)
        self.entrada_base.insert(0, valores[0])

        ret, patch = self.plano.retangulos[index]
        patch.remove()

        ret.centroide_x = centroide_x
        ret.centroide_y = centroide_y
        ret.base = base
        ret.altura = altura
        ret.subtrair = self.checkbox_subtrair.get()
        
        novo_patch = ret.desenha()
        self.plano.retangulos[index] = (ret, novo_patch)
        self.plano.ax.add_patch(novo_patch)
        self.plano.canvas.draw()
        self.tree.item(item, values=(base, altura, centroide_x, centroide_y, self.checkbox_subtrair.get()))

        

    def remover_retangulo(self):
        item = self.tree.selection()[0]
        index = self.tree.index(item)
        self.tree.delete(item)
        ret, patch = self.plano.retangulos[index]
        patch.remove()
        self.plano.retangulos.pop(index)
        self.plano.canvas.draw()

    def on_close(self):
        self.root.destroy()
        exit()

    def run(self):
        self.root.mainloop()

root = tk.Tk()
app = Window(root)
app.run()
