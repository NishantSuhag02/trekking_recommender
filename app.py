import streamlit as st
import requests

base_url = 'http://127.0.0.1:8000'

st.set_page_config(page_title='Trek App',layout='wide')

page = st.sidebar.radio('Navigate',['Home','Explore Treks'])

# HOME PAGE
if page == 'Home':
    st.title('🏔 Trek Recommendation System')

    month = st.selectbox('Select Month',["Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"])
    
    difficulty = st.selectbox("Difficulty", ["Easy", "Moderate", "Difficult"])

    days = st.slider('Max Days', 1, 15, 5)

    budget = st.slider("Budget (INR)", 1000, 50000, 12000)

    if st.button('Get Recommendations'):
        params = {
            'month': month,
            'difficulty': difficulty,
            'days': days,
            'budget': budget
        }
        