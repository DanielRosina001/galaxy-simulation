import random
from math import floor

def even_div(n: int, d: int) -> list[int]: 
    if d <= 0 or n <= 0: 
        raise ValueError('d and n must be positive integers')
    if d > n: 
        raise ValueError('d must be less than n')
    
    q = n // d
    r = n % d
    ls = [q for _ in range(d)]

    for i in range(r): 
        ls[i] += 1

    return ls

def proportional_div(n: int, proportions: list[float]) -> list[int]:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if any(p < 0 for p in proportions):
        raise ValueError("proportions must be non-negative")
    if abs(sum(proportions) - 1) > 1e-5:
        raise ValueError("sum of proportions must be 1")

    raw = [p * n for p in proportions]

    result = [int(x) for x in raw]
    diff = n - sum(result)

    fractional_parts = [(i, raw[i] - result[i]) for i in range(len(proportions))]
    fractional_parts.sort(key=lambda x: x[1], reverse=True)

    for i in range(diff):
        result[fractional_parts[i][0]] += 1

    return result

def uneven_div(n: int, d: int, variation: float = 0.5) -> list[int]:
    if d <= 0 or n <= 0: 
        raise ValueError('d and n must be positive integers')
    if d > n: 
        raise ValueError('d must be less than n')
    if not (0.0 <= variation <= 1.0):
        raise ValueError("variation must be between 0 and 1")

    alpha_high = 200.0 
    alpha_low  = 0.2 
    alpha = (alpha_low ** variation) * (alpha_high ** (1.0 - variation))

    weights = [random.gammavariate(alpha, 1.0) for _ in range(d)]
    total_w = sum(weights)
    if total_w == 0: 
        probs = [1.0 / d] * d
    else:
        probs = [w / total_w for w in weights]

    rem = n - d
    if rem == 0:
        return [1] * d

    quotas = [p * rem for p in probs]
    floors = [floor(q) for q in quotas]
    assigned = sum(floors)
    need = rem - assigned

    frac_indices = sorted(
        range(d),
        key=lambda i: (quotas[i] - floors[i]),
        reverse=True
    )
    parts = [1 + floors[i] for i in range(d)]
    for i in frac_indices[:need]:
        parts[i] += 1

    return parts