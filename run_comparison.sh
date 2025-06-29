#!/bin/bash

echo "=========================================="
echo "Java vs Python Multithreading Comparison"
echo "=========================================="
echo "Testing CPU-intensive tasks to demonstrate:"
echo "• Python GIL limitations in threading"
echo "• Java's superior multithreading performance"
echo ""

cd "$(dirname "$0")"

echo "=== PYTHON RESULTS ==="
python3 python_performance_test.py
echo ""

echo "=== JAVA RESULTS ==="
javac JavaPerformanceTest.java
java JavaPerformanceTest
echo ""

echo "=========================================="
echo "PERFORMANCE ANALYSIS:"
echo "=========================================="
echo ""
echo "🐍 PYTHON OBSERVATIONS:"
echo "• Threading shows minimal/no speedup due to GIL"
echo "• Multiprocessing can achieve better performance"
echo "• Process creation overhead affects small tasks"
echo ""
echo "☕ JAVA OBSERVATIONS:"
echo "• True parallel execution with threads"
echo "• Better raw performance for CPU tasks"
echo "• Efficient thread management"
echo ""
echo "🔍 KEY TAKEAWAY:"
echo "For CPU-intensive tasks:"
echo "• Java threading > Python threading (due to GIL)"
echo "• Python needs multiprocessing for parallelism"
echo "• Java has lower overhead and better performance"
