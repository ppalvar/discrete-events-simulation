import numpy as np

def profit_function_id(time: float) -> float:
    return time

def profit_function_ln(time: float) -> float:
    return 10 * time

def profit_function_sn_lg(time: float) -> float:
    return time - np.cos(time)

def profit_function_sn_sm(time: float) -> float:
    return (.33 * time) - (np.cos(time) / 3)