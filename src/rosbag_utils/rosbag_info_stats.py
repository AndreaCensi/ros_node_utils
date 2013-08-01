from contracts import contract
from contracts.utils import indent
from rosbag_utils import logger
from rosbag_utils.utils import system_cmd_result
import os
import warnings
import yaml


__all__ = ['rosbag_info', 'rosbag_info_cached']


@contract(returns='dict')
def rosbag_info(bag):
    """ Returns a dictionary with the fields returned by "rosbag info". """
    if not os.path.exists(bag):
        raise ValueError('no file %r' % bag)
    
    warnings.warn('Check exit code')
    
    cmd = ['rosbag', 'info', '--yaml', bag]
    cwd = os.getcwd()
    # print('cmd: %s' % cmd)
    res = system_cmd_result(cwd, cmd,
                      display_stdout=False,
                      display_stderr=False,
                      raise_on_error=True,
                      capture_keyboard_interrupt=False)
    
    stdout = res.stdout
#     stdout = subprocess.Popen(
#                               stdout=subprocess.PIPE).communicate()[0]
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

@contract(returns='dict')
def rosbag_info_cached(bag):
    """ Caches the result in a file <filename>.info.yaml """
    cache = bag + '.info.yaml'
    if os.path.exists(cache):
        logger.debug('Reading from cache: %s' % cache)
        with open(cache) as f:
            cached = yaml.load(f)
            if not isinstance(cached, dict):
                logger.debug('Invalid cache: %s' % cached)
                os.unlink(cache)
                return rosbag_info_cached(bag)
            return cached
    else:
        result = rosbag_info(bag)
        with open(cache, 'w') as f:
            yaml.dump(result, f)
        return result
    
    
