class Variable:
    def __init__(self, nombre, tam, dominio, tipo):
        self.valor = ""
        self.nombre = nombre
        self.tam = tam  
        self.dominio = list(dominio)
        self.restricciones = []  
        self.celdas = []
        self.tipo = tipo
        self.se_ha_borrado = False
        self.palabras_borradas = {}
        

    
    def __str__(self):

        nombre = str(self.nombre)
        fila, columna = map(str, self.celdas[0])
        tipo = self.tipo
        dominio = str(self.dominio)

        return f"Nombre {nombre} Posicion {fila} {columna} Tipo: {tipo} Dominio: {dominio}"
