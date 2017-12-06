from bs4 import BeautifulSoup
import os


def getOptions(options):
    dv = []
    nameList = []
    for option in options:
        attr = option.attrs
        try:
            attr['selected']

        except KeyError:
            v = attr['value']
            name = option.text
            dv.append(int(v))
            nameList.append(name)
    return (dv,nameList)

def getPartDetail(rows):
    psno_list = []
    psname_list = []
    for row in rows:
        tds = row.find_all('td')
        try:
            psno = tds[0].text
            psname = tds[2].text
            psaddress = tds[4].text
            psno_list.append(int(psno))
            psname_list.append(psname + " " + psaddress)
        except IndexError:
            print("")
    return (psno_list,psname_list)

def getPayload(soupObj):
    ##Read and init the keys
    inputs = soupObj.find_all('input')

    payload = {}
    payload['__EVENTTARGET'] = ''
    payload['__EVENTARGUMENT'] = ''
    payload['__LASTFOCUS'] = ''
    payload['__VIEWSTATE'] = ''
    payload['__VIEWSTATEGENERATOR'] = ''
    payload['__EVENTVALIDATION'] = ''
    payload['ctl00$ContentPlaceHolder1$ddlDistrict'] = ''
    payload['ctl00$ContentPlaceHolder1$ddlAssembly'] = ''

    for input in inputs:
        attr = input.attrs
        try:
            payload[attr['name']] = attr['value']
        except KeyError:
            payload[attr['name']] = ''

    return payload

def printValueName(valueList,nameList):
    for i in range(0,len(valueList)):
        print(valueList[i],nameList[i])

def getInputDistrict(dv,namelist):
    print("")
    printValueName(dv,namelist)
    print("")
    while True:
        l = input("Please input code for District :  ")
        try:
            d = int(l)
            if d > 0 and d < 10:
                district_value = "0" + str(d)
                break
            elif d in dv:
                district_value = str(d)
                break
            else:
                print("Please input", min(dv), "to", max(dv), "only")
        except ValueError:
            print("Pleas input only digits")
    return district_value


def getInputAssembaly(av,nameList):
    print("")
    printValueName(av,nameList)
    print("")
    while True:
        l = input("Please input code for Assebly :  ")
        try:
            d = int(l)
            if d in av:
                asmb_value = str(d)
                break
            else:
                print("Please input", min(av), "to", max(av), "only")
        except ValueError:
            print("Pleas input only digits")
    return asmb_value

def getInputPart(psno_list,psname_list):
    print("")
    printValueName(psno_list,psname_list)
    print("")
    while True:
        l = input("Please input code for PartNo or -1 for all : ")
        try:
            d = int(l)
            if d in psno_list:
                asmb_value = d
                break
            else:
                print("Please input", min(psno_list), "to", max(psno_list), "only")
        except ValueError:
            print("Pleas input only digits")
    return asmb_value

def printDownloadInfo(part_no,assembly_value,district_value):
    print("------------------------------------")
    print("Downloading district",district_value," assembly",assembly_value," Part no ",part_no)


def downloadPdf(part_no,assembly_value,district_value,session):
    printDownloadInfo(part_no,assembly_value,district_value)
    pdf_url = "http://ceomadhyapradesh.nic.in/ViewVoterListSR2017.aspx?partno=" + part_no
    r = session.get(pdf_url)

    path = os.path.join('data', 'pdfs', district_value, assembly_value)
    if not os.path.exists(path):
        os.makedirs(path)

    file = os.path.join(path, part_no + '.pdf')

    with open(file, 'wb+') as f:
        f.write(r.content)