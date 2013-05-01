from . import logger as main_logger
from .utils import InAWhile
from contracts import contract
from .rosbag_info_stats import _rosbag_info
   

def _read_bag_stats_progress(source, logger, interval=5):
    """ This is a wrapper for read_bag_stats that visualizes some statistics. """ 
    tracker = InAWhile(interval)
    
    for topic, msg, t, extra in source:
        if tracker.its_time():
            progress = extra['t_percentage']
            cur_obs = extra['counter']
            num_obs = '?'  # extra['messages']  # XXX: this is all messages
            status = ('%4.1f%%  (obs: %4d/%s);  %5.1f fps' % 
                   (progress, cur_obs, num_obs, tracker.fps()))
            logger.debug(status)
        yield topic, msg, t, extra


@contract(topics='list(str)')
def _read_bag_stats(bagfile, topics, logger=None):
    """ 
        This yields a dict with: 
        
            topic
            msg
            t
            
            info:
                counter
                messages

                start
                end
                t_percentage
                t_from_start
        
    """
    from rospy import rostime
    import rosbag

    if logger is None:
        logger = main_logger
        
    logger.debug('Reading info for bagfile...')
    bag_info = _rosbag_info(bagfile)
    logger.debug('Opening bagfile...')
    bag = rosbag.Bag(bagfile)

    extra = bag_info
    extra['messages'] = bag_info['messages']
    extra['start'] = bag_info['start']
    extra['end'] = bag_info['end']
    extra['duration'] = bag_info['duration']
    t0 = rostime.Time.from_sec(bag_info['start'])
    i = 0
    for topic, msg, t in bag.read_messages(topics=topics):
        if i == 0:
            logger.debug('first message arrived.')
        extra['counter'] = i
        extra['t_from_start'] = (t - t0).to_sec()
        extra['t_percentage'] = 100.0 * (extra['t_from_start'] / extra['duration'])  
        i += 1
        yield topic, msg, t, extra
       
