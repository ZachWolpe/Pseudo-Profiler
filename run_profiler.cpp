/***
 * ---------------------------------------------------------
 * Timing Code:
 * 
 * Reference: https://gist.github.com/TheCherno/31f135eea6ee729ab5f26a6908eb3a5e
 *
 *  - The simpliest for of benchmarking, to be used as a starting point.
 *  - Note:
 *      Runtime behaviour may differ from debug behaviour, as the compiler may optimizer code.
 *      Debug mode should be used, and one should be aware of the compiler's optimisation settings.
 * 
 * : Zach Wolpe
 * : zach.wolpe@medibio.com.au
 * : 09-07-2023
 * ---------------------------------------------------------
*/

#include "cppModules/profiler.cpp"

void looper() {
    // nonsense tester operation.
    for (int i=1; i<=1000000; i++) {};
};

void function1() {
    PROFILE_FUNCTION();
    std::cout << "  - Running function1..." << std::endl;
    looper();
};

void function2() {
    PROFILE_FUNCTION();
    std::cout << "  - Running function2..." << std::endl;
    looper();
};


void functionWrapper() {
    PROFILE_FUNCTION();
    std::cout << "functionWrapper Benchmarks..." << std::endl;
    looper();
    function1();
    function2();
};

void programWrapper() {
    PROFILE_FUNCTION();
    std::cout << ">> Running programWrapper..." << std::endl;
    Instrumentor::Get().LaunchSession("myprofiler", "profiler.json");
    functionWrapper();
    Instrumentor::Get().EndSession();
};


int main() {
    programWrapper();
    return 0;
}

