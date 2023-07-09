"""
============================================================================
script: Profiling.py

description:
    - This script is used to profile the CPU & memory usage of a python script.

: zach wolpe
: zach.wolpe@medibio.com.au
: 07 June 2023

----------------------------------------------------------------------------
Execution notes:
    CPU Profiler
    ------------
    
    usage:
    
        # run snakeviz (mac os)
        1. Attach the decorator @CPUProfiler.profile to the function you want to profile.
        2. run the script. pstats files will be saved to the sav_loc, including `pstats.prof`.
        3. In the command line, run:
            python -m pip install snakeviz
            snakeviz [PATH]/pstats.prof
        4. A browser window will open with the profile results.


        Additional Notes (Deprecated):
        -----------------
            run gprof2dot.py
            gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png


    Memory Profiler
    ---------------

    usage:
        mprof run script.py
        mprof plot
        mprof plot --output {PATH}/output.png
        
    Alternatives:
    https://stackoverflow.com/questions/552744/how-do-i-profile-memory-usage-in-python
----------------------------------------------------------------------------
    
============================================================================
"""

# 
from pyModules.dependencies import *


class ProfilerInterface(ABC):

    @staticmethod
    def makdir(sav_loc='temp-store'):
        if not os.path.exists(sav_loc):
            os.makedirs(sav_loc)
    
    @staticmethod
    def set_params(**kwargs):
        "**kwargs: sav_loc='temp-store', overwrite=True, print_stats=True,"
        sav_loc = 'temp-store'; overwrite=True; print_stats=True
        if 'print_stats'    in kwargs: print_stats  = kwargs['print_stats']
        if 'overwrite'      in kwargs: overwrite    = kwargs['overwrite']
        if 'sav_loc'        in kwargs: sav_loc      = kwargs['sav_loc']
        ProfilerInterface.makdir(sav_loc)
        return sav_loc, overwrite, print_stats
    
    @abstractmethod
    def profiler(func, *args, **kwargs):
        "**kwargs: sav_loc='temp-store', overwrite=True, print_stats=True"
        pass



class MemoryProfiler(ProfilerInterface):

    def elapsed_since(start):
        return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
 
    
    def get_process_memory():
        """
        Returns:    memory usage of the current process in bites.
        Notes:      `process.memory_info()` is used but also consider `psutil.virtual_memory()`
        """
        process  = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return mem_info.rss



    @staticmethod
    def save_memory_profile(results, path):
        with open(f'{path}/memory_profile.pkl', 'wb') as f:
            pickle.dump(results, f)

    # def profile(func, *args, **kwargs):
    #     def wrapper(*args, **kwargs):
    #         # set params ---------------------------++
    #         sav_loc, overwrite, print_stats = ProfilerInterface.set_params(**kwargs)
    #         # run profiler -------------------------++
    #         result, results = CPUProfiler.profiler(func, sav_loc=sav_loc, overwrite=overwrite, print_stats=print_stats, *args, **kwargs)
    #         return result, results
    #     return wrapper
    
    def profile(func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            sav_loc, _, print_stats = ProfilerInterface.set_params(**kwargs)
            result, mem_profile     = MemoryProfiler.profiler(func, *args, **kwargs)
            MemoryProfiler.save_memory_profile(mem_profile, sav_loc)
            if print_stats:
                print('Memory profile saved to {}_memory_profile.pkl'.format(sav_loc))
            return result, mem_profile
        return wrapper


    
    @staticmethod
    def profiler(func, *args, **kwargs):
        mem_start = MemoryProfiler.get_process_memory()
        start     = time.time()
        result    = func(*args, **kwargs)
        elapsed   = MemoryProfiler.elapsed_since(start)
        mem_end   = MemoryProfiler.get_process_memory()
        mem_profile   = {
            'mem_start' : mem_start,
            'mem_end'   : mem_end,
            'mem_used'  : mem_end - mem_start,
            'time'      : elapsed,
            'func_name' : func.__name__
        }
        return result, mem_profile



class CPUProfiler(ProfilerInterface):

    @staticmethod
    def convert_to_csv(infile, outfile):
        res = infile.read()
        res = 'ncalls' + res.split('ncalls')[-1]
        res = '\n'.join([','.join(line.rstrip().split(None,5)) for line in res.split('\n')])
        outfile.write(res)
        outfile.close()
    
    def profile(func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            # run profiler -------------------------++
            result, results = CPUProfiler.profiler(func, *args, **kwargs)
            return result, results
        return wrapper

    
    @staticmethod
    def profiler(func, *args, **kwargs):
        sav_loc, overwrite, print_stats = ProfilerInterface.set_params(**kwargs)
        suffix = '' if overwrite else '+'

        with cProfile.Profile() as pr:
            result   = func(*args, **kwargs)
            
            txt_file = open(f'{sav_loc}/pstats.txt', 'w{}'.format(suffix))
            results  = pstats.Stats(pr, stream=txt_file)
            results.sort_stats(pstats.SortKey.TIME)
            if print_stats:
                results.print_stats(25)

            # save results to pickle file
            results.dump_stats(f'{sav_loc}/pstats.pstats')
            results.dump_stats(f'{sav_loc}/pstats.prof')
            txt_file.close()
            
            # convert to csv
            with open(f'{sav_loc}/pstats.txt', 'r') as infile, open(f'{sav_loc}/pstats.csv', 'w{}'.format(suffix)) as outfile:
                CPUProfiler.convert_to_csv(infile, outfile)
            
            if print_stats:
                msg = """
                \nProfile saved to:
                - {}/pstats.pstats
                - {}/pstats.prof
                - {}/pstats.csv
                """.format(sav_loc, sav_loc, sav_loc)
                print(msg)

            
            return result, results





# Example Usage -----------------------------------------------------------------++
# -------------------------------------------------------------------------------++

# def build():
#     arr = []
#     for a in range(0, 1000000):
#         arr.append(a)

# def deploy():
#     print('Array deployed!')

# def main():
#     build()
#     deploy()



# if __name__ == '__main__':
#     Profiler.profile(main)

# -------------------------------------------------------------------------------++
# -------------------------------------------------------------------------------++


