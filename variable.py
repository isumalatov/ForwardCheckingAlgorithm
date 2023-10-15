class Variable:
    def __init__(self, tamaño, dominio):
        self.tamaño = tamaño
        self.dominio = list(dominio)
        self.celda = []
        self.restriccionC = []  
