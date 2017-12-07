import PyPDF2
import re
import os
import db_conn




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
    with open(file_path,'rb') as file:
        pdfReader = PyPDF2.PdfFileReader(file)
        nop = pdfReader.numPages
        for i in range(0, nop):
            cp = pdfReader.getPage(i)
            str = cp.extractText()
            for line in iter(str.splitlines()):
                epic = extractEPIC(line)
                if epic is not None:
                    print(epic)
                    sql_check = "select * from `epic_data` where `epic_no`='" + epic + "' and `queried`=1"
                    cur.execute(sql_check)
                    try:
                        a = cur.fetchone()
                        if a == None:
                            sql_insert = "INSERT INTO `epic_data` ( `epic_no`, `district`) VALUES ( '" + epic + "', '" + district + "')"
                            cur.execute(sql_insert)

                    except:
                        pass


def readPdfs(cur,db):
    pdf_path = os.path.join('data', 'pdfs')
    districts = os.listdir(pdf_path)
    cwd = os.getcwd()
    for district in districts:
        print(district.title())
        district_path = os.path.join(cwd, pdf_path, district.title())
        assemblies = os.listdir(district_path)
        for assembly in assemblies:
            print(assembly.title())
            assembly_path = os.path.join(district_path, assembly.title())
            parts = os.listdir(assembly_path)
            for part in parts:
                file_path = os.path.join(assembly_path, part.title().lower())
                if os.path.isfile(file_path):
                    saveEpic(file_path, district.title(), cur)
                    db.commit()
                    deletePdf(file_path)

def deletePdf(file_path):
    os.remove(file_path)


if __name__ == "__main__":
    db = db_conn.getConnection()
    cur = db_conn.getCursor(db)
    readPdfs(cur,db)