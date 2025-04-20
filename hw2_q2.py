from enum import Enum
from collections import namedtuple
from itertools import zip_longest

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))

# Direct maps for one‑step transitions (CURE maps to itself)
IMPROVE = {
    Condition.SICK:   Condition.HEALTHY,
    Condition.DYING:  Condition.SICK,
    Condition.CURE:   Condition.CURE,
}
WORSEN  = {
    Condition.SICK:   Condition.DYING,
    Condition.DYING:  Condition.DEAD,
    Condition.CURE:   Condition.CURE,
}

def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    # 1) Extract those who never meet
    no_meet = [ag for ag in agent_listing
               if ag.category in (Condition.HEALTHY, Condition.DEAD)]

    # 2) Those who do meet
    meeters = [ag for ag in agent_listing
               if ag.category not in (Condition.HEALTHY, Condition.DEAD)]

    result = no_meet.copy()

    # 3) Pair up (odd one stays solo)
    for a, b in zip_longest(meeters[0::2], meeters[1::2], fillvalue=None):
        if b is None:
            result.append(a)
            continue

        # Cure vs non‑cure
        if a.category is Condition.CURE and b.category is not Condition.CURE:
            result.extend([a, Agent(b.name, IMPROVE[b.category])])
        elif b.category is Condition.CURE and a.category is not Condition.CURE:
            result.extend([Agent(a.name, IMPROVE[a.category]), b])

        # Both cures => no change
        elif a.category is Condition.CURE and b.category is Condition.CURE:
            result.extend([a, b])

        # Both non‑cures => both worsen
        else:
            result.extend([
                Agent(a.name, WORSEN[a.category]),
                Agent(b.name, WORSEN[b.category])
            ])

    return result

