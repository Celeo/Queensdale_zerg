from django.shortcuts import render
from datetime import datetime, timedelta
import urllib2
import json

troll_event = 'D17D47E9-0A87-4189-B02A-54E23AA91A82'
boar_event = '69D031A8-7AD2-4419-B564-48457841A57C'
oak_event = '04084490-0117-4D56-8D67-C4FFFE933C0C'
bandit_event = 'BC997F15-4C05-4D95-A14F-9B7C4CF41B4E'
wasp_event = '3C3915FB-E2E4-4794-A700-E3B5FCFE0404'
sb_event = '31CEBA08-E44D-472F-81B0-7143D73797F5'
zerg_events = [troll_event, boar_event, oak_event, bandit_event, wasp_event, sb_event]

class Champion:
    def __init__(self, name='', event_id='', status='Unknown'):
        self.name = name
        self.event_id = event_id
        self.status = status
    def __repr__(self):
        return '%s: %s' % (self.name, self.status)
    def update_status(self, new_status):
        self.status = new_status
        last_updated = datetime.now()
    def is_active(self):
        return self.status == 'Active'

troll = Champion('Troll', troll_event)
boar = Champion('Boar', boar_event)
oak = Champion('Oak', oak_event)
bandit = Champion('Bandit', bandit_event)
wasp = Champion('Wasp', wasp_event)
shadow = Champion('SB', sb_event)
last_updated = None

def get_short_name(event_id):
    if event_id == troll_event:
        return 'Troll'
    elif event_id == boar_event:
        return 'Boar'
    elif event_id == oak_event:
        return 'Oak'
    elif event_id == bandit_event:
        return 'Bandit'
    elif event_id == wasp_event:
        return 'Wasp'
    elif event_id == sb_event:
        return 'SB'
    else:
        return '-ERROR-'

def should_update():
    global last_updated
    if last_updated == None:
        return True
    now = datetime.now()
    diff = now - last_updated
    return diff.seconds > 30

def update_all():
    global last_updated
    now = datetime.now()
    current_events = get_all_current_events()
    for event in current_events:
        if is_zerg_event(event['event_id']):
            update_event(get_short_name(event['event_id']), event['state'])
    last_updated = now

def update_event(name, state):
    if name == 'Troll':
        troll.update_status(state)
    elif name == 'Boar':
        boar.update_status(state)
    elif name == 'Oak':
        oak.update_status(state)
    elif name == 'Bandit':
        bandit.update_status(state)
    elif name == 'Wasp':
        wasp.update_status(state)
    elif name == 'SB':
        shadow.update_status(state)

def get_all_current_events():
    ret = [x for x in json.loads(urllib2.urlopen('https://api.guildwars2.com/v1/events.json?world_id=1021&map_id=15&lang=en').read())['events']]
    return ret

def is_zerg_event(event_id):
    return event_id in zerg_events

def index(request):
    return render(request, 'zerg/index.html')

def data(request):
    global last_updated
    if should_update():
        update_all()
    now = datetime.now()
    return render(request, 'zerg/data.html', {'last_updated': last_updated, 'now': now, 'troll': troll, 'boar': boar,
        'oak': oak, 'bandit': bandit, 'wasp': wasp, 'shadow': shadow})