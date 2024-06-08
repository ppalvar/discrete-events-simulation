import random

def decition_function_id(repair_time: float, repair_cost: float, delivery_wait_time: float, buy_cost: float, current_founds: float):
    return False

def decition_function_dummy(repair_time: float, repair_cost: float, delivery_wait_time: float, buy_cost: float, current_founds: float):
    return random.choice([True, False])

def decition_function_ln(repair_time: float, repair_cost: float, delivery_wait_time: float, buy_cost: float, current_founds: float):
    return repair_time * repair_cost >= delivery_wait_time * buy_cost

def decition_function_sq_time(repair_time: float, repair_cost: float, delivery_wait_time: float, buy_cost: float, current_founds: float):
    return (repair_time ** 2) * repair_cost >= (delivery_wait_time ** 2) * buy_cost

def decition_function_sq_cost(repair_time: float, repair_cost: float, delivery_wait_time: float, buy_cost: float, current_founds: float):
    return repair_time * (repair_cost ** 2) >= delivery_wait_time * (buy_cost ** 2)

def decition_function_sq_all(repair_time: float, repair_cost: float, delivery_wait_time: float, buy_cost: float, current_founds: float):
    return (repair_time ** 2) * (repair_cost ** 2) >= (delivery_wait_time ** 2) * (buy_cost ** 2)