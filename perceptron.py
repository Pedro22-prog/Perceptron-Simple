import numpy as ny

class Perceptron:
    def __init__(self, valoresEntrada, pesos, bias, tipo):
        self.valoresEntrada = valoresEntrada
        self.pesos = pesos
        self.bias = bias
        self.suma = 0
        self.tipo = tipo


    def start_function(self):
        match self.tipo:
            case 'escalon':
                return 1 if self.suma >= 0 else 0
            case 'sigmoide':
                return 1 / (1 + ny.exp(-self.suma))

    def resultado(self):
        for i in range(len(self.valoresEntrada)):
            self.suma += self.valoresEntrada[i] * self.pesos[i]
        self.suma += self.bias
        return self.start_function()