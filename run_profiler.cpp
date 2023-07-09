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
void RunBenchmarks();

int main() {
    RunBenchmarks();
    // std::cin.get();
    return 0;
}








