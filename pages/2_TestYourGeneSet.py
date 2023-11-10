import streamlit as st
import time
import numpy as np
import pandas as pd
import json
from codeBase import openAI_api_withwait as oX

st.set_page_config(page_title="Upload your gene set", page_icon="📈")

st.markdown("""
## Use following parameters to examine your gene set
""")


gene_upload, paramFile_upload = st.columns(2)
# param_json = {}
# gene_dataframe = pd.DataFrame()

with gene_upload:
    uploaded_gene_file = st.file_uploader("Choose a CSV file with genes in 'Genes' column",type=['csv'])
    if uploaded_gene_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        gene_dataframe = pd.read_csv(uploaded_gene_file)
        st.write(gene_dataframe)

        if 'Genes' in gene_dataframe.columns:
            st.sidebar.header("choose top [n] genes to run")
            gene_to_run_count = st.sidebar.slider(label="choose n top gene:", min_value=2,max_value=gene_dataframe.Genes.nunique())
            st.info("Will use top {}[/{}] gene from the uploaded doc".format(gene_to_run_count, gene_dataframe.Genes.nunique()))

        else:
            st.warning("Consider renaming gene coulumn as 'Genes'. Can not process uploaded file")

with paramFile_upload:
    uploaded_param_file = st.file_uploader("Choose a JSON file with DEFINED paramters",type=['json'])

    if uploaded_param_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        param_json = json.load(uploaded_param_file)
        st.json(param_json)
        print (param_json.keys())


st.sidebar.header("LLM Progress")
status_text = st.sidebar.empty()

if (uploaded_gene_file is not None) & (uploaded_param_file is not None):

    if (gene_dataframe.Genes.nunique()>=1) & (all(key in param_json for key in ('background', 'scoring_strategy', 'question'))):
        gList = gene_dataframe.Genes.values
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()

        json_response = {}
        gen_to_run = gList[:gene_to_run_count]
        st.write("Genrating LLM response ...[Approximate time for {} genes = {} mins]".format(len(gen_to_run),len(gen_to_run)))
        time_start = time.time()
        last_run = 0
        for i in range(1, len(gen_to_run)+1):
            status_text.text("Runnning {}[{}/{}]|last run {}sec".format(gen_to_run[i-1], i, gene_to_run_count, last_run))
            dxv = oX.run_for_gene(gList[i-1],param_json, backofftimer = 40,iteration=1) # have to include model variableqaz3q1  
            json_response[gList[i-1]] = dxv
            progress_bar.progress(int(i/(len(gen_to_run)+1)*100))
            last_run = round(time.time()-time_start, 2)
        
        time_expand = time.time()-time_start
        
        st.write("Completed in {} sec [{} mins]".format(round(time_expand,3), round(time_expand/60,3)))
        progress_bar.empty()


        if json_response:
            st.info("Save output as JSON file")
            json_string_response = json.dumps(json_response)
            with st.expander("see result in JSON"):
                st.json(json_string_response, expanded=True)

            st.download_button(
                label="Download JSON",
                file_name="data_Response.json",
                mime="application/json",
                data=json_string_response,
            )

            st.info("out put in CSV")
            outCSV_igene = oX.convertJson_DF(json_response)
            with st.expander("see result in CSV"):
                st.write(outCSV_igene)
            st.download_button(
                label="Download data as CSV",
                data=outCSV_igene.to_csv().encode('utf-8'),
                file_name='LLM_reponse_{}_genes_{}.csv'.format(gene_to_run_count,'testMyGene'),
                mime='text/csv',    
                )
