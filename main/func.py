import re, requests, bisect
from ids import *
from keys import *

def trn_api_stats(Origin_id):
    try:
        header = {'TRN-Api-Key': trn_token}
        r = requests.get(trn_url + 'origin/' + Origin_id + '/', headers= header)
        player_data = r.json()
        stats = player_data['data']['segments'][0]['stats']

    except requests.exceptions.RequestException as e:
        print(e)
        return False
    except KeyError as e:
        print(e)
        return False
    else:
        return player_data, stats