
import streamlit as st
import openai
import os
from pydub import AudioSegment
import speech_recognition as sr
import io
from dotenv import load_dotenv
from datetime import datetime
from functions import generate_gpt_letter, process_audio, generate_gpt_response, read_file #import functions

load_dotenv() # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY") # Get the OpenAI API key from environment variable
note_template = '/Users/traddhorne/Documents/Documents - Tradd’s MacBook Pro/data_science_projects/Audio_Progress_Notes/project_root/progress-note_template.txt'
note_template = read_file(note_template)
letter_template = '/Users/traddhorne/Documents/Documents - Tradd’s MacBook Pro/data_science_projects/Audio_Progress_Notes/project_root/letter_general_initial.txt'
letter_template = read_file(letter_template)

#########
#FRONT END
#########
st.title('PodiatryNotes.com')
#---------------------
# note structure and length
#---------------------
col1, col2 = st.columns(2)
with col1:
    user_selection = st.selectbox('Select Note Structure', (['SOAP', 'H&P', 'Initial-General', 'Initial-Biomechanical']))
    if user_selection == 'SOAP':
        note_structure_selected = note_template
    elif user_selection == 'H&P':
        note_structure_selected = note_template
    elif user_selection == 'Initial-General':
        note_structure_selected = note_template
    elif user_selection == 'Initial-Biomechanical':
        note_structure_selected = note_template
    else:
        note_structure_selected = user_selection


with col2:
    note_length_selected = st.selectbox('Select Note Length', (['Brief', 'Medium', 'Detailed']))
    if note_length_selected == 'Brief':
        note_length_selected = '150-200 words'
    if note_length_selected == 'Medium':
        note_length_selected = '200- 300 words'
    if note_length_selected == 'Detailed':
        note_length_selected = '400 words'

st.write("\n")


with col1:
    st.write("Would you like to generate a letter? ")
    letter_yes= st.checkbox('Yes')
with col2:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    letter_no= st.checkbox('No')
    
letter_structure_selected = st.selectbox('Select Letter Structure', (['GP Letter', 'Specialist Letter', 'Referral Letter', 'Medical Certificate', 'Initial General']))
       
#---------------------
# audio file uploader and transcription
#---------------------    
audio_file = st.file_uploader("Upload Audio", type=['wav', 'mp3', 'm4a', 'flac'])

transcribed_text = None
gpt_response = None

# Process audio file immediately after upload
if audio_file is not None:
    with st.spinner('Processing audio...'):
        transcribed_text = process_audio(audio_file)
        
    if transcribed_text:
        with st.spinner('Generating GPT-3 response...'):
            gpt_response = generate_gpt_response(transcribed_text, note_length_selected, note_structure_selected)
            st.text_area("Patient Notes:", value=gpt_response, height=500)  
    if gpt_response is not None and letter_yes is True:
        with st.spinner('Generating Letter...'):
            gp_letter = generate_gpt_letter(gpt_response, letter_structure_selected)
            st.text_area("Letter:", value=gp_letter, height=500)
else:
    st.warning("Please upload an audio file to begin.")

# if transcribed_text:
#     st.text_area("Patient Notes:", value=gpt_response, height=500)       
#     st.write("Letter Template: \n")

#---------------------
# letter structure
#---------------------
if letter_structure_selected == 'GP Letter':
    letter_structure_selected = letter_template
elif letter_structure_selected == 'Specialist Letter':
    letter_structure_selected = letter_template
elif letter_structure_selected == 'Referral Letter':
    letter_structure_selected = letter_template
elif letter_structure_selected == 'Medical Certificate':
    letter_structure_selected = letter_template
elif letter_structure_selected == 'Initial General':
    letter_structure_selected = letter_template
else:
    letter_structure_selected = letter_structure_selected

#---------------------
# letter creation
#---------------------
# if st.button('Generate Letter'):
#     with st.spinner('Generating Letter...'):
#         gp_letter = generate_gpt_letter(gpt_response, letter_structure_selected)
#         st.text_area("Letter", value=gp_letter, height=500)

# if st.button==('Generate Letter'):
#         if gpt_response:
#             gp_letter = generate_gp_letter(gpt_response, letter_structure_selected)
#             st.text_area("Letter", value=gp_letter, height=500)
#         else:
#             st.error("Please generate the GPT-3 response first.")
#---------------------

