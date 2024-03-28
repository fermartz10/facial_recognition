import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir las dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong")

# Definir las variables del juego
jugador1_puntos = 0
jugador2_puntos = 0

# Definir las coordenadas y velocidades de la pelota
pelota_x = ANCHO // 2
pelota_y = ALTO // 2
pelota_vel_x = 5 * random.choice((1, -1))
pelota_vel_y = 5 * random.choice((1, -1))

# Definir las coordenadas y dimensiones de los jugadores
jugador1_x = 50
jugador1_y = ALTO // 2 - 50
jugador2_x = ANCHO - 50
jugador2_y = ALTO // 2 - 50
jugador_alto = 100
jugador_ancho = 10

# Definir la velocidad de los jugadores
jugador_vel = 5

# Definir la función para dibujar los jugadores
def dibujar_jugadores():
    pygame.draw.rect(pantalla, BLANCO, (jugador1_x, jugador1_y, jugador_ancho, jugador_alto))
    pygame.draw.rect(pantalla, BLANCO, (jugador2_x, jugador2_y, jugador_ancho, jugador_alto))

# Definir la función para dibujar la pelota
def dibujar_pelota():
    pygame.draw.circle(pantalla, BLANCO, (pelota_x, pelota_y), 10)

# Definir la función para reiniciar la pelota
def reiniciar_pelota():
    global pelota_x, pelota_y, pelota_vel_x, pelota_vel_y
    pelota_x = ANCHO // 2
    pelota_y = ALTO // 2
    pelota_vel_x = 2 * random.choice((1, -1))
    pelota_vel_y = 2 * random.choice((1, -1))

# Definir la función principal del juego
def main():
    global jugador1_y, jugador2_y, jugador1_puntos, jugador2_puntos, pelota_x, pelota_y, pelota_vel_x, pelota_vel_y

    # Reiniciar la posición y velocidad de la pelota
    reiniciar_pelota()

    # Bucle del juego
    while True:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Manejar la entrada del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            jugador1_y -= jugador_vel
        if keys[pygame.K_s]:
            jugador1_y += jugador_vel
        if keys[pygame.K_UP]:
            jugador2_y -= jugador_vel
        if keys[pygame.K_DOWN]:
            jugador2_y += jugador_vel

        # Actualizar la posición de la pelota
        pelota_x += pelota_vel_x
        pelota_y += pelota_vel_y

        # Colisiones con los bordes de la pantalla
        if pelota_y <= 0 or pelota_y >= ALTO:
            pelota_vel_y *= -1
        if pelota_x <= 0:
            jugador2_puntos += 1
            reiniciar_pelota()
        if pelota_x >= ANCHO:
            jugador1_puntos += 1
            reiniciar_pelota()

        # Colisiones con los jugadores
        if (pelota_x <= jugador1_x + jugador_ancho and
            pelota_y >= jugador1_y and
            pelota_y <= jugador1_y + jugador_alto):
            pelota_vel_x *= -1
        if (pelota_x >= jugador2_x - jugador_ancho and
            pelota_y >= jugador2_y and
            pelota_y <= jugador2_y + jugador_alto):
            pelota_vel_x *= -1

        # Limpiar la pantalla
        pantalla.fill(NEGRO)

        # Dibujar los jugadores y la pelota
        dibujar_jugadores()
        dibujar_pelota()

        # Mostrar los puntos en la pantalla
        font = pygame.font.Font(None, 36)
        puntos_texto = font.render(f"{jugador1_puntos} - {jugador2_puntos}", True, BLANCO)
        pantalla.blit(puntos_texto, (ANCHO // 2 - puntos_texto.get_width() // 2, 10))

        # Actualizar la pantalla
        pygame.display.flip()

# Ejecutar el juego
if __name__ == "__main__":
    main()
