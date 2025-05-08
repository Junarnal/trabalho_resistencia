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

    def desenha(self):
        x = self.centroide_x - (self.base / 2)
        y = self.centroide_y - (self.altura / 2)
        cor_ret = 'cyan' if not self.subtrair else 'red'
        return patches.Rectangle((x, y), self.base, self.altura, linewidth=1, edgecolor='black', facecolor=cor_ret, alpha=0.5)

class Plano:
    def __init__(self, frame_tk) -> None:
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_tk)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        self.retangulos = []

    def adicionar_retangulo(self, altura, base, cx, cy, subtrair=False):
        ret = Retangulo(base, altura, cx, cy, subtrair)
        patch = ret.desenha()
        self.retangulos.append((ret, patch))
        self.ax.add_patch(patch)
        self.canvas.draw()

    def atualizar_canvas(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.grid(True)

        for ret, _ in self.retangulos:
            patch = ret.desenha()
            self.ax.add_patch(patch)

        self.canvas.draw()

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Momento de Inércia - Retângulos")

        # Interface lateral
        self.interface = tk.Frame(root)
        self.interface.pack(side=tk.LEFT, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(self.interface, columns=("Base", "Altura", "CX", "CY"), show="headings")
        for col in ("Base", "Altura", "CX", "CY"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=60)
        self.tree.pack()
        self.tree.bind("<<TreeviewSelect>>", self.retangulo_selecionado)

        # Campos de entrada
        self._criar_entrada("Base")
        self._criar_entrada("Altura")
        self._criar_entrada("CX")
        self._criar_entrada("CY")

        # Botões
        tk.Button(self.interface, text="Atualizar", command=self.atualizar_retangulo).pack(pady=5)
        tk.Button(self.interface, text="Excluir", command=self.excluir_retangulo).pack(pady=5)

        # Área gráfica
        self.frame_grafico = tk.Frame(root)
        self.frame_grafico.pack()
        self.plano = Plano(self.frame_grafico)

        # Dados iniciais
        self.adicionar_retangulo(3, 2, 0, 0)
        self.adicionar_retangulo(3, 2, 2, 2)

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _criar_entrada(self, label):
        lbl = tk.Label(self.interface, text=label + ":")
        lbl.pack()
        entry = tk.Entry(self.interface)
        entry.pack()
        setattr(self, f"entry_{label.lower()}", entry)

    def adicionar_retangulo(self, base, altura, cx, cy):
        self.plano.adicionar_retangulo(altura, base, cx, cy)
        index = len(self.plano.retangulos) - 1
        self.tree.insert("", tk.END, iid=str(index), values=(base, altura, cx, cy))

    def retangulo_selecionado(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        index = int(sel[0])
        ret, _ = self.plano.retangulos[index]

        self.entry_base.delete(0, tk.END)
        self.entry_base.insert(0, str(ret.base))
        self.entry_altura.delete(0, tk.END)
        self.entry_altura.insert(0, str(ret.altura))
        self.entry_cx.delete(0, tk.END)
        self.entry_cx.insert(0, str(ret.centroide_x))
        self.entry_cy.delete(0, tk.END)
        self.entry_cy.insert(0, str(ret.centroide_y))

    def atualizar_retangulo(self):
        sel = self.tree.selection()
        if not sel:
            return
        index = int(sel[0])
        try:
            base = float(self.entry_base.get())
            altura = float(self.entry_altura.get())
            cx = float(self.entry_cx.get())
            cy = float(self.entry_cy.get())
        except ValueError:
            print("Entradas inválidas.")
            return

        ret, _ = self.plano.retangulos[index]
        ret.base = base
        ret.altura = altura
        ret.centroide_x = cx
        ret.centroide_y = cy
        self.tree.item(sel[0], values=(base, altura, cx, cy))
        self.plano.atualizar_canvas()

    def excluir_retangulo(self):
        sel = self.tree.selection()
        if not sel:
            return
        index = int(sel[0])
        del self.plano.retangulos[index]
        self.tree.delete(sel[0])

        # Reindexa a árvore e lista
        self.tree.delete(*self.tree.get_children())
        novas = []
        for i, (ret, _) in enumerate(self.plano.retangulos):
            novas.append((i, ret.base, ret.altura, ret.centroide_x, ret.centroide_y))
        self.plano.atualizar_canvas()
        self.plano.retangulos = [(ret, ret.desenha()) for _, base, altura, cx, cy in novas for ret in [Retangulo(base, altura, cx, cy)]]
        for i, ret in enumerate(self.plano.retangulos):
            r, _ = ret
            self.tree.insert("", tk.END, iid=str(i), values=(r.base, r.altura, r.centroide_x, r.centroide_y))

    def run(self):
        self.root.mainloop()

root = tk.Tk()
app = Window(root)
app.run()

