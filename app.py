import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from deep_translator import GoogleTranslator
from metrics import load_clean_data, top_skills, experience_distribution, salary_distribution

HERE = Path(__file__).parent
CLEAN_PATH = HERE / "clean_jobs.csv"

st.set_page_config(page_title="Job Requirements Dashboard", layout="wide")

@st.cache_data
def get_data(path=CLEAN_PATH):
    return load_clean_data(path)

@st.cache_data
def translate_list(items, source="auto", target="en"):
    translator = GoogleTranslator(source=source, target=target)
    translations = []
    for it in items:
        try:
            translations.append(translator.translate(it))
        except:
            translations.append(it)
    return translations

df = get_data()
orig_areas = sorted(df['area'].dropna().unique())
trans_areas = translate_list(orig_areas)
en_to_area = {en: orig for orig, en in zip(orig_areas, trans_areas)}
selected_en = st.sidebar.multiselect("Select area", options=trans_areas, default=trans_areas)
filtered_df = df[df['area'].isin([en_to_area[e] for e in selected_en])]
if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()
top_n = st.sidebar.slider("Number of top skills", min_value=5, max_value=20, value=10)
st.title("Job Requirements Dashboard")
st.header("Top Skills")
skills = top_skills(filtered_df, n=top_n)
skill_names = skills.index.tolist()
translated_skills = translate_list(skill_names)
fig1 = px.bar(x=skills.values, y=translated_skills, orientation='h', labels={'x':'Number of Vacancies','y':'Skill (EN)'})
st.plotly_chart(fig1, use_container_width=True)
st.header("Experience Distribution (years)")
exp = experience_distribution(filtered_df)
fig2 = px.bar(x=exp.index, y=exp.values, labels={'x':'Years of Experience','y':'Number of Vacancies'})
st.plotly_chart(fig2, use_container_width=True)
st.header("Salary Distribution")
sal = salary_distribution(filtered_df)
salary_labels = [f"{int(interval.left)}–{int(interval.right)}" for interval in sal.index]
fig3 = px.bar(x=salary_labels, y=sal.values, labels={'x':'Salary Range','y':'Number of Vacancies'})
st.plotly_chart(fig3, use_container_width=True)
