from xml.dom.minidom import Document
from pyvi import ViTokenizer, ViPosTagger
from underthesea import word_tokenize, sent_tokenize
import regex as re
from nlp import text_preprocess


# document = "Trường đại học khoa học tự nhiên"
# document = text_preprocess(document)
# for token in document:
#     print(token)

# result = ViTokenizer.tokenize(u"Trường đại học bách khoa hà nội")
# print(result)

#text = "cho tam giác ABC có góc A = 60 độ, góc C = 50 độ"
#text = "Tia phân giác góc B cắt AC ở D."
#result = word_tokenize(text, format='text')
#result = ViTokenizer.tokenize(text)

#print(result)

text = "[Cc]ho tam_giác ABC."
reg = re.compile(r'tam_giác.+([A-Z]{3})\b')
kq = reg.search(text).group(1)
print(kq)

text = "có góc A = 60 độ, góc C = 50 độ"
reg = re.compile(r'góc\s+([A-Z]{1,3})\s*=\s*(\d{2})\b')
kq = reg.findall(text)
for item in kq:
    print(item[0])
    print(item[1])

text = "Tia_phân giác  góc  B  cắt  AC  ở  D."
reg = re.compile(r'[Tt]ia_phân.+góc\s+([A-Z]{1,3})\s+cắt\s+([A-Z]{2})\s+ở\s+([A-Z]{1})')
kq = reg.search(text)
#print(kq)
print(kq.group(1))
print(kq.group(2))
print(kq.group(3))

# text = "Tính góc ADB, góc CDB"
# reg = re.compile(r'[Tt]ính.+')
# kq = reg.search(text).group()
# print(kq)

# text = "Tính góc ADB, góc CDB"
# reg = re.compile(r'góc\s+([A-Z]{1,3})')
# kq = reg.findall(text)
# print(kq[0])
# print(kq[1])