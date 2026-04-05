import streamlit as st
import requests

base_url = 'http://127.0.0.1:8000'

st.set_page_config(page_title='Trek App',layout='wide')

page = st.sidebar.radio('Navigate',['Home','Explore Treks','ChatBot'])

# HOME PAGE
if page == 'Home':
    st.title('🏔 Trek Recommendation System')

    month = st.selectbox('Select Month',["Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"])
    
    difficulty = st.selectbox("Difficulty", ["Easy", "Moderate", "Difficult"])

    days = st.slider('Max Days', 1, 15, 5)

    budget = st.slider("Budget (INR)", 1000, 50000, 12000)

    if st.button('Get Recommendations', type="primary"):
        with st.spinner('Finding the perfect treks for you...'):
            params = {
                'month': month,
                'difficulty': difficulty,
                'days': days,
                'budget': budget
            }
            
            try:
                response = requests.get(f"{base_url}/recommend", params=params)
                
                if response.status_code == 200:
                    treks = response.json()

                    if not treks:
                        st.warning('No treks found matching your exact criteria. Try adjusting your budget or days!')
                    else:
                        st.success(f"Found {len(treks)} amazing treks for you!")
                        
                        # Displaying treks in a beautiful card-like format
                        for i, trek in enumerate(treks):
                            with st.container():
                                st.subheader(f"{i+1}. {trek.get('name', 'Unknown Trek')}")
                                
                                # Using columns to display stats neatly
                                col1, col2, col3, col4 = st.columns(4)
                                col1.metric("Difficulty", trek.get('difficulty', 'N/A'))
                                col2.metric("Duration", f"{trek.get('duration_days', 'N/A')} Days")
                                col3.metric("Est. Cost", f"₹{trek.get('estimated_cost_inr', 'N/A')}")
                                col4.metric("Rating", f"⭐ {trek.get('rating', 'N/A')}")
                                
                                # Using an expander to hide long descriptions
                                with st.expander("View Details & Gear Required"):
                                    st.write(f"**Region:** {trek.get('region', 'N/A')}")
                                    st.write(f"**Best Months:** {trek.get('best_months', 'N/A')}")
                                    st.write(f"**Description:** {trek.get('description', 'N/A')}")
                                    st.info(f"🎒 **Gear Required:** {trek.get('gear_required', 'N/A')}")
                                
                                st.divider() # Adds a clean horizontal line between treks
                else:
                    st.error("Error fetching recommendations from the API.")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend. Is your FastAPI server running?")

# ChatBot
if page == 'ChatBot':
    st.title('CHAT with our CHATBOT')

    user_input = st.text_input('Ask your Query')

    if st.button('ASK', type="primary"):
        if user_input:
            with st.spinner('Generating response...'):
                params = {'user_input': user_input}

                response = requests.get(f'{base_url}/chat', params=params)
                answer = response.json()
                st.write(answer)
        else:
            st.warning('No input was given!')


# EXPLORE TREKS PAGE
elif page == "Explore Treks":
    st.title('🏔 Explore All Treks')

    response = requests.get(f"{base_url}/treks")
    treks = response.json()

    search = st.text_input('🔍 Search Trek')

    if search:
        treks = [t for t in treks if search.lower() in t['name'].lower()]

    for trek in treks:
        if st.button(trek['name']):
            st.session_state['selected_trek'] = trek['name']
