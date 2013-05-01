from contracts import contract
from conf_tools.utils.wildcards import get_wildcard_matches
from conf_tools.utils.not_found import raise_x_not_found


@contract(baginfo='dict', topics='list(str)', returns='list(str)')
def _resolve_topics(baginfo, topics):
    """
        Given a list of topic names, which could contain "*"
        
    """ 
    
    known_topics = [t['topic'] for t in baginfo['topics']]
    
    res = []
    for t in topics:
        matches = list(get_wildcard_matches(t, known_topics))
        if not matches:
            raise_x_not_found('topic', t, known_topics)
        if len(matches) >= 2:
            msg = 'Too many matches for %s: %s' % (t, matches)
            raise ValueError(msg)
        res.append(matches[0])
    return res
    
    
    
    
