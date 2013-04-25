import rospy


class ROSNode():
    """ Some common utilities for ROS nodes. """ 
    
    def __init__(self, prefix=None):
        self.prefix = '' if prefix is None else '%s: ' % prefix
    

    # Logging shortcuts
    
    def info(self, s):
        rospy.loginfo("%s%s" % (self.prefix, s))  # @UndefinedVariable

    def error(self, s):
        rospy.logerr("%s%s" % (self.prefix, s))  # @UndefinedVariable

