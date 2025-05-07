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
        if not self.subtrair:
            return patches.Rectangle((self.centroide_x - (self.base/2), self.centroide_y - (self.altura/2)), self.base, self.altura, linewidth=1, edgecolor='blue', facecolor='cyan')
        else:
            return patches.Rectangle(((self.base/2) - self.centroide_x, (self.altura/2) - self.centroide_y), self.base, self.altura, linewidth=1, edgecolor='red', facecolor='orange')

