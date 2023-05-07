from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import sklearn
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from contentEctraction import final_resumes

in_text= final_resumes
in_text.append('new')
# terget=data['Category'].values

vect=TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english',
    max_features=400)

vect.fit(in_text)

in_Word_feature=vect.transform(in_text)

data=pd.read_csv(r"E:\\downloads\\UpdatedResumeDataSet.csv")



loaded_model = pickle.load(open('final_model.pkl', 'rb'))
prd1=loaded_model.predict(in_Word_feature)
# print(prd1)

d = {'Advocate': 0, 'Arts': 1, 'Automation Testing': 2, 'Blockchain': 3, 'Business Analyst': 4, 'Civil Engineer': 5, 'Data Science': 6, 'Database': 7, 'DevOps Engineer': 8, 'DotNet Developer': 9, 'ETL Developer': 10, 'Electrical Engineering': 11, 'HR': 12, 'Hadoop': 13, 'Health and fitness': 14, 'Java Developer': 15, 'Mechanical Engineer': 16, 'Network Security Engineer': 17, 'Operations Manager': 18, 'PMO': 19, 'Python Developer': 20, 'SAP Developer': 21, 'Sales': 22, 'Testing': 23, 'Web Designing': 24}
leng = len(prd1)
fields = []
for i in d:
    x = d.get(i)
    for j in range(leng):
        if x == prd1[j]:
            fields.append(i)

print(fields)
# print(name_lis)

