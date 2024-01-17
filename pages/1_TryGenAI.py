import streamlit as st
import pandas as pd
import json, sys

sys.path.append("../codeBase")
import privateAPIcall as pA
import openAI_api_withwait as oX

st.set_page_config(page_title="GenAI for Gene Study", page_icon=":globe_with_meridians:")

st.markdown("""
## Try out open AI for quering about a gene. 
Use following text area to try information on gene, background, scoring strategy and quesions and design your prompt. 
Read more about prompt desiging [here](https://developers.generativeai.google/guide/prompt_best_practices)

Encoded API will generate a response and will use deigned prompt for further query on multiple gene in the next page.
""")

# get prompt authentication

if 'api_obj' not in st.session_state:
    st.warning("To proceed further activate sesson with key")
    st.stop()
    st.switch_page("streamlit_app.py")
else:
    callAPI = st.session_state['api_obj']
    openAi_models_sel = callAPI.modelInfo[callAPI.modelInfo.modelName.str.contains("gpt")]
    openAi_models_select = st.selectbox("Select Model [gpt engine]",list(openAi_models_sel.modelName.values))
    st.info("prompt will use selected model : {}".format(openAi_models_select))

prompt_col, response_col = st.columns(2)

# sidebar parameters
st.sidebar.title("Tunable parameters")
st.sidebar.header("Temperature")
q_temp = 0
q_temp = st.sidebar.slider("set temperature [0: deterministic; 2: random]",value=0.7,min_value=0.0,max_value=2.0,step=0.1)

st.sidebar.header("Iteration")
q_iter = 1
q_iter = st.sidebar.slider("Generate each query :",value=1,min_value=1,max_value=10,step=1)

st.sidebar.header("Break time [seconds]")
b_timeout = 30
q_timeout = st.sidebar.slider("Time out for each query:", value=20,min_value=30, max_value=120)

param_definition= {}

with st.form("try_genAI_form"):

    with prompt_col:
        st.header("Prompt designing")

        geneName   = st.text_area('Gene to analyze', max_chars=10)
        background = "gene name, brief summary" 
        # st.text_area('Information on the gene [, separate]', max_chars=100)
        # st.write("exmaple: gene name, brief summary")
        scoring_strategy = "provide score 0 to 10 on following statements with 0 being low evidence and 10 being high evidence"
        #st.text_area("evaluatation rules:", max_chars=300)
        #st.write("example: provide score 0 to 10 on following statements with 0 being low evidence and 10 being high evidence")
        questions  = st.text_area("questions [, separated]:", max_chars=600)
        st.write("exmaple: this is a cell receptor, this is related to immune response, this gene is related to influenza infection, this is a cell adhesive gene")


        if geneName and questions:
            prompt_query = """provide following information on gene: {}; {}; {}; {}""".\
                        format(geneName, background,scoring_strategy.strip(),"\n".join(questions.split(",")))
            st.success(prompt_query, icon = "🤖")
            param_definition['background'] = background.split(",")
            param_definition['scoring_strategy'] = scoring_strategy.strip()
            param_definition['question'] = [i.strip() for i in questions.strip().split(",")]
            param_definition["model_setting"] = {"temperature":q_temp,"q_iter":q_iter}
        else:
            st.warning("provide gene name and background (like bierf summary) to start")

    submitted = st.form_submit_button("Generate Response",use_container_width=True)

    with response_col:
        st.header("Response")
        status_text = st.empty()
        if submitted and prompt_query:
            status_text.text("Runnning for {} [{} iterations] ..".format(geneName, param_definition["model_setting"]["q_iter"]))
            dxv = oX.run_for_gene(callAPI, geneName, param_definition, model_to_use=openAi_models_select, \
                                  backofftimer = b_timeout,iteration=param_definition["model_setting"]["q_iter"],\
                                   temperature=param_definition["model_setting"]["temperature"])
            
            status_text.text("Completed for {} [{} iterations] ..".format(geneName, param_definition["model_setting"]["q_iter"]))
            # with st.expander("see result in Json"):
            st.info(dxv)

            st.download_button(
                label="Download result",
                file_name="data.json",
                mime="application/json",
                data=json.dumps(dxv),
            )
        else:
            st.warning("Define a prompt query by filling in text on left column")


if param_definition:
    st.info("use the above parameters in the next excercise . Save the json and upload as a paramter file")
    json_string = json.dumps(param_definition)
    with st.expander("see set parameter in JSON"):
        st.json(json_string, expanded=True)

    st.download_button(
        label="Download JSON",
        file_name="{}_data.json".format(geneName),
        mime="application/json",
        data=json_string,
    )