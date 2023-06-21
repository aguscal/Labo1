import pygame

def crear_disparo(x,y,ancho=4,alto=8):
    imagen_disparo = pygame.image.load("laser.png")
    imagen_disparo = pygame.transform.scale(imagen_disparo,(ancho,alto))
    rect_disparo = imagen_disparo.get_rect()
    
    #rect_disparo.y -= 5
    
    rect_disparo.x = x + 22
    rect_disparo.y = y - 20
    dic_disparo = {}
    dic_disparo["imagen"] = imagen_disparo
    dic_disparo["rect"] = rect_disparo
    dic_disparo["visible"] = True

    return dic_disparo


def crear_disparo_enemigo(x,y,ancho=4,alto=8):
    imagen_disparo = pygame.image.load("laser.png")
    imagen_disparo = pygame.transform.scale(imagen_disparo,(ancho,alto))
    rect_disparo = imagen_disparo.get_rect()
    
    #rect_disparo.y -= 5
    
    rect_disparo.x = x + 15
    rect_disparo.y = y 
    dic_disparo = {}
    dic_disparo["imagen"] = imagen_disparo
    dic_disparo["rect"] = rect_disparo
    dic_disparo["visible"] = True

    return dic_disparo