#En este programa se dará un vistazo a la forma canónica de un vector en R^2 
#Se dará una alternativa con diferentes bases para R^2 y se escribirá un vector en terminos de esta
#A su ves se verá como una transformación (rotación) puede visualizarse resursivamente
#Es muy ineficiente, pero es bonito el resultado :´)
import pygame 
import numpy as np
from math import sin, cos

pygame.init()

#Cantidad de puntos para las lineas paralelas
npuntos = 50
#Tamaño de la ventana
width, height = 560, 560
#Ángulo
delta = 0
#Nuevas bases
#voy a intentar una mamadota a ver si sale, nota: ponerlo en el bucle
background = (30, 30, 30)
screen = pygame.display.set_mode((width, height))
run = True
while run:
    mousex, mousey = pygame.mouse.get_pos()
    #print(mousex, mousey)
    b1 = [-3, 2]
    b2 = [2, 2]
    q, w, e = pygame.mouse.get_pressed()
    if q == True:
        
        b1 = [-7+mousex//40, 7-mousey//40]
    elif e == True:
        b2 = [-7+mousex//40, 7-mousey//40]
    print("b1", b1)
    #b1 = [-3, -1]
    
    #Matriz para la combinación lineal con las nuevas bases
    Mb = np.transpose([b1, b2])
    #Inversa de Mb####AQUI HAY UN ERROR QUE OCUPA UN IF ELSE PARA QUE EN CASO DE detMb=0 la matriz se pueda invertir de distinta manera o regresando al estado base

    Mb_inversa = np.linalg.inv(Mb)
    #Matriz traslación, si se quiere agrandar o encoger, solo cambie zoom 
    def traslada(point):
        zoom = 40
        Tls = np.array([[zoom, 0, width/2], [0, -zoom, height/2], [0, 0, 1]])
        v = np.array([point[0], point[1], 1])
        v_tls = Tls @ v
        point = [v_tls[0], v_tls[1]]
        return point
    #Vector que se quiera escribir en la nueva base b1, b2 
    v_b = (1, 1)
    #Mismo vector, en base canónica
    v = Mb @ v_b
    #Texto en la pantalla
    texto_v = (f"[v]_b = {str(v_b)} ")
    #print(texto_v)

    #Puntos para las lineas del plano en base canónica
    pb_up = []
    pb_dwn = []
    pb_izq = []
    pb_der = []
    for i in range(npuntos):
        xcor_up = -npuntos // 2 + i
        ycor_up = height
        pb_up.append([xcor_up, ycor_up])

        xcor_dwn = -npuntos // 2 + i
        ycor_dwn = -height
        pb_dwn.append([xcor_dwn, ycor_dwn])

        xcor_izq = -width
        ycor_izq = -npuntos // 2 + i
        pb_izq.append([xcor_izq, ycor_izq])

        xcor_der = width
        ycor_der = -npuntos // 2 + i
        pb_der.append([xcor_der, ycor_der])

    #Puntos para las lineas del plano en la nueva base
    pr_up = []
    pr_dwn = []
    pr_izq = []
    pr_der = []
    for i in range(npuntos):
        pr_up.append(Mb @ pb_up[i])
        pr_dwn.append(Mb @ pb_dwn[i])
        pr_izq.append(Mb @ pb_izq[i])
        pr_der.append(Mb @ pb_der[i])

    #Inicio de la pantalla con pygame

    clock = pygame.time.Clock()
    
    #Configuración del texto
    font = pygame.font.Font(None, 20)
    texto_superficie = font.render(texto_v, True, (255, 255, 255))

#Dibujo

    fps = 2004
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill(background)

    
    #Lineas de base canónica
    for i in range(npuntos):
        pygame.draw.line(screen, (45, 35, 55), traslada(pb_up[i]), traslada(pb_dwn[i]), 3)
        pygame.draw.line(screen, (45, 35, 55), traslada(pb_izq[i]), traslada(pb_der[i]), 3)
    #Lineas centrales canónicas
    pygame.draw.line(screen, (185, 185, 185), [0, 0.5*height], [width, 0.5*height], 2)
    pygame.draw.line(screen, (185, 185, 185), [0.5*width, 0], [0.5*width, height], 2)
    #Lineas de la base b1, b2
    for i in range(npuntos):
        pygame.draw.line(screen, (205, 105, 255), traslada(pr_up[i]), traslada(pr_dwn[i]), 3)
        pygame.draw.line(screen, (205, 105, 255), traslada(pr_izq[i]), traslada(pr_der[i]), 3)
    #Lineas centrales del nuevo plano
    pygame.draw.line(screen, (225, 225, 225), traslada(pr_up[npuntos//2]), traslada(pr_dwn[npuntos//2]), 3)
    pygame.draw.line(screen, (225, 225, 225), traslada(pr_izq[npuntos//2]), traslada(pr_der[npuntos//2]), 3)
    #Base b1 (Rojo)
    pygame.draw.line(screen, (255, 30, 39), traslada((0, 0)), traslada(b1), 3)
    pygame.draw.circle(screen, (255, 30, 39), traslada(b1), 3, 2)
    #Base b2 (Azul)
    pygame.draw.line(screen, (53, 242, 255), traslada((0, 0)), traslada(b2), 3)
    pygame.draw.circle(screen, (53, 242, 255), traslada(b2), 3, 2)
    #Vector V 
    pygame.draw.line(screen, (255, 249, 0), traslada((0, 0)), traslada(v), 3)
    pygame.draw.circle(screen, (255, 249, 0), traslada(v), 4, 2)
    screen.blit(texto_superficie, traslada(v))
    #Rotación!!! en este mismo programa, se pueden aplicar una transformaciones recursivamente
    #en este caso lo roto indefinidamente en el tiempo
    delta += 0.1
    Mrotar = [[cos(delta), -sin(delta)], [sin(delta), cos(delta)]]
    vr = Mrotar @ v
    #pygame.draw.circle(screen, (255, 249, 0), traslada(vr), 4, 2)
    #pygame.draw.line(screen, (255, 249, 0), traslada((0, 0)), traslada(vr), 3)

    pygame.display.update()

pygame.quit()









