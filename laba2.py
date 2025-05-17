import numpy as np
import time
import scipy.linalg.blas as blas
import sys
import io

# Настройка кодировки для корректного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Параметры вычислений
N = 4096  
BLOCK_SIZE = 128  
NUM_RUNS = 3  

def generate_matrix(n):
    """Генерация случайной комплексной матрицы заданного размера (single precision)"""
    return np.random.rand(n, n).astype(np.float32) + 1j * np.random.rand(n, n).astype(np.float32)

def blas_multiplication(A, B):
    """Оптимизированное умножение через BLAS (single precision)"""
    return blas.cgemm(1.0, A, B)

def block_multiplication(A, B, block_size=BLOCK_SIZE):
    """Блочное умножение матриц с оптимизацией кэша (single precision)"""
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.complex64)
    
    for bi in range(0, n, block_size):
        for bj in range(0, n, block_size):
            for bk in range(0, n, block_size):
                
                i_end = min(bi + block_size, n)
                j_end = min(bj + block_size, n)
                k_end = min(bk + block_size, n)
                
                C[bi:i_end, bj:j_end] += A[bi:i_end, bk:k_end] @ B[bk:k_end, bj:j_end]
    return C

def run_benchmark(name, func, A, B):
    """Запуск и замер производительности алгоритма"""
    total_time = 0.0
    operations = 2 * N ** 3 
    
    # Прогрев системы 
    if name == "Block":
        func(A, B)
    
    for _ in range(NUM_RUNS):
        start = time.time()
        result = func(A, B)
        elapsed = time.time() - start
        total_time += elapsed
    
    avg_time = total_time / NUM_RUNS
    performance = (operations / avg_time) / 1e6 
    
    print(f"{name:<10} | Среднее время: {avg_time:.2f} сек | "
          f"Производительность: {performance:,.2f} MFLOP/с")
    return avg_time

def main():
    """Основная функция выполнения"""
    np.random.seed(42)  
    
    print(f"Умножение комплексных матриц {N}×{N} (single precision)")
    print(f"Теоретическая сложность: {2 * N ** 3 / 1e12:.2f} TFLOP")
    print("-" * 70)
    
    # Генерация входных матриц
    print("Генерация матриц:")
    A = generate_matrix(N)
    B = generate_matrix(N)
    
    # Запуск тестов производительности
    print("\nЗапуск BLAS реализации:")
    blas_time = run_benchmark("BLAS", blas_multiplication, A, B)
    
    print("\nЗапуск блочного метода:")
    block_time = run_benchmark("Block", block_multiplication, A, B)
    
    # Сравнение производительности
    print("\n" + "=" * 70)
    performance_ratio = (blas_time / block_time) * 100
    print(f"Производительность Block относительно BLAS: {performance_ratio:.1f}%")
    
    if performance_ratio >= 30:
        print("Условие выполнено: Block ≥ 30% от BLAS")
    else:
        print("Условие не выполнено")

if __name__ == "__main__":
    try:
        main()
    except MemoryError:
        print("Ошибка: Недостаточно памяти для матриц такого размера!")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        sys.exit(1)

print("Токбаев Борис Вячеславович 090304-РПИб-о24")
