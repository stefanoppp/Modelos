import matplotlib.pyplot as plt
from variables import *
from tp2 import Calentador

calentador1=Calentador(temperatura,masa,tiempo,voltaje)
resistencia = calentador1.calculo_restistencia() 
potencia_resistencia = (voltaje ** 2) / resistencia  
masa_fluido = 1  
calor_especifico_fluido = 4186
ticks_por_segundo = 10 
ticks_totales = tiempo * ticks_por_segundo

def temperatura_con_perdidas(ticks):
    temperatura = temperatura_inicial_fluido
    for _ in range(ticks):
        potencia_efectiva = potencia_resistencia - (temperatura - temperatura_inicial_fluido) * 10
        calor_suministrado = potencia_efectiva / ticks_por_segundo
        calor_absorbido = calor_especifico_fluido * masa_fluido
        delta_temperatura = calor_suministrado / calor_absorbido
        temperatura += delta_temperatura
    return temperatura

def temperatura_sin_perdidas(ticks):
    temperatura = temperatura_inicial_fluido
    for _ in range(ticks):
        calor_suministrado = potencia_resistencia / ticks_por_segundo
        calor_absorbido = calor_especifico_fluido * masa_fluido
        delta_temperatura = calor_suministrado / calor_absorbido
        temperatura += delta_temperatura
    return temperatura

temperaturas_con_perdidas = [temperatura_inicial_fluido]
temperaturas_sin_perdidas = [temperatura_inicial_fluido]

for tick in range(1, ticks_totales + 1):
    temp_con_perdidas = temperatura_con_perdidas(tick)
    temp_sin_perdidas = temperatura_sin_perdidas(tick)
    temperaturas_con_perdidas.append(temp_con_perdidas)
    temperaturas_sin_perdidas.append(temp_sin_perdidas)

# lista de tiempo en segundos para cada tick
tiempo = [i / ticks_por_segundo for i in range(ticks_totales + 1)]

# graficamos
plt.plot(tiempo, temperaturas_con_perdidas, label='Con perdidas')
plt.plot(tiempo, temperaturas_sin_perdidas, label='Sin perdidas')
plt.xlabel('Tiempo')
plt.ylabel('Temperatura del agua')
plt.title('Temperatura del agua en el calentador')
plt.legend()
plt.grid(True)
plt.show()