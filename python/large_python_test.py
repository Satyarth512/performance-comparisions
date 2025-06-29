import threading
import time
import math
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import sys

NUM_THREADS = multiprocessing.cpu_count()

def cpu_task_large():
    """Larger CPU-bound task that can be pickled"""
    result = 0
    for i in range(5_000_000):  # 10x larger than before
        result += math.sin(i) * math.cos(i)
    return result

def is_prime(n):
    """CPU-intensive task: check if number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def count_primes_in_range(start, end):
    """Count primes in a given range"""
    count = 0
    for i in range(start, end):
        if is_prime(i):
            count += 1
    return count

def fibonacci(n):
    """CPU-intensive fibonacci calculation"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_sum(start, end):
    """Calculate sum of fibonacci numbers in range"""
    total = 0
    for i in range(start, end):
        total += fibonacci(i % 40)  # Mod to keep numbers manageable
    return total

def run_large_cpu_test():
    """Large CPU test to demonstrate performance differences"""
    print("=== Large CPU Test (Math Operations) ===")
    print("Processing 5 million math operations per task...")
    
    # Single thread
    start_time = time.time()
    result1 = cpu_task_large()
    single_time = time.time() - start_time
    print(f"Single thread - Time: {single_time:.3f}s")
    
    # Multiple threads (GIL limited)
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_task_large) for _ in range(4)]
        results = [f.result() for f in futures]
    thread_time = time.time() - start_time
    print(f"4 threads - Time: {thread_time:.3f}s")
    print(f"Threading speedup: {single_time/thread_time:.2f}x")
    
    # Multiple processes (bypasses GIL)
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_task_large) for _ in range(4)]
        results = [f.result() for f in futures]
    process_time = time.time() - start_time
    print(f"4 processes - Time: {process_time:.3f}s")
    print(f"Multiprocessing speedup: {single_time/process_time:.2f}x")
    print()

def run_large_prime_test():
    """Test prime number calculation with larger range"""
    print("=== Large Prime Number Test ===")
    range_size = 200_000  # 4x larger than before
    print(f"Finding primes up to {range_size:,}...")
    
    # Single-threaded
    start_time = time.time()
    single_result = count_primes_in_range(2, range_size)
    single_time = time.time() - start_time
    print(f"Single-threaded - Primes: {single_result:,}, Time: {single_time:.3f}s")
    
    # Multi-threaded (GIL limited)
    start_time = time.time()
    range_per_thread = range_size // NUM_THREADS
    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = 2 + (i * range_per_thread)
            end = range_size if i == NUM_THREADS - 1 else start + range_per_thread
            futures.append(executor.submit(count_primes_in_range, start, end))
        
        thread_result = sum(future.result() for future in futures)
    
    thread_time = time.time() - start_time
    print(f"Multi-threaded - Primes: {thread_result:,}, Time: {thread_time:.3f}s")
    print(f"Threading speedup: {single_time/thread_time:.2f}x")
    
    # Multi-process (bypasses GIL)
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = 2 + (i * range_per_thread)
            end = range_size if i == NUM_THREADS - 1 else start + range_per_thread
            futures.append(executor.submit(count_primes_in_range, start, end))
        
        process_result = sum(future.result() for future in futures)
    
    process_time = time.time() - start_time
    print(f"Multi-process - Primes: {process_result:,}, Time: {process_time:.3f}s")
    print(f"Multiprocessing speedup: {single_time/process_time:.2f}x")
    print()
def run_fibonacci_test():
    """Test fibonacci calculation - very CPU intensive"""
    print("=== Fibonacci Test ===")
    iterations = 100_000
    print(f"Computing fibonacci sums for {iterations:,} iterations...")
    
    # Single-threaded
    start_time = time.time()
    single_result = fibonacci_sum(0, iterations)
    single_time = time.time() - start_time
    print(f"Single-threaded - Result: {single_result:,}, Time: {single_time:.3f}s")
    
    # Multi-threaded (GIL limited)
    start_time = time.time()
    range_per_thread = iterations // NUM_THREADS
    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = i * range_per_thread
            end = iterations if i == NUM_THREADS - 1 else start + range_per_thread
            futures.append(executor.submit(fibonacci_sum, start, end))
        
        thread_result = sum(future.result() for future in futures)
    
    thread_time = time.time() - start_time
    print(f"Multi-threaded - Result: {thread_result:,}, Time: {thread_time:.3f}s")
    print(f"Threading speedup: {single_time/thread_time:.2f}x")
    
    # Multi-process (bypasses GIL)
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = i * range_per_thread
            end = iterations if i == NUM_THREADS - 1 else start + range_per_thread
            futures.append(executor.submit(fibonacci_sum, start, end))
        
        process_result = sum(future.result() for future in futures)
    
    process_time = time.time() - start_time
    print(f"Multi-process - Result: {process_result:,}, Time: {process_time:.3f}s")
    print(f"Multiprocessing speedup: {single_time/process_time:.2f}x")
    print()

if __name__ == "__main__":
    print("Python Large-Scale Multithreading vs Multiprocessing Test")
    print(f"Available processors: {NUM_THREADS}")
    print(f"Python version: {sys.version.split()[0]}")
    print("=" * 65)
    
    # Large CPU test
    run_large_cpu_test()
    
    # Large prime number test
    run_large_prime_test()
    
    # Fibonacci test
    run_fibonacci_test()
    
    print("=== LARGE-SCALE TEST FINDINGS ===")
    print("With larger workloads:")
    print("• Threading: Still limited by GIL")
    print("• Multiprocessing: Should show better speedup")
    print("• Process overhead: Less significant with larger tasks")
