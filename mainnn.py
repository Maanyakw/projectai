import base64
import streamlit as st
import pickle
import pandas as pd

# Function to convert an image to base64
@st.cache_data
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Error: The file at {file} was not found.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Correct file path with forward slashes or raw string literal
file_path = r"C:\Users\Ananya dixit\OneDrive\Desktop\background.jpg"

# Get the base64-encoded image for the background
img_base64 = get_img_as_base64(file_path)

# Check if the image was loaded properly
if img_base64 is None:
    st.stop()  # Stop the app if the image loading failed

# Display the image at the top of the page
st.image(f"data:image/jpeg;base64,{img_base64}", use_column_width=True)

# Set page background image using CSS
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("C:/Users/Ananya dixit/OneDrive/Desktop/projectphoto/background.jpg");
width: 100%;
height: 100%;
background-repeat: no-repeat;
background-attachment: fixed;
background-size: cover;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/jpeg;base64,{img_base64}");
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title of the app
st.markdown("""
    # *IPL VICTORY PREDICTOR*            
""")

# Dropdown selections for teams and city
teams = ['--- select ---',
         'Sunrisers Hyderabad', 'Mumbai Indians', 'Kolkata Knight Riders',
         'Royal Challengers Bangalore', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Bangalore', 'Hyderabad', 'Kolkata', 'Mumbai', 'Visakhapatnam', 'Indore',
          'Durban', 'Chandigarh', 'Delhi', 'Dharamsala', 'Ahmedabad', 'Chennai', 'Ranchi',
          'Nagpur', 'Mohali', 'Pune', 'Bengaluru', 'Jaipur', 'Port Elizabeth', 'Centurion',
          'Raipur', 'Sharjah', 'Cuttack', 'Johannesburg', 'Cape Town', 'East London',
          'Abu Dhabi', 'Kimberley', 'Bloemfontein']

# Load pre-trained pipeline from pickle file
try:
    pipe = pickle.load(open(r'C:\Users\Ananya dixit\Downloads\IPL-Winner-Predictor-main\IPL-Winner-Predictor-main\pipe.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: The model file 'pipe.pkl' was not found.")
    st.stop()  # Stop the app if the model is not found

# Layout with columns for selecting teams
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team', teams)

with col2:
    if batting_team == '--- select ---':
        bowling_team = st.selectbox('Select Bowling Team', teams)
    else:
        filtered_teams = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('Select Bowling Team', filtered_teams)

# Select venue and match details
seleted_city = st.selectbox('Select Venue', cities)
target = st.number_input('Target')

col1, col2, col3 = st.columns(3)

with col1:
    score = st.number_input('Score')
with col2:
    overs = st.number_input("Overs Completed")
with col3:
    wickets = st.number_input("Wickets Down")

# Button to predict
if st.button('Predict Winning Probability'):
    try:
        # Calculate required features for prediction
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_remaining = 10 - wickets
        crr = score / overs
        rrr = runs_left / (balls_left / 6)
        
        # Prepare input data for prediction
        input_data = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                                   'city': [seleted_city], 'runs_left': [runs_left], 'balls_left': [balls_left],
                                   'wickets_remaining': [wickets_remaining], 'total_runs_x': [target],
                                   'crr': [crr], 'rrr': [rrr]})
        
        # Make prediction using the model
        result = pipe.predict_proba(input_data)

        # Extract win/loss probabilities
        loss = result[0][0]
        win = result[0][1]

        # Display the results
        st.header(f"{batting_team} = {round(win * 100)}%")
        st.header(f"{bowling_team} = {round(loss * 100)}%")
    except Exception as e:
        st.header("Some error occurred.. Please check your inputs!")
        st.error(f"Error: {str(e)}")
