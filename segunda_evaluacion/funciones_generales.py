import pygame
import re
from constantes import *
import json


def generar_json(archivo:str, lista:list):
    with open(archivo, "w") as archivo_json:
        json.dump(lista, archivo_json, indent=3)

def crear_boton(path:str,posicion_y:int,posicion_x:int):
    boton = {}

    boton["imagen"] = pygame.image.load(path)
    boton["imagen"] = pygame.transform.scale(boton["imagen"],(ANCHO_BOTON, ALTO_BOTON))
    boton["rect"] = boton["imagen"].get_rect()
    boton["rect"].y = posicion_y #POS_TOP_BOTON
    boton["rect"].x = posicion_x #POS_LEFT_PUNTOS

    return boton

def blitear_texto_num(posicion_x:int,posicion_y:int,tipo_letra:str,tamaño_letra:int,color,texto_blitear:str,numero_blitear,pantalla):
    font = pygame.font.SysFont(tipo_letra, tamaño_letra)
    texto = font.render(texto_blitear.format(numero_blitear), True, color)
    pantalla.blit(texto,(posicion_x,posicion_y))

def ordenar_asc_desc_lista_dic(lista:list,clave:str):
    swap = True

    while swap == True:
        swap = False
        for i in range(len(lista)-1):
            if lista[i]["score"] < lista[i+1]["score"]:
                auxiliar = lista[i]
                lista[i] = lista[i+1]
                lista[i+i] = auxiliar
                swap = True
            
def parse_puntos(archivo:str)->list:
    
    lista_puntajes_jugadores = []
    try:
        with open(archivo,"r") as archivo:
            lista_puntajes_jugadores = []
            
            todo_texto = archivo.read()
            nombre = re.findall(r'"nombre": "([a-zA-Z0-9]+)', todo_texto)
            puntos = re.findall(r'"score": ([0-9]+)', todo_texto)
            
            for i in range(len(puntos)):
                dic_puntajes = {}
                dic_puntajes["score"] = int(puntos[i])
                try:
                    dic_puntajes["nombre"] = nombre[i]
                except IndexError:
                    pass
                
                lista_puntajes_jugadores.append(dic_puntajes)
                
                
        return lista_puntajes_jugadores  
    except FileNotFoundError:
        return lista_puntajes_jugadores

def generar_json(archivo:str, lista:list):
    with open(archivo, "w") as archivo_json:
        json.dump(lista, archivo_json, indent=3)