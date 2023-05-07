import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle

Rpath = "static/PDF"
Rfiles = [os.path.join(Rpath, f) for f in os.listdir(Rpath) if os.path.isfile(os.path.join(Rpath, f))]
file = r"C:\Users\SAFAN\OneDrive\Desktop\jobdc\web-developer-3.pdf"





def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                        resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


def pdfextract(file):
    fileReader = PyPDF2.PdfFileReader(open(file, 'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:
        pageObj = fileReader.getPage(count)
        count += 1
        t = pageObj.extractText()
        #         print (t)
        text.append(t)
    return text

jd = pdfextract(file)
cleaned_jd = cleanResume(str(jd))
final_resumes = []

i = 0
while i < len(Rfiles):
    file = Rfiles[i]
    #     dat = create_profile(file)
    resumeText = str(pdfextract(file))
    cleaned = cleanResume(resumeText)
    final_resumes.append(cleaned)
    i += 1

print(final_resumes)
# name_lis = []
# i = 0
# while i < len(Rfiles):
#     file = Rfiles[i]
#     base = os.path.basename(file)
#     filename = os.path.splitext(base)
#
#     # name = filename.split('_')
#     # name2 = name[0]
#     # name2 = name2.lower()
#     name_lis.append(file)
#     i = i + 1
# # print(final_resumes)
#
