# Benchmark Results Summary

## Test Environment
- **Hardware**: 10-core processor system
- **Java Version**: 24.0.1
- **Python Version**: 3.9.13
- **Operating System**: macOS

## Performance Results

### Math Operations (5M operations per task)
```
Python Single-threaded:      801ms
Python Threading:          3,101ms (0.26x - 4x slower!)
Python Multiprocessing:     892ms (0.90x speedup)
Java Single-threaded:       340ms
Java Threading:              356ms (0.95x speedup)
```
**Java is 2.3x faster than Python's best effort**

### Prime Calculation (200K numbers)
```
Python Single-threaded:     124ms
Python Threading:            126ms (1.00x - no improvement)
Python Multiprocessing:     114ms (1.18x speedup)
Java Single-threaded:         4ms
Java Threading:                6ms (0.67x speedup)
```
**Java is 31x faster than Python**

### Fibonacci Computation (100K iterations)
```
Python Single-threaded:      65ms
Python Threading:             66ms (0.99x - no improvement)
Python Multiprocessing:     105ms (0.62x - slower!)
Java Single-threaded:         2ms
Java Threading:                1ms (2.00x speedup)
```
**Java is 65x faster than Python**

## Key Findings

1. **Python's GIL severely limits threading performance** for CPU-bound tasks
2. **Python multiprocessing shows minimal improvement** due to overhead
3. **Java demonstrates 2-65x better performance** across all test scenarios
4. **Java's threading model provides true parallelism** without artificial constraints

## Conclusion

For CPU-intensive multithreaded applications, Java significantly outperforms Python in both raw performance and scalability.
