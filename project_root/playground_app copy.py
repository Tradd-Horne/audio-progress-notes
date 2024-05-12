# from flask import Flask, render_template, request, jsonify
# from pydub import AudioSegment
# import speech_recognition as sr
# import openai
# import io
# import os
# from dotenv import load_dotenv

# output = openai.Completion.create()
# print(output)

# # Load environment variables from .env file
# load_dotenv()

# # Get the OpenAI API key from environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

#-----------------------
#-----------------------


import os
import PyPDF2
import re
import openai
import warnings

warnings.simplefilter("ignore", category=UserWarning) #supress warnings from incompatible PDFs

openai.api_key = open("key.txt", "r").read().strip("\n") #get api key from text file

def get_page(pdf_file): #get the first 400 characters from the first page of a PDF, remove newlines and special characters
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    page_obj = pdf_reader.pages[0]
    page_1 = page_obj.extract_text()
    page_1_top = page_1[0:400].replace("\n", " ") 
    page_1_top = re.sub('[^a-zA-Z0-9 \n\.]', '', page_1_top)
    return page_1_top

def get_title(prompt): #call chatgpt with few shot prompting, followed by new prompt injection, return title 
    clean_prompt =  re.sub("[:;,()\-]", "", prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role":"user", "content": "I will give you the text of the first page of a scientfic paper or article. You will reply only with the title of the article, do not include any punctuation or special characters in your response."},
                {"role":"assistant", "content": "OK, I understand. I am ready for the transcript."},
                {"role":"user", "content": "genesG C A T T A C G G C A T Review Alternative Splicing Role in New Therapies of Spinal Muscular Atrophy Jan Lejman1 Grzegorz Zieli  nski2  Piotr Gawda2 and Monika Lejman3 gid00030gid00035gid00032gid00030gid00038gid00001gid00033gid00042gid00045 gid00001 gid00048gid00043gid00031gi"},
                {"role":"assistant", "content": "Alternative Splicing Role in New Therapies of Spinal Muscular Atrophy"},
                {"role":"user", "content": "Invasiv e Californian death caps develop mushrooms unisexuallyand  bisexually   YenWen Wang1 Megan C. McKeon23 Holly Elmore4 Jaqueline Hess5 Jacob Golan1 Hunter  Gage6 William Mao1 Lynn  Harrow1 Susana C. Gonalves7 Christina M. Hull36 Anne  Pringle18 5     Abstract   Canonical  sexual"},
                {"role":"assistant", "content": "Invasive Californian death caps develop mushrooms unisexually and bisexually"},
                {"role":"user", "content": "Molecular Ecology  2009   18  817  833 doi  10.1111 j. 1365 294X.2008.04030.x   2009 The Authors Journal compilation   2009 Blackwell Publishing LtdBlackwell Publishing LtdThe ectomycorrhizal fungus Amanita phalloides  was  introduced and is expanding its range on the west coast of  North America ANNE PRINGLE     RACHEL I. ADAMS     HUGH B. CROSS  a nd THOMAS D. BRUNS   Department of Organismic an"},
                {"role":"assistant", "content": "The ectomycorrhizal fungus Amanita phalloides was introduced and is expanding its range on the west coast of North America"},
                {"role":"user", "content": "Contents lists available at ScienceDirect Metabolic Engineering journal homepage  www.elsevier.com locate meteng Metabolic engineering of Saccharomyces cerevisiae for the de novo production of psilocybin and related tryptamine derivatives N. Milne  P. Thomsen  N. M lgaard Knudsen  P. Rubaszka  M. Kristensen  I. Borodina  The Novo Nordisk Foundation Center for Biosustainability  Technical Universit"},
                {"role":"assistant", "content": "Metabolic engineering of Saccharomyces cerevisiae for the de novo production of psilocybin and related tryptamine derivatives"},
                {"role":"user", "content": "Contents lists available at ScienceDirect Talanta journal homepage www.elsevier.comlocatetalanta An overview of an arti cial nose system Xiu Zhanga1 Jing Chenga1 Lei Wua1 Yong Meia Nicole Ja rezicRenaultb Zhenzhong Guoa aHubei Province Key Laboratory of Occupational Hazard Identi cation and Control Medical College Wuhan University of Science and Technology Wuhan 430065 PR"},
                {"role":"assistant", "content": "An overview of an artificial nose system"},
                {"role":"user", "content": clean_prompt}     
                ]
    )
    reply_content = completion.choices[0].message.content
    reply_content = reply_content.replace("-", " ").replace(":", "").replace(",", "").replace("(", "").replace(")", "").replace("  ", " ").replace(".", "").replace("/", "")
    return(reply_content)

def rename_pdf(dir): #rename all pdfs in a directory after getting title
 for file in os.listdir(dir):
  if file.endswith(".pdf"):
   path = os.path.join(dir, file)
   title = get_title(get_page(path)) + ".pdf"
   os.rename(path, os.path.join(dir, title))

rename_pdf("Path to directory with PDFs")