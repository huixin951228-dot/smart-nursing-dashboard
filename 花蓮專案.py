import streamlit as st
import pandas as pd

st.set_page_config(page_title="智慧護理交班與臨床排程優化看板",layout="wide")
st.title("醫院智慧護理交班與臨床排程優化看板")
st.caption("行政流程創新提案:減輕醫護負擔 改善住院體驗")

if 'patients' not in st.session_state:
    st.session_state.patients={
        "101-1":{
            "name":"張大同","age":68,"gender":"男","diagnosis":"腦中風(Stroke)",
            "nursing_log":"今日意識清楚，右上肢肌力3分。上午10點血壓一度升至165/95mmHg，給藥後已穩定。",
            "orders":"1.每4小時測量NIBP。2.下午安排電腦斷層(CT)追蹤。3.注意防跌倒。",
            "schedule":[{"item":"腦部CT追蹤","dept":"醫學影像科","status":"等待中","priority":"緊急"}]
        }
    }


st.header("模組一:住院病患動態排程與護送調度看板")
schedule_list=[]
for bed,info in st.session_state.patients.items():
    for task in info["schedule"]:
        schedule_list.append({"病床號":bed,"姓名":info["name"],"檢查項目":task["item"],"執行科別":task["dapt"],"急迫度":task["priority"],"目前狀態":task["status"]})

df_schedule=pd.DataFrame(schedule_list)
df_schedule['sort_key']=df_schedule['急迫度'].map({'緊急':1,'一般':2,'常規':3})
df_schedule=df_schedule.sort_values(by='sort_key').drop(columns=['sort_key'])
st.dataframe(df_schedule,use_container_width=True,hide_index=True)

if st.button("啟動演算法:自動依排程權重指派傳送人員"):
    st.success("系統行政指派成功:傳送員A優先護送 101-1 張大同(原因:緊急CT檢查且權重最高)。")

st.header("模組二:AI智慧護理交班摘要(ISBAR)")
selected_bed=st.selectbox("請選擇欲交班的病床號:",list(st.session_state.patients.keys()))
patient_data=st.session_state.patients[selected_bed]

if st.button("啟動AI生成ISBAR結構化交班報告"):
    with st.spinner("AI正在提取電子病歷"):
        isbar_output=f"""
        **Identify(病人辨識):**交班{selected_bed}床{patient_data['name']}，主診斷為{patient_data['diagnosis']}。
        **Situation(現況):**目前病人意識清楚，今日主要問題為血壓波動及下午需進行隨訪CT檢查。
        **Background(臨床背景):**{patient_data['nursing_log']}
        **Assessment(評估):**醫療風險評估:高血壓危機風險、跌倒高風險(肌力受損)。
        **Recommendation(建議與叮嚀):**下一班請協助追蹤:{patient_data['orders']}
        """
        st.info("**AI行政流程優化成果:**")
        st.markdown(isbar_output)
