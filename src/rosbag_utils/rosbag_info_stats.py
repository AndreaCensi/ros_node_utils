import subprocess
import yaml
from contracts import contract
import os
import warnings

@contract(returns='dict')
def rosbag_info(bag):
    """ Returns a dictionary with the fields returned by "rosbag info". """
    if not os.path.exists(bag):
        raise ValueError('no file %r' % bag)
    warnings.warn('Check exit code')
    stdout = subprocess.Popen(['rosbag', 'info', '--yaml', bag],
                              stdout=subprocess.PIPE).communicate()[0]
    info_dict = yaml.load(stdout)
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
