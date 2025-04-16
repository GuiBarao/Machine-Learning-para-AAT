import pandas as pd

freq = pd.read_csv("data/frequencias.csv", delimiter=",")

list_freq = freq["palavra"].drop_duplicates()

list_freq.to_csv("data/frequencias2.csv")


