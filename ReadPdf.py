import PyPDF2
import re




#print str


def extractEPIC(line):
    re_new = re.compile("[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")
    re_old = re.compile("MP/[0-9][0-9]/[0-9][0-9][0-9]/[0-9][0-9][0-9][0-9][0-9][0-9]")
    epic = ''
    m = re_new.search(line)
    if m:
        epic = m.group()
        return epic
    else:
        m_o = re_old.search(line)
        if m_o:
            epic = m_o.group()
            return epic
        else:
            return None


def saveEpic(file_path,district,cur):
    file = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    nop = pdfReader.numPages
    for i in range(0, nop):
        cp = pdfReader.getPage(i)
        str = cp.extractText()
        for line in iter(str.splitlines()):
            epic = extractEPIC(line)
            if epic is not None:
                print(epic)
                sql_check = "select * from `epic_data` where `epic_no`='"+epic+"' and `queried`=1"
                cur.execute(sql_check)
                try:
                    a = cur.fetchone()
                    if a == None:
                        sql_insert = "INSERT INTO `epic_data` ( `epic_no`, `district`) VALUES ( '" + epic + "', '" + district + "')"
                        cur.execute(sql_insert)

                except:
                    pass


