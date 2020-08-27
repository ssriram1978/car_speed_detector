import logging
import sys

from car_speed_detector.constants import PACKAGE_NAME


class Logger:
   __logger_instance = None

   @classmethod
   def get_logger(cls, verbose=False):
       """
       Create a singleton logger handled by stdout

       :param level: logging level, default to INFO
       :return: the configured singleton __logger_instance
       """
       if not cls.__logger_instance:
           logger_inst = logging.getLogger(PACKAGE_NAME)
           console_handler = logging.StreamHandler(sys.stdout)
           if verbose:
               logger_inst.setLevel(logging.DEBUG)
               console_handler.setLevel(logging.DEBUG)
           else:
               logger_inst.setLevel(logging.INFO)
               console_handler.setLevel(logging.INFO)

           console_handler.setFormatter(
               logging.Formatter("%(asctime)s - %(name)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s")
           )
           logger_inst.addHandler(console_handler)
           logger_inst.propagate = False
           cls.__logger_instance = logging.LoggerAdapter(logger_inst, {})

       return cls.__logger_instance


def logger():
   """
   This function returns the log level set for this package.
   :return:
   """
   return Logger.get_logger()
