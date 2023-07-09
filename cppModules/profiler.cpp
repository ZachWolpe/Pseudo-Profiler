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
 * : 07-07-2023
 * ---------------------------------------------------------
*/


#include <sys/types.h>
#include <sys/stat.h>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <fstream>
#include <thread>
#include <string>
#include <chrono>
#include <array>
#include <cmath>


class ProfilerInterface {
public:
    static void makdir(const std::string& sav_loc = "temp-store") {
        // To create director if required.
        int mkdir(const char *pathname, mode_t mode);
        std::stringstream ss;
        ss << sav_loc;
        int rc = mkdir(ss.str().c_str(), 0777);
        if (rc == 0) std::cout << "Directory created successfully: " << ss.str() << std::endl;
        else std::cout << "Failed." <<std::endl;
    };

    static void profiler(/* Function signature */) {}
    };


struct ProfileResult {
    std::string Name;
    long long Start, End;
    uint32_t ThreadID;
};

struct InstrumentSession {
    std::string Name;
};

class Instrumentor {
private:
    InstrumentSession* CurrentSession;
    std::ofstream OutputStream;
    int ProfileCount;

public:
    Instrumentor() : CurrentSession(nullptr), ProfileCount(0) {}

    void LaunchSession(const std::string& name, const std::string& filepath = "profile.json") {
        OutputStream.open(filepath);
        WriteHeader();
        CurrentSession       = new InstrumentSession;
        CurrentSession->Name = name;
    }
    void EndSession() {
        WriteFooter();
        OutputStream.close();
        delete CurrentSession;
        CurrentSession = nullptr;
        ProfileCount = 0;
    }
    void WriteProfile(const ProfileResult& result) {
        std::cout << " >> Writing profile (ProfileCount = " << ProfileCount << ")" << std::endl;
        if (ProfileCount++ > 0)
            OutputStream << ",";
        
        std::string name = result.Name;
        std::replace(name.begin(), name.end(), '"', '\'');
        OutputStream << "{";
        OutputStream << "\"cat\":\"function\",";
        OutputStream << "\"dur\":" << (result.End - result.Start) << ',';
        OutputStream << "\"name\":\"" << name << "\",";
        OutputStream << "\"ph\":\"X\",";
        OutputStream << "\"pid\":0,";
        OutputStream << "\"tid\":" << result.ThreadID << ",";
        OutputStream << "\"ts\":" << result.Start;
        OutputStream << "}";
        OutputStream.flush(); // flushes the stream buffer, to ensure the data is written to the file immediately. So that we do not lose data if the program crashes.

    }
    void WriteHeader() {
        OutputStream << "{\"otherData\": {},\"traceEvents\":[";
        OutputStream.flush();
    }
    void WriteFooter() {
        OutputStream << "]}";
        OutputStream.flush();
    }
    static Instrumentor& Get() {
        static Instrumentor instance;
        return instance;
    }
};



class CPUProfiler : public ProfilerInterface {
private:
    const char* name;
    std::string sav_loc;
    std::chrono::time_point<std::chrono::high_resolution_clock> startTime;
    bool Stopped;
public:
// std::string sav_loc = "temp-store",
    CPUProfiler( const char* name = "CPUProfiler"): name(name), Stopped(false) {
        startTime = std::chrono::high_resolution_clock::now();
    }
    ~CPUProfiler() {
        if (!Stopped)
            cpu_EndSession();
    }
    void cpu_EndSession() {
        auto endTime        = std::chrono::high_resolution_clock::now();
        auto start          = std::chrono::time_point_cast<std::chrono::microseconds>(startTime).time_since_epoch().count();
        auto end            = std::chrono::time_point_cast<std::chrono::microseconds>(endTime).time_since_epoch().count();
        uint32_t threadID   = std::hash<std::thread::id>()(std::this_thread::get_id());
        auto duration       = end - start;
        double ms           = duration * 0.001;
        double s            = duration * 0.001;
        ProfileResult result = {name, start, end, threadID};
        Instrumentor::Get().WriteProfile(result); 
        Stopped = true; // automatically end the session when we exit scope.
        // std::cout << "CPUProfiler: Process took: " << s << " seconds ( " << duration << " milliseconds)" << std::endl;
        // std::cout << "CPUProfiler: Process took: " << duration << "us (" << ms << "ms)" << std::endl;
        // makdir(sav_loc);
    }
};


// MACRO --------------------------------------------------------------->>
// to automatically generate the name of a function 
// use a macro to automatically generate the name of a function
#define PROFILING 1
#if PROFILING
#define PROFILING_SCOPE(name) CPUProfiler timer##__LINE__(name)
#define PROFILE_FUNCTION() PROFILING_SCOPE(__FUNCTION__)
#else
#define PROFILING_SCOPE(name)
#endif
// MACRO --------------------------------------------------------------->>


void looper() {
    // nonsense tester operation.
    std::cout << "    --- looper..." << std::endl;
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

void RunBenchmarks() {
    PROFILE_FUNCTION();
    std::cout << "Running Benchmarks..." << std::endl;
    Instrumentor::Get().LaunchSession("myprofiler", "profiler.json");
    function1();
    function2();
    Instrumentor::Get().EndSession();

};
