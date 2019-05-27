#!/usr/bin/python
import requests
from bs4 import BeautifulSoup

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

    band.update({'country':     band_stats[0].getText()})
    band.update({'location':    band_stats[1].getText()})
    band.update({'status':      band_stats[2].getText()})
    band.update({'formed':      band_stats[3].getText()})
    band.update({'genre':       band_stats[4].getText()})
    band.update({'themes':      band_stats[5].getText()})
    band.update({'last_label':fetch_label(band_stats[6].find('a')['href']
                                                       .split('/')[-1])})

    band.update({'years_active':sanitise_text(band_stats[7].getText())})

    # Fetch Band members
    band.update({'members':[]})

    for member in soup.find('div',class_='ui-tabs-panel-content').find_all('tr',class_='lineupRow'):
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
                                'ended':ended
                                })
                    temp_position = ''
                    last_pointer = index
                    in_brackets = False
            elif c == '(' and text[index+1].isdigit():
                temp_position = text[last_pointer:index].replace('),','')
                last_pointer = index
                in_brackets = True
        if last_pointer+1 != len(text):
            band['members'].append({
                            'person':person,
                            'position':text,
                            'started':None,
                            'ended':None})

    band.update({'description':requests.get(read_more_page.format(id=id),headers=headers).text})

    # Fetch band Links
    source = requests.get(band_links_page.format(id=id),headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    band.update({'links':[]})

    for link in soup.find_all('a'):
        band['links'].append({'url':link['href'],
                              'display_name':link.getText()})

    # Fetch discography
    source = requests.get(discography_page.format(id=id),headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    entrys = soup.find('tbody').find_all('tr')
    band.update({'albums':[]})

    for entry in entrys:
        band['albums'].append(fetch_album(entry.find('a')['href'].split('/')[-1]))

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
    return str.replace(" ", "").replace("\t", "").replace("\n", "").replace(u'\xa0', u'')

if __name__ == '__main__':
    #fetch_band(1)
    fetch_band(81077)
    #crawl_band('https://www.metal-archives.com/bands/Craving/81077')
