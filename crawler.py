#!/usr/bin/python
import requests
from bs4 import BeautifulSoup

import json

base_url =      'https://www.metal-archives.com'

band_page =         base_url + '/band/view/id/{id}'
read_more_page =    base_url + '/band/read-more/id/{id}'
discography_page =  base_url + '/band/discography/id/{id}/tab/all'
band_links_page =   base_url + '/link/ajax-list/type/band/id/{id}'

album_page =        base_url + '/albums/view/id/{id}'

label_page =        base_url + '/label/view/id/{id}'

headers = {'User-Agent':''}

def fetch_band(id,update=False):
    if update:
        # Check if band already exists
        # if not create band
        pass
    band = {"ma_id":id}
    source = requests.get(band_page.format(id=id),headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    name_and_link = soup.find('h1',class_='band_name').find('a')
    band.update({'ma_link':name_and_link['href']})
    band.update({'name':name_and_link.getText()})

    band_stats = soup.find(id='band_stats').find_all('dd')
    band.update({'country':     sanitise_text(band_stats[0].getText())})
    band.update({'location':    sanitise_text(band_stats[1].getText())})
    band.update({'status':      sanitise_text(band_stats[2].getText())})
    band.update({'formed':      sanitise_text(band_stats[3].getText())})
    band.update({'genre':       sanitise_text(band_stats[4].getText())})
    band.update({'themes':      sanitise_text(band_stats[5].getText())})
    band.update({'years_active':sanitise_text(str(band_stats[7]).replace(' ','').replace('ahref','a href'))[4:-5]})

    if band_stats[6].find('a'):
        band.update({'last_label':fetch_label(band_stats[6].find('a')['href']
                                                       .split('/')[-1])})
    else:
        band.update({'last_label': sanitise_text(band_stats[6].getText())})

    # Fetch Band members
    band.update({'members':[]})

    for member in soup.find('div',class_='ui-tabs-panel-content').find_all('tr'):
        status = None
        if member['class'][0] == 'lineupHeaders':
            status = sanitise_text(member.getText())
        elif member['class'][0] == 'lineupRow':
            person = fetch_person(member.find_all('td')[0].find('a')['href'].split('/')[-1])
            text = sanitise_text(member.find_all('td')[1].getText())
            positiones = []
            in_brackets = False
            last_pointer = 0
            temp_position = ''
            for index,c in enumerate(text):
                if in_brackets:
                    if c == ')':
                        for position in temp_position.split(','):
                            for time in text[last_pointer:index].replace('(','').replace(')','').split(','):
                                timespan = time.split('-')
                                started = timespan[0]
                                if len(timespan) == 2:
                                    if timespan[1] == 'present':
                                        ended = None
                                    else:
                                        ended = timespan[1]
                                else:
                                    ended = timespan[0]
                                band['members'].append({
                                    'person':person,
                                    'position':position,
                                    'started':started,
                                    'ended':ended,
                                    'status':status
                                    })
                        temp_position = ''
                        last_pointer = index
                        in_brackets = False
                elif c == '(' and (text[index+1].isdigit() or text[index+1] == '?'):
                    temp_position = text[last_pointer:index].replace('),','')
                    last_pointer = index
                    in_brackets = True
            if last_pointer+1 < len(text):
                band['members'].append({
                                'person':person,
                                'position':text[last_pointer:],
                                'started':None,
                                'ended':None,
                                'status':status})

    band.update({'description':requests.get(read_more_page.format(id=id),headers=headers).text})

    # Fetch band Links
    source = requests.get(band_links_page.format(id=id),headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    band.update({'links':[]})

    for link in soup.find_all('a'):
        # if url starts with a '#' It isn't a proper link(used by the website as internal link)
        if link['href'][0] != '#':
            band['links'].append({'url':link['href'],
                                  'display_name':link.getText()})

    # Fetch discography
    source = requests.get(discography_page.format(id=id),headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    entrys = soup.find('tbody').find_all('tr')
    band.update({'albums':[]})
    # checks if albums are present, if not text with em tag is displayed
    if not entrys[0].find('em'):
        for entry in entrys:
            band['albums'].append(fetch_album(entry.find('a')['href'].split('/')[-1]))

    print(json.dumps(band, indent = 4))

def fetch_label(id,update=False):
    if update:
        # Check if label already exists
        # if not create label
        pass

    return id

def fetch_person(id,update=False):
    if update:
        # Check if person already exists
        # if not create person
        pass
    return id

def fetch_album(id,update=False):
    if update:
        # Check if album already exists
        # if not create album
        pass
    return id

def sanitise_text(str):
    str = str.replace("\t", "") .replace("\n", "").replace(u'\xa0', u'')
    if str == 'N/A':
        str = None
    return str



if __name__ == '__main__':
    fetch_band(3540429294)
    #fetch_band(75044)
