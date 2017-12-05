import requests
import helpers
from bs4 import BeautifulSoup

search_home = "http://164.100.196.163/searchengine/searchen.aspx"
s_session = requests.Session()

s_home = s_session.get(search_home)

s_soup = BeautifulSoup(s_home.text,'html.parser')
payload = helpers.getPayload(s_soup)

payload['SearchType'] = 'rbSearchDistrict'
payload['__EVENTTARGET'] = 'ddlDistricts'
payload['ddlDistricts'] = '34'

ep_r = s_session.post(search_home,data=payload)
ep_soup = BeautifulSoup(ep_r.text,'html.parser')
ep_payload = helpers.getPayload(ep_soup)

ep_payload['search'] = 'rbtn_EPIC'
ep_payload['txtEPICNo'] = 'NMU1264910'
ep_payload['btnSearch'] = 'Search'

final_r = s_session.post(search_home,data=payload)
print(final_r.text)




