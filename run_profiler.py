# from pyModules.dependencies   import *
from pyModules.profiler import *

if __name__ == '__main__':

    @CPUProfiler.profile 
    @MemoryProfiler.profile
    def test_func(*args, **kwargs):
        a = []

        print('launching test_func()..')
        time.sleep(1)
        for i in range(100000):
            a.append(i)
        print('test_func() finished.')
        return True

    result, mem_profile = test_func(sav_loc='temp-store')
    print('\nresult:    ', result)
    print('mem_profile: ', mem_profile)
