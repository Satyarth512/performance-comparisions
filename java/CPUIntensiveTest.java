import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

public class CPUIntensiveTest {
    private static final int NUM_THREADS = Runtime.getRuntime().availableProcessors();
    private static final long ITERATIONS_PER_THREAD = 100_000_000L;
    
    // CPU-intensive task: calculate prime numbers
    public static boolean isPrime(long n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        
        for (long i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        return true;
    }
    
    // Task that performs CPU-intensive work
    static class CPUTask implements Callable<Long> {
        private final long start;
        private final long end;
        
        public CPUTask(long start, long end) {
            this.start = start;
            this.end = end;
        }
        
        @Override
        public Long call() {
            long primeCount = 0;
            for (long i = start; i < end; i++) {
                if (isPrime(i)) {
                    primeCount++;
                }
            }
            return primeCount;
        }
    }    
    public static void runSingleThreaded() {
        System.out.println("=== Single-threaded execution ===");
        long startTime = System.currentTimeMillis();
        
        long totalPrimes = 0;
        for (long i = 2; i < ITERATIONS_PER_THREAD * NUM_THREADS; i++) {
            if (isPrime(i)) {
                totalPrimes++;
            }
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Single-threaded - Primes found: " + totalPrimes);
        System.out.println("Single-threaded - Time: " + (endTime - startTime) + " ms");
        System.out.println();
    }
    
    public static void runMultiThreaded() {
        System.out.println("=== Multi-threaded execution ===");
        System.out.println("Using " + NUM_THREADS + " threads");
        
        long startTime = System.currentTimeMillis();
        
        ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);
        Future<Long>[] futures = new Future[NUM_THREADS];
        
        // Divide work among threads
        long totalRange = ITERATIONS_PER_THREAD * NUM_THREADS;
        long rangePerThread = totalRange / NUM_THREADS;
        
        for (int i = 0; i < NUM_THREADS; i++) {
            long start = 2 + (i * rangePerThread);
            long end = (i == NUM_THREADS - 1) ? totalRange : start + rangePerThread;
            futures[i] = executor.submit(new CPUTask(start, end));
        }        
        // Collect results
        long totalPrimes = 0;
        try {
            for (Future<Long> future : futures) {
                totalPrimes += future.get();
            }
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        
        executor.shutdown();
        long endTime = System.currentTimeMillis();
        
        System.out.println("Multi-threaded - Primes found: " + totalPrimes);
        System.out.println("Multi-threaded - Time: " + (endTime - startTime) + " ms");
        System.out.println();
    }
    
    public static void runCPUBoundMathOperations() {
        System.out.println("=== CPU-bound math operations test ===");
        
        // Single-threaded math operations
        long startTime = System.currentTimeMillis();
        double result = 0;
        for (long i = 0; i < 50_000_000L; i++) {
            result += Math.sin(i) * Math.cos(i) + Math.sqrt(i);
        }
        long singleTime = System.currentTimeMillis() - startTime;
        System.out.println("Single-threaded math - Result: " + result);
        System.out.println("Single-threaded math - Time: " + singleTime + " ms");        
        // Multi-threaded math operations
        startTime = System.currentTimeMillis();
        ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);
        Future<Double>[] futures = new Future[NUM_THREADS];
        
        long operationsPerThread = 50_000_000L / NUM_THREADS;
        
        for (int i = 0; i < NUM_THREADS; i++) {
            final long start = i * operationsPerThread;
            final long end = (i == NUM_THREADS - 1) ? 50_000_000L : start + operationsPerThread;
            
            futures[i] = executor.submit(() -> {
                double localResult = 0;
                for (long j = start; j < end; j++) {
                    localResult += Math.sin(j) * Math.cos(j) + Math.sqrt(j);
                }
                return localResult;
            });
        }
        
        double totalResult = 0;
        try {
            for (Future<Double> future : futures) {
                totalResult += future.get();
            }
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        
        executor.shutdown();
        long multiTime = System.currentTimeMillis() - startTime;        
        System.out.println("Multi-threaded math - Result: " + totalResult);
        System.out.println("Multi-threaded math - Time: " + multiTime + " ms");
        System.out.printf("Speedup: %.2fx%n", (double) singleTime / multiTime);
        System.out.println();
    }
    
    public static void main(String[] args) {
        System.out.println("Java Multithreading CPU Performance Test");
        System.out.println("Available processors: " + NUM_THREADS);
        System.out.println("Java version: " + System.getProperty("java.version"));
        System.out.println("========================================");
        
        // Test 1: Prime number calculation
        runSingleThreaded();
        runMultiThreaded();
        
        // Test 2: Math operations
        runCPUBoundMathOperations();
        
        System.out.println("Test completed!");
    }
}