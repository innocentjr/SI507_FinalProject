from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


indicator = ['Project', 'Opportunity', 'Legislation']
filename = ['Project.json', 'Opportunity.json', 'Legislation.json']
base_url1 = 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aproject&sort=recent'
base_url2 = 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aopportunity&sort=recent'
base_url3 = 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aresource&sort=recent'


def grabPage(base_url, filename, indicator):
    driver = webdriver.Chrome()
    driver.get(base_url);
    html = driver.page_source

    bsObj = BeautifulSoup(html, "html.parser")
    bsObj2 = bsObj.prettify()

    title_list = bsObj.find('ul', "listings__list" )
    title_listttwo = title_list.find_all("a", {"class":"teaser__link"})
    activity = title_list.find_all("div", {"class":"teaser--activity"})
    location_list = title_list.find_all('ul', {"class":"related-list--locations"})
    pretty = title_list.prettify()

    Tag = []
    Link = []
    Title = []
    Address = []
    projects = {}

    #Get project title_list
    for each in title_listttwo:
        entry = each.h2.get_text()
        Title.append(entry)
        projects[entry] = {}
        dic = projects[entry]
        dic['Name'] = entry
        dic['Activity'] = indicator

    #Get the Theme or Tag
    for each in title_listttwo:
        title = each.h2.get_text()
        entry = each.find('span', {"class":"teaser__tag"}).get_text()
        #print(entry)
        Tag.append(entry)
        dic = projects[title]
        dic['Tag'] = entry

    #Get the teaser__link
    for each in title_listttwo:
        title = each.h2.get_text()
        entry = each.get('href')
        #print(entry)
        Link.append(entry)
        dic = projects[title]
        dic['Link'] = entry

    for each in activity:
        name = each.h2.get_text()
        address = each.find('ul', {"class":"related-list--locations"}).find_all('a')
        addresses = []
        for each in address:
            temp = each.get_text().strip()
            addresses.append(temp)
        address = '; '.join(map(str, addresses))
        Address.append(address)
        dic = projects[name]
        dic['Address'] = address

    with open(filename, 'w', encoding='utf-8') as f:
        dumping = json.dumps(projects, indent = 4, sort_keys = True, separators=(',',':'))
        f.write(dumping)
        f.close()

    driver.quit()

def set_me_up():
    try:
        a = open(filename[0], 'r')
        a.close()
        b = open(filename[1], 'r')
        b.close()
        c = open(filename[2], 'r')
        c.close()
    except:
        grabPage(base_url2, filename[1], indicator[1])
        grabPage(base_url3, filename[2], indicator[2])
        grabPage(base_url1, filename[0], indicator[0])


    with open('Project.json', 'r') as f:
        proj = json.loads(f.read())
        f.close()

    with open('Opportunity.json', 'r') as f:
        opps = json.loads(f.read())
        f.close()

    with open('Legislation.json', 'r') as f:
        law = json.loads(f.read())
        f.close()
#comment
    z = {**proj, **law}
    a = {**z, **opps}

    with open('Master.json', 'w', encoding='utf-8') as f:
        dumping = json.dumps(a, indent = 4, sort_keys = True, separators=(',',':'))
        f.write(dumping)
        f.close()

    return True
