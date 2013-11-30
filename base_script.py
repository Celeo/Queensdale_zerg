import sys
import urllib2
import json
from time import sleep

def get_all_current_events():
    ret = [x for x in json.loads(urllib2.urlopen('https://api.guildwars2.com/v1/events.json?world_id=1021&map_id=15&lang=en').read())['events']]
    return ret

def is_zerg_event(event_id):
    return event_id in zerg_events

def get_short_name(event_id):
    if event_id == troll_event:
        return 'Troll'
    elif event_id == boar_event:
        return 'Boar'
    elif event_id == oak_event:
        return 'Oak'
    elif event_id == bandit_event:
        return 'Bandit'
    elif event_id == spider_event:
        return 'Spider'
    elif event_id == wasp_event:
        return 'Wasp'
    else:
        return '-ERROR-'

troll_event = 'D17D47E9-0A87-4189-B02A-54E23AA91A82'
boar_event = '69D031A8-7AD2-4419-B564-48457841A57C'
oak_event = '04084490-0117-4D56-8D67-C4FFFE933C0C'
bandit_event = 'BC997F15-4C05-4D95-A14F-9B7C4CF41B4E'
spider_event = 'BA9A0595-28BC-4B60-965D-F1EF94B6068A' # don't know if it's this one - spider doesn't show event!
wasp_event = '3C3915FB-E2E4-4794-A700-E3B5FCFE0404'
zerg_events = [troll_event, boar_event, oak_event, bandit_event, spider_event, wasp_event]

def check():
    current_events = get_all_current_events()
    for event in current_events:
        if is_zerg_event(event['event_id']):
            if event['state'] in ['Preparation', 'Warmup', 'Active']:
                print '{} - {}'.format(get_short_name(event['event_id']), event['state'])

while True:
    check()
    print ''
    for i in range(101):
        sleep(0.3)
        print '\r[{0}] {1}%'.format('#'*(i/10), i),
    print '\n--------------------------\n'

sys.exit()