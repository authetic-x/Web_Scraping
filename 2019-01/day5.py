'''
Here we will learn some skills of encode and decode.
'''

from urllib.request import urlopen
from io import StringIO
from io import open
import csv


'''
textPage =  urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
print(str(textPage.read(), 'utf-8'))
'''

'''
data = urlopen("http://www.pythonscraping.com/files/MontyPythonAlbums.csv").read()
print(data)
print(data.decode('ascii', 'ignore'))
dataFile = StringIO(data.decode('ascii', 'ignore'))
csvReader = csv.reader(dataFile)
'''

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

'''
def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

pdfFile = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1.pdf")
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()
'''

from zipfile import ZipFile
from io import BytesIO

'''
wordFile = urlopen("http://www.pythonscraping.com/pages/AWordDocument.docx").read()
wordFile = BytesIO(wordFile)
document = ZipFile(wordFile)
xml_content = document.read('word/document.xml')
print(xml_content) # 会打印出字节数据  b''
print(xml_content.decode('utf-8'))
'''

