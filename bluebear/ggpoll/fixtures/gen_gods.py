#!/usr/bin/env python

import json

gods = [
    ('Janus', 'God of Transitions'),
    ('Jupiter', 'God of the Sky'),
    ('Saturn', 'God of Time'),
    ('Mercury', 'Messenger God'),
    ('Apollo', 'God of Light'),
    ('Mars', 'God of War'),
    ('Vulcan', 'God of the Forge'),
    ('Neptune', 'God of the Sea'),
    ('Sol', 'God of the Sun'),
    ('Orcus', 'God of the Underworld'),
    ('Liber', 'God of Viticulture'),
    ('Bacchus', 'God of Wine'),
    ('Tellus', 'Goddess of the Earth'),
    ('Ceres', 'Goddess of Grain'),
    ('Juno', 'Queen of the Gods'),
    ('Luna', 'Goddess of the Moon'),
    ('Diana', 'Goddess of the Hunt'),
    ('Minerva', 'Goddess of Wisdom'),
    ('Venus', 'Goddess of Love'),
    ('Vesta', 'Goddess of the Hearth'),
]

"""
[
{
    "model": "ggpoll.gggroup",
    "pk": 1,
    "fields": {
        "name": "Jupiter",
        "description": "King of the Gods"
    }
}
]
"""

data = []
x = 1
for god, desc in gods:
    entry = {}
    entry['model'] = 'ggpoll.gggroup'
    entry['pk'] = x
    x += 1
    fields = {}
    fields['name'] = god
    fields['description'] = desc
    entry['fields'] = fields
    data.append(entry)


print(json.dumps(data, indent=4))


