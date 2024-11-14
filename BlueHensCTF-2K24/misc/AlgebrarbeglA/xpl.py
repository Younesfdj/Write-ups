#! ./venv/bin/python3

import math
from sympy import * 


def calculate_k():
    factorial_78 = math.factorial(78)
    subfactorial_87 = subfactorial(87)
    
    k = (factorial_78 + subfactorial_87) // 2
    return k

k_value = calculate_k()
print(f"udctf{{{k_value}}}")