# check_pairs.py
import json
with open('data/concept_pairs.json', 'r') as f:
    data = json.load(f)
for domain, pairs in data.items():
    print(f'\n{domain}:')
    for p in pairs:
        print(f'  {p["id"]}: {p["term_a"]} vs {p["term_b"]}')