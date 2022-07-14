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

# text = "cho tam giác ABC có góc A = 60 độ, góc C = 50 độ"
# text = "Tia phân giác góc B cắt AC ở D."
# result = word_tokenize(text, format='text')
# result = ViTokenizer.tokenize(text)

# print(result)

# text = "Cho tam giác ABC, điểm M nằm trong tam giác đó"
# text = text_preprocess(text)
# reg = re.compile(r'tam giác\s+\w*\s*([A-Z]{3})')
# kq = reg.search(text).group(1)
# print(kq)

# text = " có góc A = 60 độ, góc C = 50 độ"
# #text = "Góc A = 60 độ, góc C = 50 độ"
# #text = "có góc A = góc C = 50 độ"
# #text = "Góc B - góc C = 20 độ."
# text = text_preprocess(text)
# reg = re.compile(r'(^|[^\-\+]\s)[gG]óc\s+([A-Z]{1,3})\s*=\s*(\d{1,3})\b')
# kq = reg.findall(text)
# for item in kq:
#     print(item[0])
#     print(item[1])
#     print(item[2])

# text = "Tia phân giác  góc  B  cắt  AC  ở  D."
# text = text_preprocess(text)
# reg = re.compile(r'phân giác.+góc\s+([A-Z]{1,3})\s+cắt\s+([A-Z]{2})\s+ở\s+([A-Z]{1})')
# kq = reg.search(text)
# #print(kq)
# print(kq.group(1))
# print(kq.group(2))
# print(kq.group(3))

# text = "Tính góc ADB, góc CDB"
# text = text_preprocess(text)
# reg = re.compile(r'([tính|so sánh]).+')
# kq = reg.search(text).group()
# print(kq)

# text = "Tính góc ADB, góc CDB"
# text = text_preprocess(text)
# reg = re.compile(r'góc ([A-Z]{1,3})')
# kq = reg.findall(text)
# print(kq[0])
# print(kq[1])

# text = "điểm M nằm trong tam giác đó"
# reg = re.compile(r'điểm ([A-Z]{1}) nằm trong tam giác')
# print(reg.findall(text))

# text = "Gọi E là một điểm nằm trong tam giác đó"
# reg = re.compile(r'([A-Z]{1}) là một điểm nằm trong tam giác')
# print(reg.findall(text))

# text = "Tia BM cắt AC ở K"
# text = text_preprocess(text)
# reg = re.compile(r'[tT]ia\s+([A-Z]{2})\s+cắt\s+([A-Z]{2})\s+ở\s+([A-Z]{1})')
# kq = reg.search(text)
# print(kq.group(1))
# print(kq.group(2))
# print(kq.group(3))

# text = "Kẻ BH vuông góc với AC"
# text = text_preprocess(text)
# reg = re.compile(r'\w*\s([A-Z]{2})\svuông\sgóc\s\w*\s*([A-Z]{2})')
# kq = reg.search(text)
# print(kq.group(1))
# print(kq.group(2))

# text = "có góc A = góc C = 50 độ"
# text = text_preprocess(text)
# reg = re.compile(r'góc\s([A-Z]{1,3})\s=\sgóc\s([A-Z]{1,3})\s=\s(\d{1,3})')
# kq = reg.findall(text)
# print(kq)

# text = "Gọi Am là tia phân giác của góc ngoài ở đỉnh A."
# text = text_preprocess(text)
# reg = re.compile(r'([A-Z][a-z]).*phân giác.*góc ngoài')
# kq = reg.findall(text)
# print(kq)

# text = "Hãy chứng tỏ rằng Am song song BC"
# text = text_preprocess(text)
# reg = re.compile(r'([A-Z][a-zA-Z]) song song ([A-Z][a-zA-Z])')
# kq = reg.findall(text)
# print(kq)

# text = "Góc B - góc C = 20 độ."
# #text = "có góc C = 20 độ."
# text = text_preprocess(text)
# #reg = re.compile(r'[Gg]óc ([A-Z]{1,3}) ([+-\\*/]) góc ([A-Z]{1,3}) = (\d{1,3})')
# reg = re.compile(r'[Gg]óc ([A-Z]{1,3}) ([\+\-\*\/]) góc ([A-Z]{1,3}) = (\d{1,3})')
# kq = reg.findall(text)
# print(kq)

# text = "Cho tam giác ABC vuông tại A"
# text = text_preprocess(text)
# reg = re.compile(r'vuông tại ([A-Z]{1})')
# kq = reg.search(text)
# print(kq.group(1))

# text = "Tìm góc bằng góc B"
# text = text_preprocess(text)
# reg = re.compile(r'[tT]ìm góc bằng góc ([A-Z]{1,3})')
# kq = reg.search(text)
# print(kq.group(1))

# text  = "Các tia phân giác của các góc B và C cắt nhau ở I"
# text = text_preprocess(text)
# reg = re.compile(r'phân giác.+góc ([A-Z]{1,3}) và ([A-Z]{1,3}) cắt nhau ở ([A-Z]{1})')
# kq = reg.findall(text)
# print(kq)

# text  = "Chứng minh rằng góc BEC là góc tù"
# text = text_preprocess(text)
# reg = re.compile(r'góc ([A-Z]{1,3}).*góc tù')
# kq = reg.findall(text)
# print(kq)

# text  = "Cho tam giác ABC = tam giác DEF"
# text = text_preprocess(text)
# reg = re.compile(r'tam giác ([A-Z]{3}) = tam giác ([A-Z]{3})')
# kq = reg.findall(text)
# print(kq)

# text  = "Cho hai tam giác ABC và ABD"
# text = text_preprocess(text)
# #reg = re.compile(r'tam giác ([A-Z]{3}) = tam giác ([A-Z]{3})')
# reg = re.compile(r'tam giác \w*\s*([A-Z]{3})\s*(và ([A-Z]{3}))?')
# kq = reg.findall(text)
# print(kq)

text = "có AB = BC = CA = 3cm"
text = "có AB = BD = 2cm"
text = text_preprocess(text)
reg = re.compile(r'([A-Z]{2}) = ([A-Z]{2})( = ([A-Z]{2}))?')
kq = reg.findall(text)
print(kq)

reg = re.compile(r'= ([0-9]+)cm')
kq = reg.findall(text)
print(kq)

text = "góc CAD = góc CBD"
text = text_preprocess(text)
reg = re.compile(r'góc ([A-Z]{3}) = góc ([A-Z]{3})')
kq = reg.findall(text)
print(kq)