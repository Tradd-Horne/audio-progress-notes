from pydub import AudioSegment
import speech_recognition as sr
import io
import openai

#convert .txt document to string
def read_file(letter_template):
    with open(letter_template, 'r') as file:
        data = file.read().replace('\n', '')
    return data

def process_audio(audio_file):
    if audio_file is None:
        st.error("Please upload an audio file.")
        return None

    file_extension = audio_file.name.split('.')[-1].lower()
    supported_extensions = ['wav', 'mp3', 'm4a', 'flac']
    if file_extension not in supported_extensions:
        st.error("Unsupported file type.")
        return None
    
    audio = AudioSegment.from_file(audio_file, format=file_extension)
    recognizer = sr.Recognizer()
    audio_wav_io = io.BytesIO()
    audio.export(audio_wav_io, format="wav")
    audio_wav_io.seek(0)
    
    with sr.AudioFile(audio_wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service;")
            return None
    return text


def generate_gpt_response(text, length, structure):
    if not text:
        st.error("Transcription failed or no text provided.")
        return "No response generated due to transcription failure."
    if not length:
        st.error("No length provided.")
        return "No response generated due to length not provided."
    if not structure:
        st.error("No structure provided.")
        return "No response generated due to structure not provided."
    
    

    prime_text = "Act as a world-class podiatrist in Australia, completing medical progress notes."
    prompt_text = (f'''
                   This is how the progress note should be structured: {structure}.\n
                   The structure should follow the SOAP format and use bullet points.\n
                   The medical progress note will be concise, informative and MUST BE {length}.\n
                   The medical progress note will cover all necessary aspects of the patient's condition and planned care.\n
                   Based on the dictation below, you are to curate a comprehensive progress note for the patient, 
                   adhering to the Australian Health Practitioner Regulation Agency standards.\n 
                   This is the brief presentation of the patient/ doctor interaction: {text}. 
                   ''')
    
    full_prompt = f"{prime_text}\n{prompt_text}"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=full_prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.4
    )
    
    gpt_output = response.choices[0].text.strip()
    return gpt_output


##################
#LETTER TEMPLATES
#####################
#GP LETTER TEMPLATE
#####################

#use chat gpt to generate a letter
def generate_gpt_letter(template, progress_note):
    if not progress_note:
        return "No progress note provided."
    if not template:
        return "No Letter Template provided."
    
    prime_text = '''Act as a world-class podiatrist in Australia, completing medical letters detailing patient assesments,
                    recommendations and treatment plans.'''
    prompt_text = (f'''
                   This is the brief presentation of the patient: {progress_note}.
                    Based on this dictation, I need a comprehensive letter for a the patients primary care physician,
                    detailing the patient's assessment, findings, and recommendations.
                   
                    The letter should be based of this template: {template}.
                    for the template: Informatoin inside " " should be included in the note verbatim every time.
                    Information inside [ ] is instructions to guide what information should be included in that section.
                   
                    Please ensure the medical progress note is concise, informative,
                    covering all necessary aspects of the patient's condition and planned care.
                   ''')
    
    full_prompt = f"{prime_text}\n{prompt_text}"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=full_prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7
    )
    gpt_output = response.choices[0].text.strip()
    return gpt_output
