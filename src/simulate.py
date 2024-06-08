import numpy as np

from queue import Queue as queue
from queue import PriorityQueue as p_queue

BANKRUPT = 'BANKRUPT'
BREAKDOWN = 'BREAKDOWN'
TIMEOUT = 'TIMEOUT'

def simulate(machines: int,
             spares: int, 
             founds: float, 
             buy_cost: float, 
             delivery_wait_time: float, 
             profit_function, 
             decition_function,
             event_distribution,
             repair_time_distribution,
             repair_cost_distribution,
             max_steps = 1000000,
             sjf = False) -> tuple[float, float]:
    global_time = 0
    steps = 0
    current_repair_time = np.inf
    current_delivery_time = np.inf
    broken_machines = 0
    events = p_queue()
    repair_times = queue() if not sjf else p_queue()
    delivery_times = queue()
    
    spent_repair_founds = 0
    spent_buy_founds = 0
    repaired_machines = 0
    total_repair_time = 0
    bought_machines = 0

    _events = [event_distribution() for _ in range(machines)] # np.random.exponential(np.e, machines)

    for ev in _events:
        events.put(-ev)
    
    while True:
        event_time = -events.get()
    
        # Devolver al servicio las maquinas reparadas
        while current_repair_time <= event_time and not repair_times.empty():
            current_repair_time, _current_repair_cost = repair_times.get()
            total_repair_time += current_repair_time
            current_repair_time += global_time
            spent_repair_founds += _current_repair_cost # El costo de arreglar una maquina se paga cuando se empieza la reparacion
            
            broken_machines -= 1
            repaired_machines += 1
        
        # Poner en servicio las maquinas que se compraron
        while current_delivery_time <= event_time and not delivery_times.empty():
            current_delivery_time = delivery_times.get()
            broken_machines -= 1
            
        # Actualizar el tiempo trancurrido y las
        global_time = event_time
        broken_machines += 1

        # Generar el tiempo de reparacion y el costo de reparacion
        new_repair_time = repair_time_distribution()
        new_repair_cost = repair_cost_distribution()


        # Calcular los fondos que se disponen en este momento
        current_founds = founds + profit_function(global_time) - (spent_repair_founds + spent_buy_founds)

        # Si los fondos son <= 0 la fabrica esta en bancarrota y se termina la simulacion
        if current_founds <= 0:
            average_repair_time = total_repair_time / repaired_machines if repaired_machines != 0 else 0
            return {'time': global_time,
                    'founds': current_founds, 
                    'repaired_machines': repaired_machines, 
                    'bought_machines': bought_machines, 
                    'average_repair_time': average_repair_time, 
                    'spent_repair_funds': spent_repair_founds,
                    'spent_buy_funds': spent_buy_founds,
                    'stop_reason': BANKRUPT}

        #Decidir si se desecha o se repara la maquina
        if decition_function(new_repair_time, new_repair_cost, delivery_wait_time, buy_cost, current_founds):
            spent_buy_founds += buy_cost
            delivery_times.put(delivery_wait_time + global_time)
            bought_machines += 1
        else:
            repair_times.put((new_repair_time, new_repair_cost))

        if broken_machines > spares:
            average_repair_time = total_repair_time / repaired_machines if repaired_machines != 0 else 0
            return {'time': global_time,
                    'founds': current_founds, 
                    'repaired_machines': repaired_machines, 
                    'bought_machines': bought_machines, 
                    'average_repair_time': average_repair_time, 
                    'spent_repair_funds': spent_repair_founds,
                    'spent_buy_funds': spent_buy_founds,
                    'stop_reason': BREAKDOWN}
        else:
            used_spare_lifetime = event_distribution() + global_time # np.random.exponential(np.e) + global_time
            events.put(-used_spare_lifetime)
        
        if current_repair_time is np.inf and not repair_times.empty():
            current_repair_time, _current_repair_cost = repair_times.get()
            current_repair_time +=  global_time
            spent_repair_founds += _current_repair_cost

        if current_delivery_time is np.inf and not delivery_times.empty():
            current_delivery_time = delivery_times.get() + global_time
        
        steps += 1
        if steps >= max_steps:
            average_repair_time = total_repair_time / repaired_machines if repaired_machines != 0 else 0
            return {'time': global_time,
                    'founds': current_founds, 
                    'repaired_machines': repaired_machines, 
                    'bought_machines': bought_machines, 
                    'average_repair_time': average_repair_time, 
                    'spent_repair_funds': spent_repair_founds,
                    'spent_buy_funds': spent_buy_founds,
                    'stop_reason': TIMEOUT}