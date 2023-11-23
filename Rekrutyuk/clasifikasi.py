import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

xls = pd.ExcelFile('Employee_data_prediksi.xlsx')
df = pd.read_excel(xls, 'employee')
df_dict = pd.read_excel(xls, 'data_dictionary')

df=df.dropna()
df=df.reset_index()

from sklearn.preprocessing import LabelEncoder