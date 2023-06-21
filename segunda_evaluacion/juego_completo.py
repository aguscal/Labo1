#from constantes import *
#from personaje import Personaje
import pygame 
import colores
import naves_enemigas
from nave_jugador import Nave
import disparos
import random
import json
import re

ANCHO_VENTANA = 500
ALTO_VENTANA = 500
JUGANDO = 0
ANCHO_BOTON = 90
ALTO_BOTON = 40
ANCHO_PUNTOS = 90 
ALTO_PUNTOS = 40
score = 0
vidas = 2

"""def parse_puntos(archivo:str)->list:
    i=0
    with open(archivo, "r")as archivo:
        lista_puntos = []
        todo = archivo.read()
        nombre = re.findall(r'"nombre": "([a-zA-Z0-9]+)', todo)
        tiempo = re.findall(r'"tiempo": ([0-9]+)', todo)
        puntos = re.findall(r'"puntos": ([0-9]+)', todo)

        for i in range(len(nombre)):
            dic_puntajes={}
            dic_puntajes["nombre"]=nombre[i]
            dic_puntajes["tiempo"]= tiempo[i]
            dic_puntajes["puntos"]=puntos[i]
            lista_puntos.append(dic_puntajes)
            i += 1
    return lista_puntos"""

pygame.init()

#CONFIGURACION DEL RELOJ
reloj = pygame.time.Clock()

tiempo_inicial = pygame.time.get_ticks()


#SONIDOS
pygame.mixer.init()
# Crear objetos de sonido para cada archivo de sonido
sonido1 = pygame.mixer.Sound("laser_nave_jugador.wav")
sonido2 = pygame.mixer.Sound("laser_nave_enemiga.wav")
# Configurar los volúmenes de los sonidos (opcional)
sonido1.set_volume(0.5)
sonido2.set_volume(0.8)


#LISTA DE PUNTAJES
puntaje = parse_puntos("data_juego.json")

#PANTALLA
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("GALAXIA")

#RELOJ
reloj = pygame.time.Clock()

#FONDO
imagen_fondo = pygame.image.load("fondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))
rectangulo_fondo = imagen_fondo.get_rect()

#BOTON JUGAR
imagen_jugar = pygame.image.load("imagen_jugar-boton1.png")
imagen_jugar = pygame.transform.scale(imagen_jugar,(ANCHO_BOTON, ALTO_BOTON))
rect_boton = imagen_jugar.get_rect()
rect_boton.y = 250 #POS_TOP_BOTON
rect_boton.x = 10 #POS_LEFT_PUNTOS

#BOTON PUNTAJE
imagen_puntaje = pygame.image.load("imagen_puntajes_boton.jpg")
imagen_puntaje = pygame.transform.scale(imagen_puntaje,(ANCHO_PUNTOS, ALTO_PUNTOS))
rect_boton_puntos = imagen_puntaje.get_rect()
rect_boton_puntos.y = 250#POS_TOP_PUNTOS
rect_boton_puntos.x = 200#POS_LEFT_PUNTOS

#CREO MI NAVE
nave_juego = Nave()

#NAVES ENEMIGAS
lista_naves_enemigas = naves_enemigas.crear_lista_naves_enemigas(9)

#LISTA DISPAROS
lista_disparos = []

#LISTA DISPAROS ENEMIGOS
lista_disparos_enemigos = []

#LISTA DE NAVES ENEMIGAS MAS CERCANAS
lista_enemigas_mas_cercanas = []

flag_correr = True
while flag_correr:

    #TIEMPO TRANSCURRIDO
    tiempo_actual = pygame.time.get_ticks()  # Obtiene el tiempo actual en milisegundos
    tiempo_transcurrido = tiempo_actual - tiempo_inicial

    #LISTA DE EVENTOS
    lista_eventoS = pygame.event.get()
    
    #fondo
    pantalla.blit(imagen_fondo,rectangulo_fondo)

    if JUGANDO == 0:
        pantalla.blit(imagen_jugar, rect_boton)
        pantalla.blit(imagen_puntaje, rect_boton_puntos)
        pygame.display.flip()
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion = evento.pos
                if rect_boton_puntos.collidepoint(posicion):
                    JUGANDO = 2
                    print("CLICK SOBRE los puntos {0}".format(JUGANDO))
                if rect_boton.collidepoint(posicion):
                    JUGANDO = 1
                    print("CLICK SOBRE jugar {0}".format(JUGANDO))
    
    elif JUGANDO == 2:
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                flag_correr = False
        
        for i in range(len(puntaje)):
            font_nombre = pygame.font.SysFont("Arial", 24)
            texto_nombre = font_nombre.render(puntaje[i]["nombre"], True, colores.BLACK)
            pantalla.blit(texto_nombre,(LEFT_TEXTO, TOP_TEXTO+(i*25)))

            font_tiempo= pygame.font.SysFont("Arial", 24)
            texto_tiempo = font_tiempo.render(puntaje[i]["tiempo"], True, colores.BLACK)
            pantalla.blit(texto_tiempo,(LEFT_TEXTO*2, TOP_TEXTO+(i*25)))

            font_puntos = pygame.font.SysFont("Arial", 24)
            texto_puntos = font_puntos.render(puntaje[i]["puntos"], True, colores.BLACK)
            pantalla.blit(texto_puntos,(LEFT_TEXTO*2.5, TOP_TEXTO+(i*25)))

    """elif JUGANDO == 1:
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    personaje1.caminarDerecha("derecha")
                if evento.key == pygame.K_LEFT:
                    personaje1.caminarIzquierda("izquierda")"""

    #    milis = reloj.tick(6) #milis guarda el tiempo que transcurrió desde la última vez que 
        
        
        #llamé a la función reloj.tick
        #actualizo los movimientos de mi personaje
    #    personaje1.actualizar()
        #dibujar mi personaje
    #    personaje1.dibujar(pantalla)

    """    font = pygame.font.SysFont("Arial", 30)
        tiempo = font.render("TIEMPO: {0}".format(SEGUNDOS),True,colores.WHITE)
        pantalla.blit(tiempo,(10,10))
        TIEMPO +=1
        if TIEMPO == 8:
            TIEMPO = 0
            SEGUNDOS -= 1"""

    pygame.display.flip()

pygame.quit

