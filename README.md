# C++ & Python Profiler
-----

Decorators to attach to your `C++` or `Python` code to profile runtime characteristics.



## Getting Started

----
### C++ Profiler

The C++ profiler contains an `Instrumentor` class which is responsible for writing timing data to `.json`. This is then leveraged by the `CPUProfiler` class to write runtime data. The CPUProfiler decorates a function that you wish to profile.

1. Include the class declaration in the required source file (preferably using a header file).
   
  ```
  #include "[$PATH]/profiler.cpp"
  ```

2. Attached the macro (that calls the CPUProfiler decorator) to the desired code block.

  ```
  void function() {
    PROFILE_FUNCTION();
    // some function...
  };
  ```

3. Compile and build your source code.

4. Use chrome://tracing to upload and analyse the (nearly created) `profile.json` file.


----
### Python Profiler

1. Simply attach the decorators `@CPUProfiler.profile` and `@MemoryProfiler.profile` to any code and you'll generate the necessary data.

2. I recommend using `snakeviz` to view the newly generated `.prof` file.

   ```
   snakeviz [$PATH]/pstats.prof
   ```


----
## Example

A detailed example is provided on my [Medium](http://medium.com/ZachWolpe)



```
: Zach Wolpe
: 10 July 2023
```
