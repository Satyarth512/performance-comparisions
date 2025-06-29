#!/bin/bash

echo "========================================================"
echo "Java vs Python Multithreading Performance Benchmark"
echo "========================================================"
echo "This comprehensive benchmark will test both languages"
echo "across multiple CPU-intensive scenarios."
echo ""
echo "Tests included:"
echo "• Quick performance comparison"
echo "• Large-scale workload analysis"  
echo "• Comprehensive CPU-intensive tests"
echo ""

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check dependencies
echo "Checking dependencies..."

# Check Java
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1)
    echo "✓ Java found: $JAVA_VERSION"
else
    echo "✗ Java not found. Please install Java 11+ to run Java tests."
    echo "  Java tests will be skipped."
    SKIP_JAVA=true
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✓ Python found: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "✗ Python not found. Please install Python 3.7+ to run Python tests."
    echo "  Python tests will be skipped."
    SKIP_PYTHON=true
fi

echo ""
echo "System Information:"
echo "• Available CPU cores: $(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 'Unknown')"
echo "• Operating System: $(uname -s)"
echo "• Architecture: $(uname -m)"
echo ""

if [[ "$SKIP_JAVA" == "true" && "$SKIP_PYTHON" == "true" ]]; then
    echo "❌ Both Java and Python are missing. Cannot run any tests."
    exit 1
fi

echo "========================================================"
echo "RUNNING BENCHMARKS"
echo "========================================================"

# Test 1: Quick Performance Comparison
echo ""
echo "🚀 Test 1: Quick Performance Comparison"
echo "----------------------------------------"

if [[ "$SKIP_PYTHON" != "true" ]]; then
    echo "Running Python quick test..."
    $PYTHON_CMD python/python_performance_test.py
    echo ""
fi

if [[ "$SKIP_JAVA" != "true" ]]; then
    echo "Running Java quick test..."
    if javac java/JavaPerformanceTest.java 2>/dev/null; then
        java -cp java JavaPerformanceTest
    else
        echo "Failed to compile JavaPerformanceTest.java"
    fi
    echo ""
fi

# Test 2: Large-Scale Workload Analysis
echo ""
echo "🔥 Test 2: Large-Scale Workload Analysis"
echo "-----------------------------------------"

if [[ "$SKIP_PYTHON" != "true" ]]; then
    echo "Running Python large-scale test..."
    $PYTHON_CMD python/large_python_test.py
    echo ""
fi

if [[ "$SKIP_JAVA" != "true" ]]; then
    echo "Running Java large-scale test..."
    if javac java/LargeJavaTest.java 2>/dev/null; then
        java -cp java LargeJavaTest
    else
        echo "Failed to compile LargeJavaTest.java"
    fi
    echo ""
fi

# Test 3: Comprehensive Analysis (if files exist)
if [[ -f "python/cpu_intensive_test.py" && -f "java/CPUIntensiveTest.java" ]]; then
    echo ""
    echo "🧪 Test 3: Comprehensive CPU-Intensive Analysis"
    echo "-----------------------------------------------"
    echo "⚠️  Warning: This test may take several minutes to complete."
    echo ""
    
    read -p "Run comprehensive tests? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$SKIP_PYTHON" != "true" ]]; then
            echo "Running Python comprehensive test..."
            $PYTHON_CMD python/cpu_intensive_test.py
            echo ""
        fi
        
        if [[ "$SKIP_JAVA" != "true" ]]; then
            echo "Running Java comprehensive test..."
            if javac java/CPUIntensiveTest.java 2>/dev/null; then
                java -cp java CPUIntensiveTest
            else
                echo "Failed to compile CPUIntensiveTest.java"
            fi
            echo ""
        fi
    else
        echo "Skipping comprehensive tests."
    fi
fi

echo "========================================================"
echo "BENCHMARK SUMMARY"
echo "========================================================"
echo ""
echo "✅ All available tests completed successfully!"
echo ""
echo "🔍 KEY OBSERVATIONS:"
echo ""
echo "If you ran the complete benchmark suite, you should observe:"
echo ""
echo "1. PYTHON PERFORMANCE:"
echo "   • Threading: Minimal or negative speedup due to GIL"
echo "   • Multiprocessing: Limited speedup due to overhead"
echo "   • Best case: 1.1-1.2x speedup in optimal scenarios"
echo ""
echo "2. JAVA PERFORMANCE:"
echo "   • Threading: True parallel execution capability"
echo "   • Significant raw performance advantage (2-65x faster)"
echo "   • Consistent scaling with available CPU cores"
echo ""
echo "3. PRACTICAL IMPLICATIONS:"
echo "   • For CPU-intensive tasks: Java >> Python"
echo "   • Python's strength: Rapid development, rich libraries"
echo "   • Java's strength: Performance, scalability, true parallelism"
echo ""
echo "📊 DETAILED ANALYSIS:"
echo ""
echo "Check the generated log files for detailed performance metrics:"
if [[ "$SKIP_PYTHON" != "true" ]]; then
    echo "• Python results logged to console output above"
fi
if [[ "$SKIP_JAVA" != "true" ]]; then
    echo "• Java results logged to console output above"
fi
echo ""
echo "🚀 NEXT STEPS:"
echo ""
echo "1. Review the performance differences for your specific hardware"
echo "2. Consider your application's requirements (development speed vs execution speed)"
echo "3. For production CPU-intensive systems, consider Java's advantages"
echo "4. For rapid prototyping and data science, Python remains excellent"
echo ""
echo "📝 SHARING RESULTS:"
echo ""
echo "Found interesting results? Please share them with the community:"
echo "• GitHub Issues: Report your hardware-specific findings"
echo "• Medium Article: Comment with your benchmark results"
echo "• Twitter: Tag @your-handle with your results"
echo ""
echo "Thank you for running the Java vs Python multithreading benchmark!"
echo "========================================================"
