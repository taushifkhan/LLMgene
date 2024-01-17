from openai import OpenAI
import pandas as pd
import json

class genAuth:
    def __init__(self,api_key):
        self.key = api_key
        self.client = OpenAI(
                            api_key=self.key,
                            )
        self.modelInfo = pd.DataFrame()
        self.client_state = False

    def getModels(self):
        openAi_models = []
        for k in self.client.models.list().data:
            # capbility =k["capabilities"]
            openAi_models.append([k.id,k.object,k.owned_by])
        self.modelInfo = pd.DataFrame(openAi_models,columns=["modelName","object","ownedby"])
        self.check()
        if self.client_state:
            return True
        else:
            return False
    
    def check(self):
        if self.client and self.modelInfo.shape[0]:
            self.client_state = True

    def getResponse(self, modelID, prompt_x, temperature_set):
        try:
            response_chat = self.client.chat.completions.create(
                model=modelID,
                # response_format={ "type": "json_object" },
                seed=99,
                messages=prompt_x,
                temperature=temperature_set)
            if (response_chat.choices[0].finish_reason == "stop"):
                return json.loads(response_chat.choices[0].message.content)
            else:
                return {"error":'response could not generate sucessfully'}
        except Exception as e:
            return {"error":str(e)}
        

class promptGeneration:
    def __init__(self, gname):
        self.gname = gname
    
    def addChatQuery(self,param):
        scorinscheme = 'from 0 to 10, with 0 indicating no evidence and 10 indicating very strong evidence'
        prompt_set = []
        prompt_set.append({"role":'assistant',"content":"Provide gene symbol and brief summary for the gene {} in json format.".format(self.gname)})
        prompt_set.append({"role":'user',"content":"For the gene {} score following statement {}.\
                            Use statement as key and score as value in the output".format(self.gname,scorinscheme)})

        for l in param['question']:
            prompt_set.append({"role":'assistant',"content":l})

        return prompt_set
    
    def addChatQuery_v2(self,param):
        scorinscheme = param['scoring_strategy']
        promptx_head = "provide following for the gene {} in json format: ".format(self.gname)
        prompt_body  = "official symbol, brief description. {} in Json format with statement as key and score as value.".format(scorinscheme)
        prompt_question_text = "\n".join(param['question'])
        prompt_x = promptx_head+prompt_body+prompt_question_text

        return [{"role":'system',"content":prompt_x}]

