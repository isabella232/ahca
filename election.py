import csv
import os
import requests

states = []
BASE_URL = 'https://apps.npr.org/elections16/data/presidential-{0}-counties.json'
election_data = []

def get_states():
    for filename in os.listdir('data/census'):
        state = filename.split('-')[0]
        states.append(state)

def process_data():
    for state in states:
        r = requests.get(BASE_URL.format(state))
        response = r.json()
        results = response['results']
        for fips, data in results.items():
            if fips == 'state':
                continue

            output = {
                'FIPS': fips
            }

            for candidate in data:
                last_name = candidate['last'].lower()
                output['{0}_votecount'.format(last_name)] = candidate['votecount']

            election_data.append(output)

def write_csv():
    with open('data/elex.csv', 'w') as f:
        fieldnames = ['FIPS', 'trump_votecount', 'clinton_votecount', 'johnson_votecount', 'stein_votecount', 'mcmullin_votecount', 'other_votecount']
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval=0, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()

        for row in election_data:
            writer.writerow(row)


if __name__ == '__main__':
    get_states()
    process_data()
    write_csv()