from openai import AzureOpenAI
import pandas as pd
import json


class genAuth:
    def __init__(self,auth):
        self.client = AzureOpenAI(
                            api_key= auth['api_key'],
                            azure_endpoint = auth["azure_endpoint"],
                            api_version= auth["version"]) 
        modelID = auth['model']
        self.modelInfo = pd.DataFrame([[modelID, 'azure', 'GPT-4-Turbo']],columns=["modelName","object","ownedby"])
        self.client_state = True
    
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
                try:
                    return json.loads(response_chat.choices[0].message.content)
                except:
                    return response_chat.choices[0].message.content
            else:
                return {"error":'response could not generate sucessfully'}
        except Exception as e:
            return {"error":str(e)}
        