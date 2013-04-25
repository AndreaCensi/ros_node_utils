
import sys
import traceback


def wrap_ros_script(function):
    import rospy
    try:
        function()
        sys.exit(0)
    except rospy.ROSInterruptException:  # @UndefinedVariable
        sys.exit(0)
    except Exception:
        rospy.logerr('Robot adapter terminated due to an exception:\n%s'
                       % traceback.format_exc())
        sys.exit(-1)


