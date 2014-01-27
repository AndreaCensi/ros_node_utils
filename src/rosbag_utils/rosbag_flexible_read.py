from conf_tools.utils import raise_x_not_found
from conf_tools.utils.wildcards import get_wildcard_matches
from contracts import contract
import warnings

__all__ = ['resolve_topics', 'topics_in_bag']

@contract(known='list(str)', topics='list(str)',
          returns='tuple(list(str),dict(str:str),dict(str:str))')
def resolve_topics(known, topics, soft=True):
    """
        Given a list of topic names, which could contain "*"
        
        return res, resolved2asked, asked2resolved

    """ 
    
    res = []
    for t in topics:
        matches = list(get_wildcard_matches(t, known))
        if not matches:
            if soft:
                warnings.warn('make this better')
                print('warning, no match for %r' % t)
                res.append(t)
                continue
            else:
                raise_x_not_found('topic', t, known)
        if len(matches) >= 2:
            msg = 'Too many matches for %s: %s' % (t, matches)
            raise ValueError(msg)
        res.append(matches[0])
    
    asked2resolved = {}
    resolved2asked = {}
    for a, t in zip(topics, res):
        resolved2asked[t] = a
        asked2resolved[a] = t 
        
    return res, resolved2asked, asked2resolved
    
    
@contract(returns='list(str)')
def topics_in_bag(baginfo):
    return [t['topic'] for t in baginfo['topics']]
