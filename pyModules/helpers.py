

"""
=======================================================================================================================
HELPER MODULES
--------------

Methods:
    - SystemInfo:   Get runtime specific system information.
    - timeit:       Time runtime.
    - logging:      Log runtime behaviour.
    - store:        Lickle (interim) results.


: zach wolpe
: zach.wolpe@medibio.com.au
: 09 June 2023

=======================================================================================================================
"""

from pyModules.dependencies import *


class Helpers:

    @staticmethod
    def SystemInfo():
        try:
            info={}
            info['platform']            = platform.system()
            info['platform-release']    = platform.release()
            info['platform-version']    = platform.version()
            info['architecture']        = platform.machine()
            info['hostname']            = socket.gethostname()
            info['ip-address']          = socket.gethostbyname(socket.gethostname())
            info['mac-address']         = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['processor']           = platform.processor()
            info['ram']                 = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
            return info
        except Exception as e:
            logging.exception(e)
            return {'error':e}
    

    @staticmethod
    def timeit(func):
        """
        DECORATOR to time a function.
        """
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time  = time.perf_counter()
            result      = func(*args, **kwargs)
            end_time    = time.perf_counter()
            total_time  = end_time - start_time
            # print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
            return result, total_time
            # return result
        return timeit_wrapper

    

    @staticmethod
    def ConfigureLogger(log_file='runtime.log', LOG_LEVEL=logging.DEBUG, shutdown_logger=None, Custom_Filter=None, LOGFORMAT=None):
        """
        Configure logger.
        
        Parameters
        ----------
            - log_file (str):  Name of log file.
            - LOG_LEVEL (int): Logging level.
            - shutdown_logger (logger): Logger to shutdown.
            - Custom_Filter (logging.Filter): Custom filter to add to logger.
            - LOGFORMAT (str): Custom log format. NOTE: Ensure that the log format is compatible with the custom filter.
        """
    
        date_format = "%Y-%m-%d %H:%M:%S" 
        if LOGFORMAT is None:
            LOGFORMAT   = "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)"
            LOGFORMAT   = '[%(asctime)s] [%(levelname)8s] --- %(platform)s %(architecture)s %(ram)s: %(message)s (%(filename)s:%(lineno)s)'

        if shutdown_logger is not None:
            try:
                shutdown_logger.handlers.clear()
            except Exception as e:
                pass


        formatter   = logging.Formatter(LOGFORMAT, date_format)
        handler     = logging.FileHandler(log_file)
        logger      = logging.getLogger('Custom Logger:')
        
        if Custom_Filter is not None:
            handler.addFilter(Custom_Filter())
        handler.setLevel(logging.DEBUG)


        handler.setFormatter(formatter)
        logger.addHandler(handler)
        coloredlogs.install(level=LOG_LEVEL, logger=logger)

        return logger

        # Some examples.
        # logger.debug("this is a DEBUG message")
        # logger.info("this is an INFO message")
        # logger.warning("this is a WARNING message")
        # logger.error("this is an ERROR message")
        # logger.critical("this is a CRITCAL message")




class Custom_Filter(logging.Filter):
        """
        available attributes: ['platform', 'platform-release', 'platform-version', 'architecture', 'hostname', 'ip-address', 'mac-address', 'processor', 'ram']
        """
        Helpers.SystemInfo()

        # hostname = platform.node()
        system = Helpers.SystemInfo()
        hostname = system['hostname']

        def filter(self, record, system=system):
            for s,v in system.items():
                if s == 'hostname':
                    s = s.split('.')[0]
                record.__setattr__(s,v)
            return True





# Example Usage ================================================##


# @Helpers.timeit
# def calculate_something(num):
#     """
#     Simple function that returns sum of all numbers up to the square of num.
#     """
#     total = sum((x for x in range(0, num**2)))
#     return total



# if __name__ == '__main__':

#     # timer
#     @Helpers.timeit
#     def calculate_something(num):
#         """
#         Simple function that returns sum of all numbers up to the square of num.
#         """
#         total = sum((x for x in range(0, num**2)))
#         return total
    
#     calculate_something(10)
#     calculate_something(1000)
    
    
#     # test logger
#     log = Helpers.ConfigureLogger('log-1.log', LOG_LEVEL=logging.DEBUG, Custom_Filter=Custom_Filter)    
#     log.debug("- 1: my first logger.")   


#     log = Helpers.ConfigureLogger('log-2.log', LOG_LEVEL=logging.DEBUG, shutdown_logger=log, Custom_Filter=Custom_Filter)    
#     log.debug("- 2: my second logger.")
#     # log.handlers.clear()


#     log = Helpers.ConfigureLogger('log-3.log', LOG_LEVEL=logging.DEBUG, Custom_Filter=Custom_Filter)    
#     log.debug("- 3: my third logger.")


 

