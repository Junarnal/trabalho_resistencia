import matplotlib.pyplot as plt
import matplotlib.patches as patches



plano = Plano_Cartesiano()
plano.adicionar_retangulos(2, 2, 0, 0)
plano.adicionar_retangulos(4, 4, -1, -1, True)
plano.adicionar_retangulos(3, 5, 2, 3)
plano.run()
