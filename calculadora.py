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

xmin = -5
xmax = 5
ymin = -5
ymax = 5
plt.rcParams['toolbar'] = 'none'

fig, ax = plt.subplots(figsize=(10, 10))
#fig.patch.set_facecolor('#ffffff')


ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.set_aspect('equal')
ax.grid(True)

plt.show()

