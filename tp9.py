import pygame
import random
import math

# Configuración inicial de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulación de Depósito de Partículas')
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Solicitar forma y dimensiones del conducto
conducto_forma = 'circular'  # Ejemplo: circular, cuadrado, rectangular
conducto_dimensiones = [400]  # Ejemplo: diámetro para circular, lado para cuadrado, ancho y alto para rectangular

if conducto_forma == 'circular':
    radio_conducto = conducto_dimensiones[0] // 2
elif conducto_forma == 'cuadrado':
    lado_conducto = conducto_dimensiones[0]
elif conducto_forma == 'rectangular':
    ancho_conducto, alto_conducto = conducto_dimensiones
else:
    print("Forma de conducto no válida")
    exit()

# Establecer dimensiones de las partículas
PARTICLE_MIN_SIZE = 5  # en píxeles
PARTICLE_MAX_SIZE = 10  # en píxeles
PARTICLE_TOLERANCE = 2  # Tolerancia de adherencia en píxeles
STOP_DISTANCE = 300  # Distancia al centro para detener la simulación

# Clase para Partícula
class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def move(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.y -= self.size
        elif direction == 'down':
            self.y += self.size
        elif direction == 'left':
            self.x -= self.size
        elif direction == 'right':
            self.x += self.size

    def is_near_wall(self):
        if conducto_forma == 'circular':
            dist_to_center = math.sqrt((self.x - WIDTH // 2) ** 2 + (self.y - HEIGHT // 2) ** 2)
            return dist_to_center + self.size // 2 >= radio_conducto
        elif conducto_forma == 'cuadrado':
            return (self.x - self.size // 2 <= 0 or self.x + self.size // 2 >= WIDTH or
                    self.y - self.size // 2 <= 0 or self.y + self.size // 2 >= HEIGHT)
        elif conducto_forma == 'rectangular':
            return (self.x - self.size // 2 <= 0 or self.x + self.size // 2 >= WIDTH or
                    self.y - self.size // 2 <= 0 or self.y + self.size // 2 >= HEIGHT)

    def is_near_particle(self, particles):
        for particle in particles:
            dist = math.sqrt((self.x - particle.x) ** 2 + (self.y - particle.y) ** 2)
            if dist <= self.size + PARTICLE_TOLERANCE:
                return True
        return False

# Lista de partículas adheridas
particles = []

# Centro del conducto
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Main loop
running = True
scale_time = 1  # Escala de tiempo
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generar nueva partícula en el centro del conducto
    size = random.randint(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
    new_particle = Particle(center_x, center_y, size)

    while True:
        new_particle.move()

        if new_particle.is_near_wall() or new_particle.is_near_particle(particles):
            particles.append(new_particle)
            break

        # Detener la simulación si las partículas alcanzan una cierta distancia al centro
        dist_to_center = math.sqrt((new_particle.x - center_x) ** 2 + (new_particle.y - center_y) ** 2)
        if dist_to_center >= STOP_DISTANCE:
            running = False
            break

    # Dibujar
    screen.fill(WHITE)

    # Dibujar conducto
    if conducto_forma == 'circular':
        pygame.draw.circle(screen, BLACK, (center_x, center_y), radio_conducto, 2)
    elif conducto_forma == 'cuadrado':
        pygame.draw.rect(screen, BLACK, (center_x - lado_conducto // 2, center_y - lado_conducto // 2, lado_conducto, lado_conducto), 2)
    elif conducto_forma == 'rectangular':
        pygame.draw.rect(screen, BLACK, (center_x - ancho_conducto // 2, center_y - alto_conducto // 2, ancho_conducto, alto_conducto), 2)

    # Dibujar partículas adheridas
    for particle in particles:
        pygame.draw.rect(screen, RED, (particle.x - particle.size // 2, particle.y - particle.size // 2, particle.size, particle.size))

    pygame.display.flip()
    clock.tick(60 * scale_time)

pygame.quit()
