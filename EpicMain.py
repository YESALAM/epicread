import ReadPdf
import searchepic
import db_conn
import downloadPdfs

db = db_conn.getConnection()
cur = db_conn.getCursor(db)

db2 = db_conn.getConnection()
cur2 = db_conn.getCursor(db2)

downloadPdfs.download()

ReadPdf.readPdfs(cur,db)

searchepic.updateEPICData(cur,cur2,db2)

