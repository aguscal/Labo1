import pygame
import colores
import random

def crear_nave_enemiga(x,y,ancho,alto):
    opciones = ["nave_enemiga_azul.png","nave_enemiga_verde.png"]
    imagen_elegida = random.choice(opciones)

    imagen_nave = pygame.image.load(imagen_elegida)
    imagen_nave = pygame.transform.scale(imagen_nave,(ancho,alto))#tamaño de la imagen
    rectangulo_nave = imagen_nave.get_rect()
    rectangulo_nave.x = x#modificar la posicion de la imagen en el horizontal
    rectangulo_nave.y = y#modificar la posicion de la imagen en el vertical
    #guardar la imagen y el rect de la imagen en un diccionario
    dic_nave = {}
    dic_nave["imagen"] = imagen_nave
    dic_nave["rect"] = rectangulo_nave
    dic_nave["visible"] = True
    dic_nave["ancho"] = ancho
    dic_nave["alto"] = alto
    dic_nave["x"] = x
    dic_nave["velocidad"] = 1
    dic_nave["disparo"] = False

    return dic_nave

def crear_lista_naves_enemigas(cantidad):
    lista_naves = []
    y = 40

    for j in range(5):
        for i in range(cantidad):
            lista_naves.append(crear_nave_enemiga(30+(i*50),y,30,30))#modificop la posicion para derecha con la i*50
        y = y + 35#modifico la posicion de las naves para abajo con la y +35
    return lista_naves

"""def mover_inicial_nave_enemiga(dic_nave_enemiga,ancho_pantalla):
    #for e_nave in lista_naves_enemigas:
    if dic_nave_enemiga["visible"] == True:
        #dic_nave_enemiga["x"] += dic_nave_enemiga["velocidad"]
        dic_nave_enemiga["rect"].x += dic_nave_enemiga["velocidad"]

        #if dic_nave_enemiga["x"] <= 0 or dic_nave_enemiga["x"] + dic_nave_enemiga["ancho"] >= ancho_pantalla:
        #    dic_nave_enemiga["velocidad"] *= -1
        if dic_nave_enemiga["rect"].x <= 0 or dic_nave_enemiga["rect"].x + dic_nave_enemiga["ancho"] >= ancho_pantalla:
            dic_nave_enemiga["velocidad"] *= -1

        #dic_nave_enemiga["rect"].x = dic_nave_enemiga["x"]"""

def mover_inicial_nave_enemigas(lista_naves_enemigas, ancho_pantalla):
    primera_nave_visible = None
    ultima_nave_visible = None

    for dic_nave_enemiga in lista_naves_enemigas:
        if dic_nave_enemiga["visible"] == True:
            if primera_nave_visible is None or dic_nave_enemiga["rect"].x < primera_nave_visible["rect"].x:
                primera_nave_visible = dic_nave_enemiga
            if ultima_nave_visible is None or dic_nave_enemiga["rect"].x > ultima_nave_visible["rect"].x:
                ultima_nave_visible = dic_nave_enemiga

    if primera_nave_visible is not None and ultima_nave_visible is not None:
        if primera_nave_visible["rect"].x <= 0 or ultima_nave_visible["rect"].x + ultima_nave_visible["ancho"] >= ancho_pantalla:
            for dic_nave_enemiga in lista_naves_enemigas:
                dic_nave_enemiga["velocidad"] *= -1

    for dic_nave_enemiga in lista_naves_enemigas:
        if dic_nave_enemiga["visible"] == True:
            dic_nave_enemiga["rect"].x += dic_nave_enemiga["velocidad"]


def encontrar_nave_enemiga_mas_cercana(lista_naves_enemigas):

    nave_enemiga_mas_cercana = lista_naves_enemigas[0]
    for nave_enemiga in lista_naves_enemigas:
        if nave_enemiga["visible"] == True:
            if nave_enemiga["rect"].y > nave_enemiga_mas_cercana["rect"].y:
                nave_enemiga_mas_cercana = nave_enemiga
    return nave_enemiga_mas_cercana

def crear_lista_naves_mas_cercanas(lista_naves_enemigas,nave_enemiga_mas_cercana):
    lista_naves_enemigas_mas_cercanas = []

    for nave_enemiga in lista_naves_enemigas:
        if nave_enemiga_mas_cercana["rect"].y == nave_enemiga["rect"].y:
            if nave_enemiga not in lista_naves_enemigas_mas_cercanas:
                lista_naves_enemigas_mas_cercanas.append(nave_enemiga)

    return lista_naves_enemigas_mas_cercanas



def actualizar_pantalla_enemigas(lista_naves, pantalla, dic_disparo, score):
    for e_nave in lista_naves:
        if dic_disparo["rect"].colliderect(e_nave["rect"]):
            if e_nave["visible"] == True:
                e_nave["visible"] = False
                score = score + 100
            if dic_disparo["visible"] == True:
                dic_disparo["visible"] == False


        if e_nave["visible"] == True:
            pygame.draw.rect(pantalla, colores.RED1, e_nave["rect"])
            pantalla.blit(e_nave["imagen"], e_nave["rect"])

        """if dic_disparo["visible"] == True:

            dic_disparo["rect"].y -= 0.8
            pantalla.blit(dic_disparo["imagen"],dic_disparo["rect"])"""

    return score