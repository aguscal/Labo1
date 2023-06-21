import pygame 
import colores
import naves_enemigas
from nave_jugador import Nave
import disparos
import random


ANCHO_VENTANA = 500
ALTO_VENTANA = 500
score = 0
vidas = 2

pygame.init()#inicio pygame

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


pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))#medida en pixeles 500 * 400 pixels, recibe una tupla

#RELOJ
reloj = pygame.time.Clock()

imagen_fondo = pygame.image.load("fondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))
rectangulo_fondo = imagen_fondo.get_rect()

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

run = True
while run :
    tiempo_actual = pygame.time.get_ticks()  # Obtiene el tiempo actual en milisegundos
    tiempo_transcurrido = tiempo_actual - tiempo_inicial

    for event in pygame.event.get():
        if event.type == pygame.QUIT:#ME FIJO SI EL TIPO DE EVENTO ES IGUAL A QUIT
            #CIERRO LA VENTANA
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                sonido1.play()
                
                disparo = disparos.crear_disparo(nave_juego.rect.x,nave_juego.rect.y)
                lista_disparos.append(disparo)
                
    
    nave_juego.manejar_evento_teclado(ANCHO_VENTANA,2)

    pantalla.blit(imagen_fondo,rectangulo_fondo)

    font = pygame.font.SysFont("Arial", 20)
    texto_vidas = font.render("VIDAS: {0}".format(vidas), True, colores.ROYALBLUE)
    pantalla.blit(texto_vidas,(300,10))
    
    segundos = int(tiempo_transcurrido / 1000)

    font = pygame.font.SysFont("Arial", 20)
    texto_segundos = font.render("TIEMPO: {0}/40".format(segundos), True, colores.GREENYELLOW)
    pantalla.blit(texto_segundos,(140,10))
   

    font = pygame.font.SysFont("Arial", 20)
    texto_score = font.render("SCORE: {0}".format(score), True, colores.YELLOW1)
    pantalla.blit(texto_score,(10,10))

    pantalla.blit(nave_juego.imagen,nave_juego.rect)

    lista_disparos_eliminar = []#PORQUE ACA?
    lista_naves_eliminar = []
    lista_disparos_enemigos_eliminar = []
    
    #OTRO TIPO DE MOVIMIENTO
    """for nave_enemiga in lista_naves_enemigas:
        if nave_enemiga["visible"] == True:
            naves_enemigas.mover_inicial_nave_enemiga(nave_enemiga,ANCHO_VENTANA)
            pantalla.blit(nave_enemiga["imagen"],nave_enemiga["rect"])"""

    naves_enemigas.mover_inicial_nave_enemigas(lista_naves_enemigas,ANCHO_VENTANA)
    
    if tiempo_transcurrido > 5000:
            
        #ENCONTRAR LA NAVE MAS CERCANA
        if len(lista_naves_enemigas) > 0:
            nave_enemiga_mas_cercana = naves_enemigas.encontrar_nave_enemiga_mas_cercana(lista_naves_enemigas)
            
            #OBTENER LISTA NAVES MAS CERCANAS
            lista_enemigas_mas_cercanas = naves_enemigas.crear_lista_naves_mas_cercanas(lista_naves_enemigas,nave_enemiga_mas_cercana)
            

            #SI QUEDAN 24 NAVES O MENOS Y HAY AL MENOS UNA
            if len(lista_naves_enemigas) <= 42 and len(lista_naves_enemigas) > 24 :
                #REALIZAR LA ACCION AL HABER -24 NAVES
                probabilidad_disparo = 0.005
                
                if len(lista_enemigas_mas_cercanas) > 0 and random.random() < probabilidad_disparo:
                    nave_random = random.choice(lista_enemigas_mas_cercanas)#SOBRE LAS NAVES MAS CERCANAS 
                    
                    disparo_enemigo = disparos.crear_disparo_enemigo(nave_random["rect"].x, nave_random["rect"].y)
                    sonido2.play()
                    if disparo_enemigo not in lista_disparos_enemigos:
                        lista_disparos_enemigos.append(disparo_enemigo)
                    
            
            if len(lista_naves_enemigas) <= 24:
                #REALIZAR LA ACCION AL HABER -24 NAVES
                probabilidad_disparo = 0.006
                
                #if len(lista_enemigas_mas_cercanas) > 0 and random.random() < probabilidad_disparo:
                if random.random() < probabilidad_disparo:
                    nave_random = random.choice(lista_naves_enemigas)#SOBRE EL TOTAL DE NAVES
                    
                    disparo_enemigo = disparos.crear_disparo_enemigo(nave_random["rect"].x, nave_random["rect"].y)
                    sonido2.play()
                    if disparo_enemigo not in lista_disparos_enemigos:
                        lista_disparos_enemigos.append(disparo_enemigo)
                    

    #BLITEAR LAS NAVES ENEMIGAS
    for nave_enemiga in lista_naves_enemigas:
        if nave_enemiga["visible"] == True:
            pantalla.blit(nave_enemiga["imagen"],nave_enemiga["rect"])

    #COLISION DISPARO ENEMIGO CON NAVE JUGADOR Y BLITEO DE DISPARO ENEMIGO
    for disparo_enemigo in lista_disparos_enemigos:

        if disparo_enemigo["visible"] == True:
            disparo_enemigo["rect"].y += 3
            
            pantalla.blit(disparo_enemigo["imagen"],disparo_enemigo["rect"])
        
        if disparo_enemigo["rect"].colliderect(nave_juego.rect):
            disparo_enemigo["visible"] = False
            if disparo_enemigo not in lista_disparos_enemigos_eliminar:
                lista_disparos_enemigos_eliminar.append(disparo_enemigo)
            vidas -= 1



    #COLISION DISPARO JUGADOR CON NAVES ENEMIGAS Y BLITEAR DISPARO JUGADOS
    for disparo in lista_disparos:

        if disparo["visible"] == True:

            disparo["rect"].y -= 5
            
            pantalla.blit(disparo["imagen"],disparo["rect"])

        #score = naves_enemigas.actualizar_pantalla_enemigas(lista_naves_enemigas,pantalla,disparo,score)
        for nave_enemiga in lista_naves_enemigas:
            if nave_enemiga["visible"] and disparo["rect"].colliderect(nave_enemiga["rect"]):
                nave_enemiga["visible"] = False
                disparo["visible"] = False
                #if disparo["visible"] == False and disparo in lista_disparos:
                #    lista_disparos.remove(disparo)
                if disparo not in lista_disparos_eliminar:
                    lista_disparos_eliminar.append(disparo)
                if nave_enemiga not in lista_naves_eliminar:
                    lista_naves_eliminar.append(nave_enemiga)
                score += 100

    #ELIMINAR COLISIONADOS
    for disparo_eliminar in lista_disparos_eliminar:
        lista_disparos.remove(disparo_eliminar)
    
    for nave_eliminar in lista_naves_eliminar:
        lista_naves_enemigas.remove(nave_eliminar)

    for disparo_enemigo_eliminar in lista_disparos_enemigos_eliminar:
        lista_disparos_enemigos.remove(disparo_enemigo_eliminar)
        

    pygame.display.flip()#actualizo la pantalla(lo que se muestra)
    reloj.tick(120) # maneja la velocidad de actualizacion  del juego y de la nave
pygame.quit()