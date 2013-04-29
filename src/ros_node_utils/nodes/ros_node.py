

class ROSNode():
    """ Some common utilities for ROS nodes. """ 
    
    def __init__(self, prefix=None):
        self.prefix = '' if prefix is None else '%s: ' % prefix
    

    # Logging shortcuts
    
    def info(self, s):
        import rospy
        rospy.loginfo("%s%s" % (self.prefix, s))  # @UndefinedVariable

    def error(self, s):
        import rospy
        rospy.logerr("%s%s" % (self.prefix, s))  # @UndefinedVariable

    def debug(self, s):
        import rospy
        rospy.logdebug("%s%s" % (self.prefix, s))  # @UndefinedVariable
