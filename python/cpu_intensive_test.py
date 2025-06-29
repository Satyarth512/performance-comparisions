import threading
import time
import math
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import sys

NUM_THREADS = multiprocessing.cpu_count()
ITERATIONS_PER_THREAD = 10_000_000  # Reduced for Python due to slower execution

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
def math_operations(start, end):
    """CPU-intensive math operations"""
    result = 0.0
    for i in range(start, end):
        result += math.sin(i) * math.cos(i) + math.sqrt(i)
    return result

def run_single_threaded():
    """Test single-threaded execution"""
    print("=== Single-threaded execution ===")
    start_time = time.time()
    
    total_primes = count_primes_in_range(2, ITERATIONS_PER_THREAD * NUM_THREADS)
    
    end_time = time.time()
    print(f"Single-threaded - Primes found: {total_primes}")
    print(f"Single-threaded - Time: {(end_time - start_time):.2f} seconds")
    print()
    return end_time - start_time

def run_multi_threaded():
    """Test multi-threaded execution (affected by GIL)"""
    print("=== Multi-threaded execution (with GIL limitation) ===")
    print(f"Using {NUM_THREADS} threads")
    
    start_time = time.time()
    
    # Divide work among threads
    total_range = ITERATIONS_PER_THREAD * NUM_THREADS
    range_per_thread = total_range // NUM_THREADS    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = 2 + (i * range_per_thread)
            end = total_range if i == NUM_THREADS - 1 else start + range_per_thread
            futures.append(executor.submit(count_primes_in_range, start, end))
        
        total_primes = sum(future.result() for future in futures)
    
    end_time = time.time()
    print(f"Multi-threaded - Primes found: {total_primes}")
    print(f"Multi-threaded - Time: {(end_time - start_time):.2f} seconds")
    print()
    return end_time - start_time

def run_multi_process():
    """Test multi-process execution (bypasses GIL)"""
    print("=== Multi-process execution (bypasses GIL) ===")
    print(f"Using {NUM_THREADS} processes")
    
    start_time = time.time()
    
    # Divide work among processes
    total_range = ITERATIONS_PER_THREAD * NUM_THREADS
    range_per_process = total_range // NUM_THREADS
    
    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = 2 + (i * range_per_process)
            end = total_range if i == NUM_THREADS - 1 else start + range_per_process
            futures.append(executor.submit(count_primes_in_range, start, end))
        
        total_primes = sum(future.result() for future in futures)
    
    end_time = time.time()
    print(f"Multi-process - Primes found: {total_primes}")
    print(f"Multi-process - Time: {(end_time - start_time):.2f} seconds")
    print()
    return end_time - start_time
def run_math_operations_test():
    """Test CPU-bound math operations"""
    print("=== CPU-bound math operations test ===")
    
    operations_count = 5_000_000  # Reduced for Python
    
    # Single-threaded math operations
    start_time = time.time()
    result = math_operations(0, operations_count)
    single_time = time.time() - start_time
    print(f"Single-threaded math - Result: {result:.6f}")
    print(f"Single-threaded math - Time: {single_time:.2f} seconds")
    
    # Multi-threaded math operations (with GIL)
    start_time = time.time()
    operations_per_thread = operations_count // NUM_THREADS
    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = i * operations_per_thread
            end = operations_count if i == NUM_THREADS - 1 else start + operations_per_thread
            futures.append(executor.submit(math_operations, start, end))
        
        total_result = sum(future.result() for future in futures)
    
    thread_time = time.time() - start_time
    print(f"Multi-threaded math - Result: {total_result:.6f}")
    print(f"Multi-threaded math - Time: {thread_time:.2f} seconds")
    print(f"Threading speedup: {single_time / thread_time:.2f}x")    
    # Multi-process math operations (bypasses GIL)
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_THREADS):
            start = i * operations_per_thread
            end = operations_count if i == NUM_THREADS - 1 else start + operations_per_thread
            futures.append(executor.submit(math_operations, start, end))
        
        total_result = sum(future.result() for future in futures)
    
    process_time = time.time() - start_time
    print(f"Multi-process math - Result: {total_result:.6f}")
    print(f"Multi-process math - Time: {process_time:.2f} seconds")
    print(f"Multiprocessing speedup: {single_time / process_time:.2f}x")
    print()

if __name__ == "__main__":
    print("Python Multithreading vs Multiprocessing CPU Performance Test")
    print(f"Available processors: {NUM_THREADS}")
    print(f"Python version: {sys.version}")
    print("=" * 60)
    
    # Test 1: Prime number calculation
    single_time = run_single_threaded()
    thread_time = run_multi_threaded()
    process_time = run_multi_process()
    
    print("=== Performance Summary ===")
    print(f"Single-threaded: {single_time:.2f}s (baseline)")
    print(f"Multi-threaded: {thread_time:.2f}s (speedup: {single_time/thread_time:.2f}x)")
    print(f"Multi-process: {process_time:.2f}s (speedup: {single_time/process_time:.2f}x)")
    print()
    
    # Test 2: Math operations
    run_math_operations_test()
    
    print("Key Observations:")
    print("1. Multi-threading shows minimal improvement due to GIL")
    print("2. Multi-processing shows significant improvement by bypassing GIL")
    print("3. Java's threading model allows true parallelism for CPU-bound tasks")
    print("4. Python's GIL serializes CPU-bound operations in threads")
    
    print("\nTest completed!")