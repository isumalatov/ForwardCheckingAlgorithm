# Representa el crucigrama: medidas y matriz correspondiente a las celdas
class Tablero:    
    def __init__(self, FILS, COLS):
        self.ancho=COLS
        self.alto=FILS    
        self.tablero=[]
        
        for i in range(self.alto):
            self.tablero.append([])
            for j in range(self.ancho):
                self.tablero[i].append('-')
                 
        
    def __str__(self):
        salida=""
        for f in range(self.alto):            
            for c in range(self.ancho):
                salida += self.tablero[f][c]                
            salida += "\n"
        return salida
       
    def reset(self):
        for f in range(self.alto):
            for c in range(self.ancho):
                self.tablero[f][c]='-'        
       
    def getAncho(self):
        return self.ancho
    
    def getAlto(self):
        return self.alto
    
    def getCelda(self, fila, col):
        return self.tablero[fila][col]
    
    def setCelda(self, fila, col, val):
        self.tablero[fila][col]=val    
    