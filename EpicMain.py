import os,errno
import requests
import helpers
from bs4 import BeautifulSoup

home_url = 'http://ceomadhyapradesh.nic.in/VoterlistSR2017.aspx'
session = requests.Session()
main_page = session.get(home_url)

soup = BeautifulSoup(main_page.text,'html.parser')

options = soup.find_all('option')
(dv,nameList) = helpers.getOptions(options)

##get district value using helper function
district_value = helpers.getInputDistrict(dv,nameList)
assembly_value = '-1'

payload = helpers.getPayload(soup)
payload['__EVENTTARGET'] = 'ctl00_ContentPlaceHolder1_ddlDistrict'
payload['ctl00$ContentPlaceHolder1$ddlDistrict'] = district_value
payload['ctl00$ContentPlaceHolder1$ddlAssembly'] = assembly_value


choose_assembly = session.post(home_url,data=payload)

soup_asmb = BeautifulSoup(choose_assembly.text,'html.parser')
select_asmb = soup_asmb.find(id='ctl00_ContentPlaceHolder1_ddlAssembly')
options_asmb = select_asmb.find_all('option')
(valList_asm,nameList_asm) = helpers.getOptions(options_asmb)

assembly_value = helpers.getInputAssembaly(valList_asm,nameList_asm)

payload_asmb = helpers.getPayload(soup_asmb)
payload_asmb['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$ddlAssembly'
payload_asmb['ctl00$ContentPlaceHolder1$ddlDistrict'] = district_value
payload_asmb['ctl00$ContentPlaceHolder1$ddlAssembly'] = assembly_value

asmblies = session.post(home_url,payload_asmb)
soup_asmblies = BeautifulSoup(asmblies.text,'html.parser')
table  = soup_asmblies.find(id='ctl00_ContentPlaceHolder1_GridView4')
rows = table.find_all('tr')
(psno_list,psname_list) = helpers.getPartDetail(rows)

part_no = helpers.getInputPart(psno_list,psname_list)
if part_no == -1 :
    ##download all part
    for part in psno_list:
        helpers.downloadPdf(str(part),assembly_value,district_value,session)
else:
    helpers.downloadPdf(str(part_no),assembly_value,district_value,session)

pdf_path = os.path.join('data','pdfs')
districts = os.listdir(pdf_path)
for district in districts:
    




