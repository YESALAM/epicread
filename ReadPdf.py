import PyPDF2
import re

file = open('S12A154P001.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(file)

nop = pdfReader.numPages

#print str
re_new = re.compile("[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")
re_old = re.compile("MP/[0-9][0-9]/[0-9][0-9][0-9]/[0-9][0-9][0-9][0-9][0-9][0-9]")



def extractEPIC(line):
    global re_new
    global re_old
    epic = ''
    m = re_new.search(line)
    if m:
        epic = m.group()
        return (True,epic)
    else:
        m_o = re_old.search(line)
        if m_o:
            epic = m_o.group()
            return (True,epic)
        else:
            return (False,'')


count = 0
for i in range(0,nop):
    cp = pdfReader.getPage(i)
    str = cp.extractText()
    for line in iter(str.splitlines()):
        (matched,epic) = extractEPIC(line)
        if matched:
            count = count + 1
            print(count,epic)