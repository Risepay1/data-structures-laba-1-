def find_min_number(N):
    remainder = 0
    for k in range(1, 10**6 + 1):
        remainder = (remainder * 10 + 1) % N
        if remainder == 0:
            return '1' * k
    return "NO"

N = 57
print(find_min_number(N))
