from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class Subarea:
    def __init__(self, base, altura, cx, cy, adicionar=True):
        self.base = base
        self.altura = altura
        self.cx = cx
        self.cy = cy
        self.adicionar = adicionar

    def Ix_c(self):
        return (self.base * self.altura ** 3) / 12

    def Iy_c(self):
        return (self.altura * self.base ** 3) / 12

    def Ix(self, ox):
        dy = self.cy - ox
        return self.Ix_c() + self.area() * dy ** 2

    def Iy(self, oy):
        dx = self.cx - oy
        return self.Iy_c() + self.area() * dx ** 2

    def Ixy(self, ox, oy):
        dx = self.cx - oy
        dy = self.cy - ox
        return self.area() * dx * dy

    def area(self):
        return self.base * self.altura if self.adicionar else -self.base * self.altura

def main():
    subareas = []
    print("=== Entrada de subáreas (retângulos) ===")
    while True:
        try:
            b = float(input("Base: "))
            h = float(input("Altura: "))
            cx = float(input("Cx (centro em x): "))
            cy = float(input("Cy (centro em y): "))
            tipo = input("Adicionar (a) ou Subtrair (s)? [a/s]: ").strip().lower()
            adicionar = tipo != 's'
            subareas.append(Subarea(b, h, cx, cy, adicionar))
        except ValueError:
            print("Valores inválidos. Tente novamente.")
            continue

        cont = input("Deseja adicionar outra subárea? [s/n]: ").strip().lower()
        if cont != 's':
            break

    try:
        ox = float(input("Origem Ox: "))
        oy = float(input("Origem Oy: "))
    except ValueError:
        print("Valores inválidos para origem.")
        return

    Ix = sum(s.Ix(ox) for s in subareas)
    Iy = sum(s.Iy(oy) for s in subareas)
    Ixy = sum(s.Ixy(ox, oy) for s in subareas)
    Jo = Ix + Iy

    print("\n=== Resultados ===")
    print(f"Ix = {Ix:.2f}")
    print(f"Iy = {Iy:.2f}")
    print(f"Ixy = {Ixy:.2f}")
    print(f"Jo = {Jo:.2f}")

    fig, ax = plt.subplots()
    for s in subareas:
        color = 'blue' if s.adicionar else 'red'
        rect = Rectangle((s.cx - s.base / 2, s.cy - s.altura / 2), s.base, s.altura, fill=True, color=color, alpha=0.5)
        ax.add_patch(rect)

    ax.axhline(y=ox, color='black', linestyle='--')
    ax.axvline(x=oy, color='black', linestyle='--')
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_aspect('equal')
    ax.set_title("Área Composta (azul = adição, vermelho = subtração)")
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    main()

