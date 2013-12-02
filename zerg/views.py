from django.shortcuts import render
from datetime import datetime
import urllib2
import json

# ===============================
#        Data setup
# ===============================

troll_event = 'D17D47E9-0A87-4189-B02A-54E23AA91A82'
boar_event = '69D031A8-7AD2-4419-B564-48457841A57C'
oak_event = '04084490-0117-4D56-8D67-C4FFFE933C0C'
bandit_event = 'BC997F15-4C05-4D95-A14F-9B7C4CF41B4E'
wasp_event = '3C3915FB-E2E4-4794-A700-E3B5FCFE0404'
sb_event = '31CEBA08-E44D-472F-81B0-7143D73797F5'
zerg_events = [troll_event, boar_event, oak_event, bandit_event, wasp_event, sb_event]

worlds = {}
for d in json.loads(urllib2.urlopen('https://api.guildwars2.com/v1/world_names.json?lang=en').read()):
    worlds[d['id']] = d['name']
world_names = [str(d).replace(' ', '_') for d in worlds.itervalues()]

class Champion:
    def __init__(self, name='', event_id='', status='Unknown'):
        self.name = name
        self.event_id = event_id
        self.status = status
    def __repr__(self):
        return '%s: %s' % (self.name, self.status)
    def update_status(self, new_status):
        self.status = new_status
    def is_active(self):
        return self.status == 'Active'

class World:
    def __init__(self, world_id, world_name, troll, boar, oak, bandit, wasp, shadow):
        self.id = world_id
        self.name = world_name
        self.troll = troll
        self.boar = boar
        self.oak = oak
        self.bandit = bandit
        self.wasp = wasp
        self.shadow = shadow
        self.last_updated = datetime.now()
    def get_champion_status(self, champion_name):
        if champion_name == 'troll':
            return self.troll.status
        elif champion_name == 'boar':
            return self.boar.status
        elif champion_name == 'oak':
            return self.oak.status
        elif champion_name == 'bandit':
            return self.bandit.status
        elif champion_name == 'wasp':
            return self.wasp.status
        elif champion_name == 'shadow':
            return self.shadow.status
    def try_update(self):
        if not last_updated or (datetime.now() - self.last_updated).seconds > 30:
            self._update()
    def _update(self):
        pass

# ===============================
#       Data use
# ===============================

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

def should_update():
    global last_updated
    if last_updated == None:
        return True
    now = datetime.now()
    diff = now - last_updated
    return diff.seconds > 30

def get_all_current_events(world_id):
    ret = [x for x in json.loads(urllib2.urlopen('https://api.guildwars2.com/v1/events.json?world_id=%s&map_id=15&lang=en' % world_id).read())['events']]
    return ret

def get_world_object(world_id):
    """ Retruns World class object matching the world_id """
    return None

def is_zerg_event(event_id):
    """ Returns True if event_id matches that of a zerg event """ 
    return event_id in zerg_events

# ===============================
#           Pages
# ===============================

def index(request):
    """ Index page - show list of worlds to choose """
    return render(request, 'zerg/world_choose.html', {'worlds': world_names})

def world(request, world_name):
    """ Base page for this world - load and continue to refresh that world's data """
    world_name = world_name.replace('_', ' ')
    world_id = -1
    for w_id, name in worlds.items():
        if name == world_name:
            world_id = w_id
    return render(request, 'zerg/index.html', {'world_name': world_name, 'world_id': world_id})

def data(request, world_id):
    """ Data page for loading via Javacsript - return render of all data for that world """
    world = get_world_object(world_id)
    world.try_update()
    return render(request, 'zerg/data.html', {'last_updated': last_updated, 'now': datetime.now(), 'world': world})
