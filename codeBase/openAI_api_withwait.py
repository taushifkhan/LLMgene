# Modules
import os
import openai
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
import json
openAi_models_select = 'datasvc-openai-dev-gpt35-turbo-instruct'

def createPrompt(gname,params):
    #copy prompt here"
    promptx_head = "provide following for the gene {}".format(gname)
    prompt_body  = "{} {}".format(params['background'],params['scoring_strategy'])
    prompt_question = params['question']
    prompt_question_text = "\n".join(prompt_question)
    promptx = promptx_head+prompt_body+prompt_question_text
    return promptx

def callGPT(modelID="text-davinci-003",temperature=0,promptID=''):
    response = openai.Completion.create(
              engine=modelID,
              prompt=promptID,
              temperature=0,
              max_tokens=1000,
              top_p=1.0,
              frequency_penalty=0.0,
              presence_penalty=0.0
            )
    
    if response["choices"][0]["finish_reason"] == "stop":
        return response
    else:
        return 0

def run_for_gene(gname, param_dict, model_to_use=openAi_models_select, backofftimer = 40,iteration=1,temperature=0):
    print (gname)
    mID = model_to_use 
    pd_tmp = {}
    promptx = createPrompt(gname, param_dict)

    for k in np.arange(1,1+iteration):
        start = time.time()
        res = callGPT(modelID=mID, promptID=promptx,temperature=temperature)
        end = time.time()

        timetaken = end-start
        if timetaken < backofftimer:
            time.sleep(backofftimer)

            runID = "{}_{}".format(mID, k)
            pd_tmp[runID] = res["choices"][0]["text"].strip().split("\n")
            
    return pd_tmp


def convertJson_DF(drespo):
    conver_dict = []
    for gene in drespo.keys():
        for model in drespo[gene].keys():
            tmp = {}
            tmp = {'geneSymbol':gene,'model':model}
            for m in drespo[gene][model]:
                if m:
                    tmp.update({m.split(":")[0].strip().replace(" ","_") : m.split(":")[1]})
            conver_dict.append(tmp)

    pd_csv = pd.DataFrame.from_dict(conver_dict)
    return pd_csv

def convertJson_DF_singleGene(drespo):
    conver_dict = []
    try:
        for model in drespo.keys():
            tmp = {}
            tmp = {'model':model}
            for m in drespo[model]:
                if m:
                    tmp.update({m.split(":")[0].strip().replace(" ","_") : m.split(":")[1]})
            conver_dict.append(tmp)

        pd_csv = pd.DataFrame.from_dict(conver_dict)
        return pd_csv, 0
    except:
        print ("error in parsing output")
        return 0, 0

# dfAll = {}
# geneList = pd.read_csv("./geneList/M9.2_genes.csv")


# for k in tqdm(geneList.Genes.values[:2]):
#     start = time.time()
#     dxv = run_for_gene(k,backofftimer=30,iteration=1)
#     end = time.time()
#     if end-start < 40:
#         time.sleep(30)
#     dfAll[k] = dxv

# # save out put in json
# json.dump(dfAll,open("./data/test_llm_Result.json","w"),indent=4)
