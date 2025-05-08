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
        x = self.centroide_x - (self.base / 2)
        y = self.centroide_y - (self.altura / 2)
        cor_ret = 'cyan' if not self.subtrair else 'red'
        return patches.Rectangle((x, y), self.base, self.altura, linewidth=1, edgecolor='black', facecolor=cor_ret, alpha=0.5)

class Plano:
    def __init__(self, frame_tk) -> None:
        self.fig, self.ax = plt.subplots(figsize=(6, 6))  # menor para telas normais
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['top'].set_position('zero')
        self.ax.spines['right'].set_position('zero')
        self.ax.spines['left'].set_color('black')
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color('black')
        self.ax.spines['right'].set_color('black')
#        self.ax.tick_params(top=True, labeltop=True)
#        self.ax.tick_params(right=True, labelright=True)



        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_tk)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.draw()

        self.press = False
        self.last_mouse_pos = None
        self.retangulos = []

        self.fig.canvas.mpl_connect('button_press_event', self.mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.fig.canvas.mpl_connect('button_release_event', self.mouse_release)
        self.fig.canvas.mpl_connect('scroll_event', self.mouse_scroll)

    def atualizar_spines(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
    
        x0_visivel = ylim[0] <= 0 <= ylim[1]
        y0_visivel = xlim[0] <= 0 <= xlim[1]
    
        # ----------------------
        # EIXO X (horizontal)
        # ----------------------
        if x0_visivel:
            # Eixo X aparece em y = 0
            self.ax.spines['bottom'].set_position(('data', 0))
            self.ax.spines['top'].set_position(('outward', 1000))  # some com o de cima
            self.ax.tick_params(bottom=True, labelbottom=True)
            self.ax.tick_params(top=False, labeltop=False)
        else:
            # Fora da tela, mostrar no limite mais próximo de Y
            if ylim[1] < 0:
                # Estamos no 3º quadrante -> eixo em cima
                self.ax.spines['top'].set_position(('axes', 1))
                self.ax.spines['bottom'].set_position(('outward', 1000))  # some com o de baixo
                self.ax.tick_params(top=True, labeltop=True)
                self.ax.tick_params(bottom=False, labelbottom=False)
            else:
                # Estamos no 1º ou 2º quadrante -> eixo embaixo
                self.ax.spines['bottom'].set_position(('axes', 0))
                self.ax.spines['top'].set_position(('outward', 1000))  # some com o de cima
                self.ax.tick_params(bottom=True, labelbottom=True)
                self.ax.tick_params(top=False, labeltop=False)
    
        # ----------------------
        # EIXO Y (vertical)
        # ----------------------
        if y0_visivel:
            # Eixo Y aparece em x = 0
            self.ax.spines['left'].set_position(('data', 0))
            self.ax.spines['right'].set_position(('outward', 1000))  # some com o da direita
            self.ax.tick_params(left=True, labelleft=True)
            self.ax.tick_params(right=False, labelright=False)
        else:
            # Fora da tela, mostrar no limite mais próximo de X
            if xlim[0] > 0:
                # Estamos no 1º ou 4º quadrante -> eixo à esquerda
                self.ax.spines['left'].set_position(('axes', 0))
                self.ax.spines['right'].set_position(('outward', 1000))
                self.ax.tick_params(left=True, labelleft=True)
                self.ax.tick_params(right=False, labelright=False)
            else:
                # Estamos no 2º ou 3º quadrante -> eixo à direita
                self.ax.spines['right'].set_position(('axes', 1))
                self.ax.spines['left'].set_position(('outward', 1000))
                self.ax.tick_params(right=True, labelright=True)
                self.ax.tick_params(left=False, labelleft=False)
    
        self.canvas.draw()
    
     
    def adicionar_retangulos(self, altura, base, centroide_x, centroide_y, subtrair=False):
        retangulo = Retangulo(altura, base, centroide_x, centroide_y, subtrair)
        desenho = retangulo.desenha()
        self.retangulos.append((retangulo, desenho))
        self.ax.add_patch(desenho)

    def atualizar_retangulos(self):
        ret, patch = self.retangulos[0]
        patch.remove()
        ret.subtrair = True
        ret.centroide_x = -2
        novo_patch = ret.desenha()
        self.ax.add_patch(novo_patch)
        self.retangulos[0] = (ret, novo_patch)
        self.canvas.draw()

    def mouse_press(self, event) -> None:
        inv = self.ax.transData.inverted()
        self.last_mouse_data = inv.transform((event.x, event.y))
        self.press = True

    def mouse_move(self, event) -> None:
        if self.press:
            self.atualizar_spines()
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
        self.atualizar_spines()
        base_scale = 1.1
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1
        curr_xlim = self.ax.get_xlim()
        curr_ylim = self.ax.get_ylim()
        new_xlim = [event.xdata - (event.xdata - curr_xlim[0]) * scale_factor,
                    event.xdata + (curr_xlim[1] - event.xdata) * scale_factor]
        new_ylim = [event.ydata - (event.ydata - curr_ylim[0]) * scale_factor,
                    event.ydata + (curr_ylim[1] - event.ydata) * scale_factor]
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.fig.canvas.draw()

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Momento de Inércia")
        self.root.geometry("900x700")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=3)

        self.interface = tk.Frame(root)
        self.interface.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

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
        checkbox_subtrair = tk.Checkbutton(self.interface, text="Subtrair área", variable=self.checkbox_subtrair)
        checkbox_subtrair.grid(row=0, column=2, padx=10)

        botao_adicionar = tk.Button(self.interface, text="Adicionar", command=self.adicionar_retangulo)
        botao_adicionar.grid(row=1, column=2, padx=5)

        botao_atualizar = tk.Button(self.interface, text="Atualizar", command=self.atualizar_retangulo)
        botao_atualizar.grid(row=2, column=2, padx=5)

        botao_remover = tk.Button(self.interface, text="Remover", command=self.remover_retangulo)
        botao_remover.grid(row=3, column=2, padx=5)

        self.tree = ttk.Treeview(self.interface, columns=("Base", "Altura", "Cx", "Cy", "Subtrair"), show="headings", height=6)
        self.tree.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')

        for col in ("Base", "Altura", "Cx", "Cy", "Subtrair"):
            self.tree.heading(col, text=col)

        self.frame_grafico = tk.Frame(root)
        self.frame_grafico.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.frame_grafico.rowconfigure(0, weight=1)
        self.frame_grafico.columnconfigure(0, weight=1)

        self.plano = Plano(self.frame_grafico)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def adicionar_retangulo(self):
        try:
            cx = float(self.entrada_centroide_x.get())
            cy = float(self.entrada_centroide_y.get())
            base = float(self.entrada_base.get())
            altura = float(self.entrada_altura.get())
        except ValueError:
            return
        subtrair = self.checkbox_subtrair.get()
        self.plano.adicionar_retangulos(altura, base, cx, cy, subtrair)
        self.tree.insert("", "end", values=(base, altura, cx, cy, subtrair))
        self.plano.canvas.draw()

    def atualizar_retangulo(self):
        try:
            cx = float(self.entrada_centroide_x.get())
            cy = float(self.entrada_centroide_y.get())
            base = float(self.entrada_base.get())
            altura = float(self.entrada_altura.get())
        except ValueError:
            return
        item = self.tree.selection()[0]
        index = self.tree.index(item)
        ret, patch = self.plano.retangulos[index]
        patch.remove()
        ret.centroide_x = cx
        ret.centroide_y = cy
        ret.base = base
        ret.altura = altura
        ret.subtrair = self.checkbox_subtrair.get()
        novo_patch = ret.desenha()
        self.plano.retangulos[index] = (ret, novo_patch)
        self.plano.ax.add_patch(novo_patch)
        self.plano.canvas.draw()
        self.tree.item(item, values=(base, altura, cx, cy, self.checkbox_subtrair.get()))

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

