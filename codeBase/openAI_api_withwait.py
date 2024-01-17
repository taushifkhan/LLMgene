# Modules
import pandas as pd
import numpy as np
import time, json

import privateAPIcall as pA

def run_for_gene(apiObj, gname, param_dict, model_to_use='gpt-4', backofftimer = 30,
                 iteration=1,temperature=0):
    print (gname)
    pd_tmp = {}
    promptGen = pA.promptGeneration(gname)
    promptx   = promptGen.addChatQuery_v2(param_dict)

    for k in np.arange(1,1+iteration):
        start = time.time()
        res = apiObj.getResponse(model_to_use, promptx, temperature)
        time.sleep(backofftimer)
        runID = "{}_{}".format(model_to_use, k)
        runID_time = "timestamp_{}_{}".format(model_to_use, k)
        pd_tmp[runID] = res 
        pd_tmp[runID_time] = round(time.time() -start,2) 
    return pd_tmp