from zuper_commons.logs import ZLogger
from zuper_commons.types import ZKeyError, ZValueError

from conf_tools.utils.wildcards import get_wildcard_matches
from contracts import contract

logger = ZLogger(__name__)
# from . import logger

__all__ = [
    "resolve_topics",
    "topics_in_bag",
]


@contract(
    known="list(str)",
    topics="list(str)",
    returns="tuple(list(str),dict(str:str),dict(str:str))",
)
def resolve_topics(known, topics, soft=True):
    """
    Given a list of topic names, which could contain "*"

    return res, resolved2asked, asked2resolved

    """
    logger.info(f"known : {known}")
    logger.info(f"topics : {topics}")
    res = []
    for t in topics:
        matches = list(get_wildcard_matches(t, known))
        if not matches:
            if soft:

                logger.error("warning, no match for t = %r known = %r" % (t, known))
                res.append(t)
                continue
            else:
                raise ZKeyError("no topic foudnd", t=t, known=known)
                # raise_x_not_found('topic', t, known)
        if len(matches) >= 2:
            msg = "Too many matches"
            raise ZValueError(msg, t=t, matches=matches)
        res.append(matches[0])

    asked2resolved = {}
    resolved2asked = {}
    for a, t in zip(topics, res):
        resolved2asked[t] = a
        asked2resolved[a] = t

    return res, resolved2asked, asked2resolved


@contract(returns="list(str)")
def topics_in_bag(baginfo):
    return [t["topic"] for t in baginfo["topics"]]
