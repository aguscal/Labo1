import pygame
import colores

class Nave:
    def __init__(self,posicion_inicial=(205,450)):
        self.imagen = pygame.image.load("nave_jugador.png")
        self.imagen = pygame.transform.scale(self.imagen,(45,45))
        #self.imagen = self.imagen.convert()
        self.rect = self.imagen.get_rect()

        self.rect.x = posicion_inicial[0]
        self.rect.y = posicion_inicial[1]

    def mover_derecha(self,movimiento:int):
        self.rect.x = self.rect.x + movimiento
    
    def mover_izquierda(self,movimiento:int):
        self.rect.x = self.rect.x - movimiento
        
    def manejar_evento_teclado(self,ancho_ventana:int,movimiento:int):
        lista_teclas = pygame.key.get_pressed()
        if True in lista_teclas:
            if lista_teclas[pygame.K_RIGHT] and self.rect.right < ancho_ventana:
                self.mover_derecha(movimiento)
        
            if lista_teclas[pygame.K_LEFT] and self.rect.left > 0:
                self.mover_izquierda(movimiento)
   
    def colision_disparo_enemigo():
        print("ACA TIENE QEU COLISIONAR LOS DOS Y DESPARECER LA NAVE O HACER ALGO NO SE o capas esto es en otro lado para ver si sigue corriendo o no el juego")
