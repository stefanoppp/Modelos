import pygame
import random
import math

# Configuración inicial de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulación de Sistema de Atención al Público')
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Parámetros del sistema
NUM_BOXES = 5  # Puede ser de 1 a 10
BOX_COST = 1000
CUSTOMER_LOSS_COST = 10000
OPEN_HOURS = 4  # De 8 a 12 horas
SECONDS_PER_HOUR = 3600
TOTAL_SECONDS = OPEN_HOURS * SECONDS_PER_HOUR
ARRIVAL_PROBABILITY = 1 / 144
SERVICE_TIME_MEAN = 10 * 60  # 10 minutos en segundos
SERVICE_TIME_STD_DEV = 5 * 60  # 5 minutos en segundos
CLOSE_TIME = 12 * SECONDS_PER_HOUR

# Variables de simulación
customers = []
boxes = [None] * NUM_BOXES
waiting_queue = []
served_customers = 0
unserved_customers = 0
total_customers = 0
current_time = 0
service_times = []
waiting_times = []

# Función para generar tiempo de atención
def generate_service_time():
    return max(1, int(random.gauss(SERVICE_TIME_MEAN, SERVICE_TIME_STD_DEV)))

# Cliente
class Customer:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_end_time = None

    def start_service(self, start_time):
        self.service_start_time = start_time
        self.service_end_time = start_time + generate_service_time()
        service_times.append(self.service_end_time - self.service_start_time)

    def is_being_served(self, current_time):
        return self.service_start_time is not None and self.service_start_time <= current_time < self.service_end_time

    def is_served(self, current_time):
        return self.service_end_time is not None and current_time >= self.service_end_time

# Main loop
running = True
while running and current_time <= TOTAL_SECONDS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generar nuevos clientes
    if random.random() < ARRIVAL_PROBABILITY:
        customers.append(Customer(current_time))
        total_customers += 1

    # Asignar clientes a boxes libres
    for i in range(NUM_BOXES):
        if boxes[i] is None and waiting_queue:
            customer = waiting_queue.pop(0)
            customer.start_service(current_time)
            boxes[i] = customer
            waiting_times.append(current_time - customer.arrival_time)

    # Procesar clientes en boxes
    for i in range(NUM_BOXES):
        if boxes[i] is not None:
            if boxes[i].is_served(current_time):
                boxes[i] = None
                served_customers += 1

    # Mover clientes a la cola
    for customer in customers:
        if not customer.is_being_served(current_time):
            if current_time - customer.arrival_time >= 30 * 60:
                unserved_customers += 1
                customers.remove(customer)
            elif customer not in waiting_queue and customer.service_start_time is None:
                waiting_queue.append(customer)

    # Dibujar
    screen.fill(WHITE)
    # Dibujar boxes
    for i in range(NUM_BOXES):
        color = GREEN if boxes[i] is None else RED
        pygame.draw.rect(screen, color, (50 + i * 70, 50, 60, 60))

    # Dibujar clientes en la cola
    for i, customer in enumerate(waiting_queue):
        pygame.draw.circle(screen, BLUE, (100, 150 + i * 30), 10)

    pygame.display.flip()
    clock.tick(60)
    current_time += 1

pygame.quit()

# Calcular estadísticas
if service_times:
    min_service_time = min(service_times)
    max_service_time = max(service_times)
else:
    min_service_time = max_service_time = 0

if waiting_times:
    min_waiting_time = min(waiting_times)
    max_waiting_time = max(waiting_times)
else:
    min_waiting_time = max_waiting_time = 0

# Resultados
print(f'Total de clientes: {total_customers}')
print(f'Clientes atendidos: {served_customers}')
print(f'Clientes no atendidos: {unserved_customers}')
print(f'Tiempo mínimo de atención en box: {min_service_time / 60:.2f} minutos')
print(f'Tiempo máximo de atención en box: {max_service_time / 60:.2f} minutos')
print(f'Tiempo mínimo de espera en salón: {min_waiting_time / 60:.2f} minutos')
print(f'Tiempo máximo de espera en salón: {max_waiting_time / 60:.2f} minutos')
print(f'Costo de operación: {NUM_BOXES * BOX_COST + unserved_customers * CUSTOMER_LOSS_COST}')
