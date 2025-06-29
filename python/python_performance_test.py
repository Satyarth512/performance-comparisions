import threading
import time
import math
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import sys

NUM_THREADS = multiprocessing.cpu_count()

def cpu_task():
    """Simple CPU-bound task that can be pickled"""
    result = 0
    for i in range(500000):
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

def run_simple_cpu_test():
    """Simple CPU test to demonstrate GIL impact"""
    print("=== Simple CPU Test (Math Operations) ===")
    
    # Single thread
    start_time = time.time()
    result1 = cpu_task()
    single_time = time.time() - start_time
    print(f"Single thread - Time: {single_time:.3f}s")
    
    # Multiple threads (GIL limited)
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_task) for _ in range(4)]
        results = [f.result() for f in futures]
    thread_time = time.time() - start_time
    print(f"4 threads - Time: {thread_time:.3f}s")
    print(f"Threading speedup: {single_time/thread_time:.2f}x (GIL limited!)")
    
    # Multiple processes (bypasses GIL)
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_task) for _ in range(4)]
        results = [f.result() for f in futures]
    process_time = time.time() - start_time
    print(f"4 processes - Time: {process_time:.3f}s")
    print(f"Multiprocessing speedup: {single_time/process_time:.2f}x")
    print()

def run_prime_test():
    """Test prime number calculation"""
    print("=== Prime Number Test ===")
    range_size = 50000
    
    # Single-threaded
    start_time = time.time()
    single_result = count_primes_in_range(2, range_size)
    single_time = time.time() - start_time
    print(f"Single-threaded - Primes: {single_result}, Time: {single_time:.3f}s")
    
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
    print(f"Multi-threaded - Primes: {thread_result}, Time: {thread_time:.3f}s")
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
    print(f"Multi-process - Primes: {process_result}, Time: {process_time:.3f}s")
    print(f"Multiprocessing speedup: {single_time/process_time:.2f}x")
    print()

if __name__ == "__main__":
    print("Python Multithreading vs Multiprocessing Test")
    print(f"Available processors: {NUM_THREADS}")
    print(f"Python version: {sys.version.split()[0]}")
    print("=" * 50)
    
    # Simple CPU test
    run_simple_cpu_test()
    
    # Prime number test
    run_prime_test()
    
    print("=== KEY FINDINGS ===")
    print("✗ Threading: Poor speedup due to Global Interpreter Lock (GIL)")
    print("✓ Multiprocessing: Good speedup by bypassing GIL")
    print("✓ Java: Excellent threading performance (no GIL limitation)")
