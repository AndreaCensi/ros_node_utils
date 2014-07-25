from .rosbag_info_stats import rosbag_info_cached
from .utils import InAWhile
from contracts import contract
from rosbag_utils import logger as main_logger
   
__all__ = ['read_bag_stats', 'read_bag_stats_progress']

def read_bag_stats_progress(source, logger, interval=5):
    """ This is a wrapper for read_bag_stats that visualizes some statistics. """ 
    tracker = InAWhile(interval)
    
    for topic, msg, t, extra in source:
        if tracker.its_time():
            progress = extra['t_percentage']
            cur_obs = extra['counter']
            num_obs = '?'  # extra['messages']  # XXX: this is all messages
            status = ('%4.1f%% %5.2f sec (obs: %4d/%s);  %5.1f fps' %
                   (progress, extra['t_from_start'], cur_obs, num_obs, tracker.fps()))
            logger.debug(status)
        yield topic, msg, t, extra


@contract(topics='list(str)')
def read_bag_stats(bagfile, topics,
                   logger=None, start_time=None, stop_time=None):
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
    from rospy import rostime  # @UnresolvedImport

    import rosbag  # @UnresolvedImport

    if logger is None:
        logger = main_logger
        
    logger.debug('Reading info for bagfile...')
    bag_info = rosbag_info_cached(bagfile)
    logger.debug('Opening bagfile...')
    bag = rosbag.Bag(bagfile)

    if start_time is None:
        start_time = bag_info['start']
    if stop_time is None:
        stop_time = bag_info['end']
            
    extra = bag_info
    extra['messages'] = bag_info['messages']
    extra['start'] = start_time
    extra['end'] = stop_time
    extra['duration'] = stop_time - start_time
    t0 = rostime.Time.from_sec(bag_info['start'])
    
    start_time = rostime.Time.from_sec(start_time)
    stop_time = rostime.Time.from_sec(stop_time)
    
    i = 0
    messages = bag.read_messages(topics=topics, start_time=start_time, end_time=stop_time)
    for topic, msg, t in messages:
        if i == 0:
            logger.debug('first message arrived.')
        extra['counter'] = i
        extra['t_from_start'] = (t - t0).to_sec()
        extra['t_percentage'] = 100.0 * (extra['t_from_start'] / extra['duration'])  
        i += 1
        yield topic, msg, t, extra
       
