import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
st.title("Show Graph")

# gg sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# page connecting 
data_med = conn.read(worksheet="ข้อมูลยา", ttl=5)
data_med  = data_med.dropna(how="all")
data_info = conn.read(worksheet="รายชื่อนักเรียนหอพัก", ttl=5)
data_info = data_info.dropna(how="all")
data_ill = conn.read(worksheet="ข้อมูลโรค", ttl=5)
data_ill = data_ill.dropna(how="all")
data_stat = conn.read(worksheet="บันทึก", ttl=5)
data_stat = data_stat.dropna(how="all")

st.write("จำนวนคนกลุ่มโรคต่าง ๆ")
disease_df = pd.DataFrame(data_stat)
data_ill = pd.DataFrame(data_ill)
ill2type = {}
for i in range(len(data_ill)):
    ill2type[data_ill.loc[i, "ชื่อโรค"]] = data_ill.loc[i, "ข้อมูลกลุ่มโรค"]

#print(ill2type)

n_ill = []

for j in range(len(disease_df)):
    all_de = disease_df.loc[j,"โรค"].split(',')
    for k in all_de:
        n_ill.append(ill2type[k])
#print(n_ill)

labels = list(set(n_ill))
numeachlabels = [0]*len(labels)
for m in range(len(n_ill)):
    idxx = labels.index(n_ill[m])
    numeachlabels[idxx]+=1

df_ill_plot = pd.DataFrame({"ชื่อโรค":labels, "จำนวน":numeachlabels})
fig = px.pie(df_ill_plot, values='จำนวน', names='ชื่อโรค', color_discrete_sequence=px.colors.sequential.deep)
st.plotly_chart(fig, theme=None)

# plot each level and ill
name_ill = list(set(data_ill["ข้อมูลกลุ่มโรค"]))

illes = []
for i in range(len(name_ill)):
    for j in range(3):
        illes.append(name_ill[i])

classes = ["ม.4", "ม.5", "ม.6"]*len(name_ill)
cols = [0, 0, 0]*len(name_ill)
#print(name_ill)

for j in range(len(disease_df)):
    all_de = disease_df.loc[j,"โรค"].split(',')
    for l in range(len(all_de)):
        now_class = disease_df.loc[j,"ห้อง"]
        #classes.append(now_class)
        if(now_class == "ม.6"):
            idxx = name_ill.index(ill2type[all_de[l]])
            new_idx = (idxx*3)+2
            cols[new_idx]+=1
            
        elif(now_class == "ม.5"):
            idxx = name_ill.index(ill2type[all_de[l]])
            new_idx = (idxx*3)+1
            cols[new_idx]+=1

        elif(now_class == "ม.4"):
            idxx = name_ill.index(ill2type[all_de[l]])
            new_idx = (idxx*3)
            cols[new_idx]+=1

# print(classes)
# print(illes)
# print(cols)

de_class_df = pd.DataFrame({"ชั้น":classes, "โรค":illes, "จำนวน":cols})
#st.dataframe(de_class_df)
fig1 = px.bar(de_class_df, x="ชั้น", y="จำนวน", color="โรค")

st.plotly_chart(fig1, theme=None)
