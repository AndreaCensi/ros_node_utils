__all__ = ['RospyLogger']

class RospyLogger:

    def __init__(self, prefix):
        if prefix is not None:
            self.prefix = '%s:' % prefix
        else:
            self.prefix = '' 

    def info(self, s):
        import rospy
        rospy.loginfo("%s%s" % (self.prefix, s))  # @UndefinedVariable

    def debug(self, s):
        import rospy
        rospy.logdebug("%s%s" % (self.prefix, s))  # @UndefinedVariable

    def error(self, s):
        import rospy
        rospy.logerr("%s%s" % (self.prefix, s))  # @UndefinedVariable

