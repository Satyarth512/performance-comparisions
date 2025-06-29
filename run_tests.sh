#!/bin/bash

echo "============================================"
echo "Java vs Python Multithreading Comparison"
echo "============================================"

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if Java is available
if command -v java &> /dev/null; then
    echo "✓ Java found: $(java -version 2>&1 | head -n 1)"
else
    echo "✗ Java not found. Please install Java to run the Java test."
    exit 1
fi

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✓ Python found: $(python3 --version)"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "✓ Python found: $(python --version)"
    PYTHON_CMD="python"
else
    echo "✗ Python not found. Please install Python to run the Python test."
    exit 1
fi

echo ""
echo "Running tests..."
echo ""

# Compile and run Java test
echo "========== JAVA TEST =========="
if javac CPUIntensiveTest.java; then
    java CPUIntensiveTest
    echo ""
else
    echo "Failed to compile Java code"
fi

echo "========== PYTHON TEST =========="
$PYTHON_CMD cpu_intensive_test.py

echo ""
echo "============================================"
echo "Comparison Summary:"
echo "============================================"
echo "Expected Results:"
echo "• Java: Near-linear speedup with multiple threads"
echo "• Python Threading: Minimal speedup due to GIL"
echo "• Python Multiprocessing: Good speedup (bypasses GIL)"
echo ""
echo "Key Takeaways:"
echo "1. Java's threads can utilize multiple CPU cores effectively"
echo "2. Python's GIL limits CPU-bound threading performance"
echo "3. Python multiprocessing is needed for CPU parallelism"
echo "4. Java generally shows better raw performance for CPU tasks"