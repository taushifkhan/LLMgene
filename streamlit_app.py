import openai 
import streamlit as st
import pandas as pd

st.set_page_config(page_title="GenAI for Genes",page_icon=":cyclone:")

st.markdown("""## Use of Generative AI for gene prioritisation
Given an api authentication, you can use different models listed below for your own search.

## this uses open AI from azure ## for internal use only
""")
st.info("Add your openAI key on side bar to get strated")

openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

openai.api_key = openai_api_key
openai.api_type = 'azure'
openai.api_base =  'https://datasvc-openai-dev.openai.azure.com/'
openai.api_version = '2023-05-15'

openAi_models = []
for k in openai.Model.list()["data"]:
    capbility =k["capabilities"]
    openAi_models.append([k["id"],k["status"],k["object"],capbility["completion"],capbility["chat_completion"]])
openAi_models = pd.DataFrame(openAi_models,columns=["modelName","status","kind","completion","chat_completion"])


st.header("Models with give api")
st.write(openAi_models[openAi_models.completion==True])
st.info("(Read more about Models available in openAI)[https://platform.openai.com/docs/models]")
# openAi_models_select = st.selectbox("choose model ,use 'text-davinci-003':", list(openAi_models.modelName.values))