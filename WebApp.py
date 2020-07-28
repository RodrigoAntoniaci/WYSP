#Libraries
import streamlit as st
import pandas as pd
import base64
#Importing code to calculate distance
from Calc_Dist import PlayIt

#Loading Dataframe to calculate distance
@st.cache
def load_dataset():
    dataframe = pd.read_csv('dummy_ign.csv',sep='|')
    return dataframe  

dataset = load_dataset()
@st.cache
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download: Right click here and save as CSV</a>'
    return href

#Creating Dict structure of user's choice
def Calc_result(dataframe,platform,theme1,theme2,old,critic,metric,n_results):
    user_dict = {'title':["User's choice"], 'release_date':[None],'score':[None], 'score_phrase':[None],'editors_choice':[None],
                'genre':[None],'url':[None],'old_game':[0], 'critic_high_score':[0],'Sony':[0],'Microsoft':[0],'Nintendo':[0],
                'Portable':[0],'Old_Consoles':[0],'Mobile':[0],'PC':[0],'Others_Plat':[0],'Playstation_4':[0],'Xbox_One':[0],
                'Wii_U':[0],'Action':[0],'Adult':[0],'Adventure':[0],'Baseball':[0],'Battle':[0],'Board':[0],'Card':[0],
                'Casino':[0],'Compilation':[0],'Editor':[0],'Educational':[0],'Episodic':[0],'Fighting':[0],'First-Person':[0],
                'Flight':[0],'Golf':[0],'Hardware':[0],'Hunting':[0],'Music':[0],'Other':[0],'Party':[0],'Pet':[0],'Pinball':[0],
                'Platformer':[0],'Productivity':[0],'Puzzle':[0],'RPG':[0],'Racing':[0],'Shooter':[0],'Simulation':[0],'Sports':[0],
                'Strategy':[0],'Trivia':[0],'Virtual':[0],'Word':[0],'Wrestling':[0]}

    if old == 'Hell Yeah':
        user_dict['old_game'] = [1]
    else:
        pass  

    if critic == 'Yes, milord':
        user_dict['critic_high_score'] = [1] 
    else:
        pass

    for key,value in user_dict.items():
        if key == theme1 or key == theme2 or key == platform:
            user_dict[key] = [1]
        else:
            pass
    
    calc = PlayIt(dataframe,user_dict,metric=metric, n_results=n_results)
    return calc.play_it()

st.sidebar.markdown('# IronHack - Final Project')
st.sidebar.markdown('# What You Should Play')
st.sidebar.markdown('## Description: \n\n Content-based game recommender system, calculates multi-dimensional distance between **User Input** VS **[Kaggle IGN Database](https://github.com/john7obed/ign_games_of_20_years/blob/master/ign.csv)**.')
st.sidebar.markdown('## Created by: \n\n **Rodrigo Sampaio Antoniaci**')

st.title('Choose Your Weapons')

#Initilizing Class to load Select Fields
play = PlayIt()

#Select Box of Platform
st.markdown('### **Choose a Console or Fabricant**')
platform = st.selectbox('',(play.platforms))


#Select Box of Theme 1
st.markdown('### **And what about the genres, which do you like the most?**')
themes1 = st.selectbox('',(play.themes))

#Select Box of Theme 2
st.markdown('### **Choose another on the house, if you want of course**')
themes2 = st.selectbox("",(play.themes),index=2)


#Select Box of Old
st.markdown('### **Would you like this game be an old one?** \n\n **We consider everything before 2k old... Milennials**')
old = st.selectbox("¯\__(ツ)__/¯",('Hell Yeah', 'Nops' ))


#Select Box of Critic Score
st.markdown('### **Would you like this game have high score by critics?**')
critic = st.selectbox("",('Yes, milord', 'Hate this guys' ))

#Select Box of Metric
st.markdown('### **What kind of metric do you want to use?**')
metric = st.selectbox("",('cityblock', 'cosine', 'euclidean'),index=2)

#Input of the number of results the user
st.markdown('### **How many results do you want to see?**')
n_results = st.number_input('',min_value=10,max_value=100,value=20)

#Button to run the distance calculation
apply_button = st.button("Lets play a game")
if apply_button:
    result = Calc_result(dataset,platform,themes1,themes2,old,critic,metric,n_results)
    st.markdown('# **Have a nice play time ;D**')
    st.markdown(f'## {get_table_download_link(result)}', unsafe_allow_html=True)
    st.dataframe(result)
else:
    pass
