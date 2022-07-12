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
text = "Tia phân giác góc B cắt AC ở D."
#result = word_tokenize(text, format='text')
result = ViTokenizer.tokenize(text)

print(result)
