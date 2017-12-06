import requests
import helpers
from bs4 import BeautifulSoup

def searchEPIC(district,epicno):
    search_home = "http://164.100.196.163/searchengine/searchen.aspx"
    s_session = requests.Session()

    s_home = s_session.get(search_home)

    s_soup = BeautifulSoup(s_home.text, 'html.parser')
    payload = helpers.getPayload(s_soup)

    payload['SearchType'] = 'rbSearchDistrict'
    payload['__EVENTTARGET'] = 'ddlDistricts'
    payload['ddlDistricts'] = district

    ep_r = s_session.post(search_home, data=payload)
    ep_soup = BeautifulSoup(ep_r.text, 'html.parser')

    ep_payload = helpers.getPayload(ep_soup)

    ep_payload['search'] = 'rbtn_EPIC'
    ep_payload['txtEPICNo'] = epicno
    ep_payload['btnSearch'] = 'Search'
    ep_payload['ddlDistricts'] = '34'
    ep_payload['SearchType'] = 'rbSearchDistrict'

    final_r = s_session.post(search_home, data=ep_payload)
    final_soup = BeautifulSoup(final_r.text, 'html.parser')
    lbl_note = final_soup.find(id='lblNote').text
    if lbl_note != 'No Match Found : (':
        result_table = final_soup.find(id='gvSearchResult')
        tds = result_table.find_all('td')
        try:
            ac_no = tds[0].text
            part_no = tds[1].text
            section_no = tds[2].text
            serial_no = tds[3].text
            house_no = tds[4].text
            electors_name = tds[5].text
            electors_name_hindi = tds[6].text
            relatives_name = tds[7].text
            relatives_name_hindi = tds[8].text
            dob = tds[9].text
            age = tds[10].text
            gender = tds[11].text
            epic_no = tds[12].text
            print(epic_no,electors_name_hindi)

            sql_update = "UPDATE `epic_data` SET `queried` = 1, `ac_no` = '"+ac_no+"', `part_no` = '"+part_no+"', `section_no` = '"+section_no+"', `serial_no` = '"+serial_no+"', `house_no` = '"+house_no+"', `electors_name` = '"+electors_name+"', `electors_name_hindi` = '"+electors_name_hindi+"', `relatives_name` = '"+relatives_name+"', `relatives_name_hindi` = '"+relatives_name_hindi+"', `dob` = '"+dob+"', `age` = '"+age+"', `gender` = '"+gender+"' WHERE `epic_data`.`epic_no` = '"+epic_no+"' "

            return sql_update
        except IndexError:
            print("")
            return None
    return None


def updateEPICData(cur,cur2,db2):
    sql_fetch = "select epic_no,district from epic_data where queried = 0 and district='34'";
    cur.execute(sql_fetch)
    noOfRows = cur.rowcount
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            epic_no = row[0]
            district = row[1]
            sql_update = searchEPIC(district, epic_no)
            if sql_update is not None:
                cur2.execute(sql_update)
                db2.commit()







