import streamlit as st
import pandas as pd
import sys
sys.path.append("./codeBase")
import privateAPIcall as pA
import azureAPIcall as aZ

st.set_page_config(page_title="GenAI for Genes",page_icon=":cyclone:")
st.markdown("""## Use of Generative AI for gene prioritisation
        Given an api, after authentication, you can use different models listed""")

st.info("Add your openAI key to get strated")

api_flavours = st.radio(
    "Access point specification",
    ["general","azure"]
)

if api_flavours == "general":
    st.write("API key to access openAI:")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    try:
        gA = pA.genAuth(openai_api_key)
        assert gA.getModels(), "error in model access"
        if gA.client_state:
            openAi_models_sel = gA.modelInfo[gA.modelInfo.modelName.str.contains("gpt")]
            if 'api_obj' not in st.session_state:
                st.session_state['api_obj'] = gA
            st.header("Models with give api")
            st.write(openAi_models_sel)
            st.info("(Read more about Models available in openAI)[https://platform.openai.com/docs/models]")
        else:
            st.warning("authentication error")
            st.stop()

    except Exception as e:
        st.warning("Error in API access:")
        st.write(str(e))
        st.stop()


    
    
elif api_flavours == "azure":
    st.warning("developing...")
    st.markdown("""
    ## Accessing openAI with custom deployed Auzre API
    """)

    auth_repo = {
            "azure_endpoint":"https://datasvc-openai-compsci-poc.openai.azure.com/",
            "api_key":"",
            "model":"datasvc-openai-compsci-poc-gpt4-turbo",
            "version":"2023-05-15"}

    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    endpoint = auth_repo["azure_endpoint"]#st.text_input("Azure endpoint",key="chatbot_endpoint", type="password")
    model = auth_repo["model"]#st.text_input("OpenAI Model",key="chatbot_model", type="password")
    api_version = auth_repo["version"]#st.text_input("deployemet version",key="chatbot_api_version", type="password")

    if not (openai_api_key and endpoint and model and api_version):
        st.info("Please add your Azure credentials to continue.")
        st.stop()

    auth = {"azure_endpoint":endpoint,
            "api_key":openai_api_key,
            "model":model,
            "version":api_version
            }
    # try:
    gA = aZ.genAuth(auth)
    assert gA.client_state, "Error in api"

    if 'api_obj' not in st.session_state:
        st.session_state['api_obj'] = gA
    st.write(gA.modelInfo)
    st.success("AzureOpenAI is now linked. WIll use give model in this session.")

    # except Exception as e:
    #     st.warning("Error in API access:")
    #     st.write(str(e))
    #     st.stop()


    # st.write(openai.Models.list())

    # openai.api_key = openai_api_key
    # openai.api_type = 'azure'
    # openai.api_base =  'https://datasvc-openai-dev.openai.azure.com/'
    # openai.api_version = '2023-05-15'



    # st.header("Models with give api")
    # st.write(openAi_models[openAi_models.completion==True])
    # st.info("(Read more about Models available in openAI)[https://platform.openai.com/docs/models]")
    # openAi_models_select = st.selectbox("choose model ,use 'text-davinci-003':", list(openAi_models.modelName.values))