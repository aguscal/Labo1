import pygame 
import colores
import naves_enemigas
from nave_jugador import Nave
from constantes import *
from funciones_generales import *
import disparos
import random
import json
import re

pygame.init()

#CONFIGURACION DEL RELOJ
reloj = pygame.time.Clock()


#SONIDOS
pygame.mixer.init()
# Crear objetos de sonido para cada archivo de sonido
sonido1 = pygame.mixer.Sound("C:\Labo_1\py_games\segunda_evaluacion\laser_nave_jugador.wav")
sonido2 = pygame.mixer.Sound("C:\Labo_1\py_games\segunda_evaluacion\laser_nave_enemiga.wav")
# Configurar los volúmenes de los sonidos (opcional)
sonido1.set_volume(0.5)
sonido2.set_volume(0.8)


#PANTALLA
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("GALAXIA")

#FONDO
imagen_fondo = pygame.image.load("C:\Labo_1\py_games\segunda_evaluacion\elfondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))
rectangulo_fondo = imagen_fondo.get_rect()

#IMAGEN GALAXIA
imagen_galaxia = pygame.image.load("C:\Labo_1\py_games\segunda_evaluacion\imagen_galaxia.png")
imagen_galaxia = pygame.transform.scale(imagen_galaxia,(400,200))
rectangulo_galaxia = imagen_galaxia.get_rect()
rectangulo_galaxia.x = 50
rectangulo_galaxia.y = 20

#BOTONES
boton_jugar = crear_boton("C:\Labo_1\py_games\segunda_evaluacion\imagen_opcion_jugar.png",350,110)
boton_puntaje = crear_boton("C:\Labo_1\py_games\segunda_evaluacion\imagen_opcion_score.png",350,300)
boton_atras = crear_boton("C:\Labo_1\py_games\segunda_evaluacion\imagen_atras.png",0,0)

#CREO MI NAVE
nave_juego = Nave()

#NAVES ENEMIGAS
lista_naves_enemigas = naves_enemigas.crear_lista_naves_enemigas(9)

#LISTAS
lista_disparos = []
lista_disparos_enemigos = []
lista_enemigas_mas_cercanas = []

#TIEMPO
tiempo_corriente = 0
tiempo_boton_presionado = 0

#INGRESO NOMBRE DE USUARIO
font_nombre = pygame.font.SysFont("Arial",30)
nombre = ""
rect_ingreso_nombre = pygame.Rect(170,400,150,40)
#FALTA DIBUJARLO Y DEMAS

#CREO UNA LISTA EN LA QEU VOY GUARDANDO LOS JUGADORES QEU JUEGAN HASTA QUE EL JUEGO SE CIERRE
lista_jugadores = parse_puntos("puntajes.json")

#FLAG SWAP
swap = True

#FLAGS INGRESO NOMBRE
flag_apreto_jugar = False
bandera_termino_nombre = False


flag_correr = True
while flag_correr:
    tiempo_corriente = pygame.time.get_ticks()

    #LISTA DE EVENTOS
    lista_eventos = pygame.event.get()
    
    #FONDO
    pantalla.blit(imagen_fondo,rectangulo_fondo)

    if JUGANDO == 0:
        pantalla.blit(boton_jugar["imagen"], boton_jugar["rect"])
        pantalla.blit(boton_puntaje["imagen"], boton_puntaje["rect"])
        pantalla.blit(imagen_galaxia,rectangulo_galaxia)
        pygame.display.flip()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False

            #VERIFICA SI HIZO CLICK EN LA POSICION DE ALGUNO DE LOS BOTONES
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion = evento.pos
                if boton_puntaje["rect"].collidepoint(posicion):
                    flag_jugar = False#QUE VUELVA A APRETAR JUGAR SI QUIERE JUGAR
                    JUGANDO = 2
                if boton_jugar["rect"].collidepoint(posicion):
                    flag_apreto_jugar = True
                       
            #ACA SE ESCRIBE EL NOMBRE
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[0:-1]
                else:
                    nombre += evento.unicode
                
                #FIJARSE SI TERMINO DE ESCRIBIR
                if evento.key == pygame.K_RETURN and len(nombre) > 3:
                    bandera_termino_nombre = True
            
            #FIJARSE SI TERMINO DE ESCRIBIR Y APRETO JUGAR , COMIENZA EL JUEGO
            if flag_apreto_jugar == True and bandera_termino_nombre == True:
                nombre = nombre.strip()
                vidas = 2
                score = 0
                flag_jugar = False
                bandera_termino_nombre = False
                tiempo_boton_presionado = pygame.time.get_ticks()
                JUGANDO = 1

        #ESTO ES PARA LA CAJA EN DONDE VA EL NOMBRE
        pygame.draw.rect(pantalla,colores.ALICEBLUE,rect_ingreso_nombre,2)
        font_nombre_surface = font_nombre.render(nombre,True,colores.RED1)
        pantalla.blit(font_nombre_surface,(rect_ingreso_nombre.x+5,rect_ingreso_nombre.y+5))

    
    elif JUGANDO == 2:
        # RECORRER EL JSON Y ORDENAR LOS JUGADORES , LUEGO MOSTRARLOS!!!!
        
        pantalla.blit(boton_atras["imagen"], boton_atras["rect"])

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion = evento.pos
                if boton_atras["rect"].collidepoint(posicion):
                    JUGANDO = 0

        #ORDENA LA LISTA DE MANERA DESCENDENTE
        for i in range(len(lista_jugadores)-1):
            for j in range(i+1, len(lista_jugadores)):
                if lista_jugadores[i]["score"] < lista_jugadores[j]["score"]:
                    auxiliar = lista_jugadores[i]
                    lista_jugadores[i] = lista_jugadores[j]
                    lista_jugadores[j] = auxiliar

        #IMPRIME EN PANTALLA EL RANKING DE POSICIONES
        for i in range(len(lista_jugadores)):
           
            font_nombre = pygame.font.SysFont("Arial", 24)
            texto_nombre = font_nombre.render("NOMBRE : {0}".format(lista_jugadores[i]["nombre"]), True, colores.YELLOW1)
            pantalla.blit(texto_nombre,(50, 100+(i*25)))

            font_puntos = pygame.font.SysFont("Arial", 24)
            texto_puntos = font_puntos.render("SCORE : {0}".format(lista_jugadores[i]["score"]), True, colores.YELLOW1)
            pantalla.blit(texto_puntos,(50*6, 100+(i*25)))
        
    elif JUGANDO == 1:
        
        #MIENTRAS SE CUMPLA ESTE IF TRANSCURRE LA PARTIDA 
        if vidas >= 0 and tiempo_transcurrido <= 20000:

            segundos = int(tiempo_transcurrido / 1000)

            for evento in lista_eventos:
                if evento.type == pygame.QUIT:
                    flag_correr = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_x:
                        sonido1.play()
                        
                        disparo = disparos.crear_disparo(nave_juego.rect.x,nave_juego.rect.y)
                        lista_disparos.append(disparo)
                        
            #MOVIMIENTO DE LA NAVE JUGADOR
            nave_juego.manejar_evento_teclado(ANCHO_VENTANA,2)

            #BLIT IMAGEN DE FONDO
            pantalla.blit(imagen_fondo,rectangulo_fondo)

            #BLITEAR TEXTO VIDAS
            blitear_texto_num(300,10,"Arial",20,colores.ROYALBLUE,"VIDAS: {0}",vidas,pantalla)
            
            #BLITEAR TEXTO TIEMPO
            blitear_texto_num(140,10,"Arial",20,colores.GREENYELLOW,"TIEMPO: {0}/20",segundos,pantalla)

            #BLITEAR TEXTO SCORE
            blitear_texto_num(10,10,"Arial",20,colores.YELLOW1,"SCORE: {0}",score,pantalla)

            #BLIT NAVE JUGADOR
            pantalla.blit(nave_juego.imagen,nave_juego.rect)

            lista_disparos_eliminar = []
            lista_naves_eliminar = []
            lista_disparos_enemigos_eliminar = []
            

            #MOVIMIENTO DE LAS NAVES ENEMIGAS
            naves_enemigas.mover_inicial_nave_enemigas(lista_naves_enemigas,ANCHO_VENTANA)
            
            
            #if segundos > 2:
                    
            if len(lista_naves_enemigas) > 0:
                #ENCONTRAR LA NAVE MAS CERCANA
                nave_enemiga_mas_cercana = naves_enemigas.encontrar_nave_enemiga_mas_cercana(lista_naves_enemigas)
                
                #OBTENER LISTA NAVES MAS CERCANAS
                lista_enemigas_mas_cercanas = naves_enemigas.crear_lista_naves_mas_cercanas(lista_naves_enemigas,nave_enemiga_mas_cercana)
                
                #SI HAY UNA NAVE ELIMINADA Y HAY MAS DE 44 INCLUSIVE
                if len(lista_naves_enemigas) <= 49 and len(lista_naves_enemigas) >= 44:
                    probabilidad_disparo = 0.003
                    
                    if len(lista_enemigas_mas_cercanas) > 0 and random.random() < probabilidad_disparo:
                        nave_random = random.choice(lista_enemigas_mas_cercanas)#SOBRE LAS NAVES MAS CERCANAS 
                        
                        disparo_enemigo = disparos.crear_disparo_enemigo(nave_random["rect"].x, nave_random["rect"].y)
                        sonido2.play()
                        if disparo_enemigo not in lista_disparos_enemigos:
                            lista_disparos_enemigos.append(disparo_enemigo)


                #SI QUEDAN MENOS DE 44 NAVES Y MAS DE 24 INCLUSIVE
                if len(lista_naves_enemigas) < 44 and len(lista_naves_enemigas) >= 24 :
                    probabilidad_disparo = 0.005
                    
                    if len(lista_enemigas_mas_cercanas) > 0 and random.random() < probabilidad_disparo:
                        nave_random = random.choice(lista_enemigas_mas_cercanas)#SOBRE LAS NAVES MAS CERCANAS 
                        
                        disparo_enemigo = disparos.crear_disparo_enemigo(nave_random["rect"].x, nave_random["rect"].y)
                        sonido2.play()
                        if disparo_enemigo not in lista_disparos_enemigos:
                            lista_disparos_enemigos.append(disparo_enemigo)
                        
                #SI QEUDAN MENOS DE 24 NAVES 
                if len(lista_naves_enemigas) < 24:
                    probabilidad_disparo = 0.006
                    
                    if random.random() < probabilidad_disparo:
                        nave_random = random.choice(lista_naves_enemigas)#SOBRE EL TOTAL DE NAVES
                        
                        disparo_enemigo = disparos.crear_disparo_enemigo(nave_random["rect"].x, nave_random["rect"].y)
                        sonido2.play()
                        if disparo_enemigo not in lista_disparos_enemigos:
                            lista_disparos_enemigos.append(disparo_enemigo)               
            elif len(lista_naves_enemigas) ==  0:
                lista_naves_enemigas = naves_enemigas.crear_lista_naves_enemigas(9)

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
                
                if disparo_enemigo["rect"].y > ALTO_VENTANA:
                    lista_disparos_enemigos_eliminar.append(disparo_enemigo)



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
                        if disparo not in lista_disparos_eliminar:
                            lista_disparos_eliminar.append(disparo)
                        if nave_enemiga not in lista_naves_eliminar:
                            lista_naves_eliminar.append(nave_enemiga)
                        score += 100
                if disparo["rect"].y < 0:
                    lista_disparos_eliminar.append(disparo)                    

            #ELIMINAR COLISIONADOS
            for disparo_eliminar in lista_disparos_eliminar:
                lista_disparos.remove(disparo_eliminar)
            
            for nave_eliminar in lista_naves_eliminar:
                lista_naves_enemigas.remove(nave_eliminar)

            for disparo_enemigo_eliminar in lista_disparos_enemigos_eliminar:
                lista_disparos_enemigos.remove(disparo_enemigo_eliminar)
                

            reloj.tick(120) # maneja la velocidad de actualizacion  del juego y de la nave

            pygame.display.flip()
        else:
            #ACTUALIZAR EL JSON Y AGREGARLE EL NUEVO JUGADOR
            data = {}
            data["jugadores"] = lista_jugadores
            data["jugadores"].append({"score": score,"nombre": nombre})

            generar_json("puntajes.json", data)

            lista_disparos.clear()
            lista_disparos_enemigos.clear()
            lista_naves_enemigas.clear()
            nombre = ""
            
            JUGANDO = 0
    
    #print(tiempo_corriente,tiempo_boton_presionado)
    tiempo_transcurrido = tiempo_corriente - tiempo_boton_presionado
    pygame.display.flip()

pygame.quit()