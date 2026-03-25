# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:26:26 2026

@author: trent
"""

#
from pathlib import Path
import warnings
from threading import Thread
import zipfile
import typing
from types import MappingProxyType

import requests
from rapidfuzz import process

from glyphloom.generation import SpellData

#%% 5e.Tools Mirror
try:
    URL = r'https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/main/data/spells'
    SPELLS_BY_SOURCE = {}
    SOURCE_BY_SPELL = {}
    SOURCES = requests.get(f"{URL}/index.json").json()
    def get_spell_map(source:str, file:str) -> None:
        file = f'{URL}/{file}'
        data = requests.get(file).json()
        spell_names = [spell['name'] for spell in data['spell']]
        SPELLS_BY_SOURCE[source] = tuple(spell_names)
        return
    threads = []
    for source, file in SOURCES.items():
        thread = Thread(target=get_spell_map, args=(source,file))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    
    
    SOURCE_BY_SPELL = {spell: 'XPHB' for spell in SPELLS_BY_SOURCE['XPHB']}
    for source, spells in reversed(SPELLS_BY_SOURCE.items()):
        if source == 'PHB':
            continue
        for spell in spells:
            if spell in set(SOURCE_BY_SPELL):
                continue
            SOURCE_BY_SPELL[spell] = source
    del threads, thread, source, file, spell, spells
except Exception as e:
    print(f"{type(e)}: {e}")
    warnings.warn("No access to the 5e.tools Mirror Repo!")
    SOURCES = None
    


#%% Data
FIVE_E = Path(__file__).absolute().parent
SpellData_5e = SpellData.from_yaml(
    (FIVE_E / 'fifth_edition.yaml'))

OFFLINE_LIBRARY = {}
def get_offline_map(file:typing.IO[str]) -> None:
    data = SpellData_5e.yaml_spell(file)
    OFFLINE_LIBRARY[data.name] = data
    return
threads = []
with zipfile.ZipFile(FIVE_E / "library.zip") as zf:
    for file_info in zf.filelist:
        t = Thread(target=get_offline_map, args=(zf.open(file_info),))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
del zf, t, threads

#%% Monkey Type

AOE_MAP = MappingProxyType({
        "C" : "Cube",
        "E" : "Emanation",
        "H" : "Hemisphere",
        "L" : "Line",
        "MT" : "Multiple Targets",
        "N" : "Cone",
        "Q" : "Square",
        "R" : "Circle",
        "S" : "Sphere",
        "ST" : "Single Target",
        "W" : "Wall",
        "Y" : "Cylinder"
    })
def _get_spell_json_online(spell_name:str, source:str = None) -> SpellData_5e:
    """
    Utilizes the 5etools-mirror-3 repo to load in a spell to the SpellData_5e 
    type

    Parameters
    ----------
    spell_name : str
        Spell name as it appears in the compendium.

    Returns
    -------
    SpellData_5e

    """
    lower, conf, idx = process.extractOne(spell_name.lower(),
                                          map(str.lower, SOURCE_BY_SPELL))
    spell_name = tuple(SOURCE_BY_SPELL)[idx]
    if source is None:
        file = SOURCES[SOURCE_BY_SPELL[spell_name]]
    else:
        file = SOURCES[source]
    url = f'{URL}/{file}'
    data = requests.get(url).json()
    
    spell = max(data['spell'],
                key=lambda sp: sp['name'] == spell_name)
    
    level = spell['level']
    school = max(SpellData_5e.school.options,
                 key=lambda s : s[0] == spell['school'])
    
    damage_type = list(map(str.capitalize, spell.get('damageInflict', [])))
    if len(damage_type) == 1:
        damage_type = damage_type[0]
    elif len(damage_type) > 1:
        damage_type = tuple(sorted(damage_type))
    if not damage_type:
        damage_type = 'None'
    
    aoe_shape = spell.get('areaTags', [])
    aoe_shape = list(map(lambda s : AOE_MAP[s],
                         aoe_shape))
    if len(aoe_shape) == 1:
        aoe_shape = aoe_shape[0]
    elif len(aoe_shape) > 1:
        aoe_shape = tuple(sorted(aoe_shape))
    if not aoe_shape:
        aoe_shape = 'None'
    
    rg = spell['range']
    tp = rg['type']
    if 'distance' in rg:
        if 'amount' in rg['distance']:
            am = rg['distance']['amount']
            unit = rg['distance']['type']
            if am != tp:
                rg = f"{rg['type']} ({am} {unit})"
            else:
                rg = 'point (None)'
        else:
            second = rg['distance']['type'].capitalize()
            first = rg['type']
            rg = f'{first} ({second})'
            # types[tp].add(rg['type'])
    else:
        rg = 'special (Special)'    
            
    duration = spell['duration']
    if len(duration) > 1:
        if duration[0]['type'] == 'instant':
            duration = duration[1]
    else:
        duration = duration[0]
    if duration['type'] == 'timed':
        timing = f'({duration["duration"]["amount"]} {duration["duration"]["type"]})'
        if duration.get('concentration', False):
            duration = f'concentration {timing}'
        else:
            duration = f'timed {timing}'
    elif 'amount' in duration:
        duration = f'timed ({duration["amount"]} {duration["type"]})'
    else:
        duration = f'special ({duration["type"].capitalize()})'
    
    #Ritual
    meta = spell.get('meta', {})
    ritual = False
    if 'ritual' in meta:
        ritual = meta['ritual']
    
    spell_data = {'name' : spell_name,
                  'system': '5e',
                  'level' : level,
                  'school' : school,
                  'damage_type' : damage_type,
                  'area_of_effect' : aoe_shape,
                  'range' : rg,
                  'duration' : duration,
                  'ritual' : ritual}
    for key, value in spell_data.items():
        if value is None:
            spell_data[key] = 'None'
    
    return spell_data
    
    


__SPELL_CACHE = {}

@classmethod
def get_spell(cls, 
              spell_name: str,
              source: str = 'offline') -> SpellData_5e:
    """
    Retrieves a spell from 5eTools using 5.5e PHB, Tasha's, and Xanathar's.
    Spells err on the side of the player's handbook, so if you want the spell
    from a different book, use the source argument with 'xge', 'tce', or the
    last part of the "spells-*.json" data file name from 5e.toosl.data/spells.

    Parameters
    ----------
    spell_name : str
        Name exactly as it appears on 5eTools.
    source: str
        Override command to grab a different book's spells, literal "offline"
        will use the preloaded spells in the library

    Returns
    -------
    SpellData_5e
        Spell Data for the retrieved spell.

    """
    
    if source == 'offline':
        choices = list(OFFLINE_LIBRARY)
        lower, conf, idx = process.extractOne(spell_name.lower(), map(str.lower,choices))
        return tuple(OFFLINE_LIBRARY.values())[idx]
    
    
    if source == 'online' or source is None:
        spell_data_dict = _get_spell_json_online(spell_name)
    elif source:
        spell_data_dict = _get_spell_json_online(spell_name, source)
    
    spell = cls(**spell_data_dict)
    
    return spell
setattr(SpellData_5e, 'get_spell', get_spell)

