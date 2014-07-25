import os
import warnings

from contracts import contract
from contracts.utils import indent
import yaml

from rosbag_utils import logger

from .utils import system_cmd_result


__all__ = ['rosbag_info', 'rosbag_info_cached']


@contract(returns='dict')
def rosbag_info(bag):
    """ Returns a dictionary with the fields returned by "rosbag info". """
    if not os.path.exists(bag):
        raise ValueError('no file %r' % bag)
    
#     raise Exception('rosbag_info for %r' % bag)
    
    cmd = ['rosbag', 'info', '--yaml', bag]
    cwd = os.getcwd()

    res = system_cmd_result(cwd, cmd,
                      display_stdout=False,
                      display_stderr=False,
                      raise_on_error=True,
                      capture_keyboard_interrupt=False)
    
    stdout = res.stdout

    try:
        info_dict = yaml.load(stdout)
    except:
        logger.error('Could not parse yaml:\n%s' % indent(stdout, '| '))
        raise
    
    return info_dict

# Example output:
# path: /home/andrea/01-youbot-ros-logs-good/unicornA_base1_2013-04-02-20-37-43.bag
# version: 2.0
# duration: 3499.176103
# start: 1364960263.862855
# end: 1364963763.038959
# size: 997946578
# messages: 2656954
# indexed: True
# compression: bz2
# uncompressed: 1840288997
# compressed: 962203048
# types:
#     - type: array_msgs/FloatArray
#       md5: 788898178a3da2c3718461eecda8f714 
# topics:
#     - topic: /arm_1/arm_controller/position_command
#       type: brics_actuator/JointPositions

class Storage():
    warned_cache = set()
    cache = {}

@contract(returns='dict')
def rosbag_info_cached(bag):
    """ Caches the result in a file <filename>.info.yaml """
    if bag in Storage.cache:
        return Storage.cache[bag]
    
    cache = bag + '.info.yaml'
    if os.path.exists(cache):
        if not cache in Storage.warned_cache:
            # only warn once per file
            logger.debug('Reading from cache: %s' % cache)
            Storage.warned_cache.add(cache)
        with open(cache) as f:
            cached = yaml.load(f)
            if not isinstance(cached, dict):
                logger.error('Invalid cache: %s' % cached)
                os.unlink(cache)
                return rosbag_info_cached(bag)
            Storage.cache[bag] = cached
            return cached
    else:
        print('cache file does not exist: %s' % cache)
        result = rosbag_info(bag)
        with open(cache, 'w') as f:
            yaml.dump(result, f)
        Storage.cache[bag] = result
        return result
    
    
