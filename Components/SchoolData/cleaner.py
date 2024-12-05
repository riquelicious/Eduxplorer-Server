import json
from fuzzywuzzy import process, fuzz

def clean():
    with open('refelementary.json') as f:
        data = json.load(f)
        for school in data:
            school.pop('Distance', None)

    with open('refelementary.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
clean()
