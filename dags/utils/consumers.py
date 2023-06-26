import requests
import pandas as pd
import json
import ssl

#from dag_utils import normalize_collumns
from time import sleep

ssl._create_default_https_context = ssl._create_unverified_context

class FileConsumer:
    def __init__(self, main_url, total: int = None ):
        self.main_url  = main_url
        self.total     = total
        
    def request(self, **params ) -> pd.DataFrame:

            data_type : str = "json"
            n_tries : int = 5

            resource = params["resource"]
            if "data_type" in params:
                data_type = params["data_type"]
            if "encoding" in params:
                encoding = params["encoding"]
            else:
                encoding = 'UTF-8'

            self.url = f'{self.main_url}/{resource}'
            print(f'[INFO] - Getting data from {self.url} : data_type = {data_type}')
            
            #data = requests.get(self.url, allow_redirects=True,verify=False)
            #print(data.content.decode(encoding))
            if data_type == 'csv':
                sep = ","
                decimal = '.'

                if "sep" in params:
                    sep = params["sep"]

                if'decimal' in params:
                    decimal = params["decimal"]
                
                #IFCE(discentes) está com o erro http.client.IncompleteRead 
                df = pd.read_csv(self.url, sep=sep, decimal=decimal, encoding=encoding,on_bad_lines='skip')
            elif data_type == 'xls':
                df = pd.read_excel(self.url, sheet_name=0, header=0, engine='openpyxl')

            elif data_type == 'json':
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.get(self.url, headers=headers)
                for tries in range(n_tries):
                    if response.status_code == 200:
                        df = pd.read_json(self.url)                        
                    elif response.status_code == 500:
                        print(f"[ERROR] - Status Code 500: Internal Error, try number {tries + 1}, trying again.")
                        sleep(10)
                        continue
                    else:
                        raise Exception(f"[ERROR] - Status code {response.status_code}, {json.dumps(response)}")
                
            if "query" in params:
                #colunas_str = data.dtypes[data.dtypes == 'str'].index
                #data[colunas_str].fillna('Desconhecido', inplace=True) # todo
                df.fillna('Desconhecido', inplace=True) ## se for tudo string, pode dar erro
                df = df.query(params['query'])
                print (df)
            
            if "index_col" in params:
                df[params['index_col']] = df.index
                print(df.head())
            
            if self.total:
                df = df.iloc[:self.total] 
            #Print Collumns
            print(df.columns)
            df = normalize_collumns(df)
            "---After---"
            print(df.columns)

            return df  

class CkanConsumer:
    def __init__(self, main_url, total = 10):
        self.total = total
        self.url = f'{main_url}/api/action/datastore_search'
    #COlocar campo da versão
    def request(self, **params) -> pd.DataFrame:
        self.resource_id = params["resource_id"]
        transform_params = params.copy()
        if 'limit' not in params:
            limit = 10000
            if self.total < 1000:
                limit = self.total
            params['limit'] = limit

        if 'offset' not in params:
            params['offset'] =  0

        if "query" in params:
            del params['query']

        data = []
        
        #print (params)
        response = requests.get(self.url, params=params,verify=False,)
        print(f'[INFO] - Getting data from {response.url}')
        print(f'[INFO] - Status:{response.status_code}')
        print(response.json())
        total = response.json()['result']['total']
        if total > self.total:
            total = self.total
        #print (response.json())
        print(f'[INFO] - Getting data from {response.url} at offset {len(data)} from {total}')

        data.extend(response.json()['result']['records'])

        while len(data) < total:
            params['offset'] = len(data)
            print(f'[INFO] - Getting data from {response.url} at offset {len(data)} from {total}')
            response = requests.get(self.url, params=params, verify=False)
            while response.status_code != 200:
                print(f'[ERROR] - Response code {response.status_code} from {self.url} on resource {self.resource_id} at offset {len(data)}')
                print(f'[INFO] - Waiting 5 seconds before trying again')
                sleep(5)
                response = requests.get(self.url, params=params, verify=False)
            data.extend(response.json()['result']['records'])
        print(f'[INFO] - Total of {len(data)} records retrieved from {self.url} on resource {self.resource_id}')
        df = pd.DataFrame(data)
        df = normalize_collumns(df)

        if "query" in transform_params:
                #colunas_str = data.dtypes[data.dtypes == 'str'].index
                #data[colunas_str].fillna('Desconhecido', inplace=True) # todo
                df.fillna('Desconhecido', inplace=True) ## se for tudo string, pode dar erro
                df = df.query(transform_params['query'])
                print (df)
        
        return df
    
def normalize_collumns(data:pd.DataFrame):
    #All collumns to lowercase
    data.columns = data.columns.str.lower()
    #Remove spaces
    data.columns = data.columns.str.replace(' ', '_')
    #Remove special characters
    #data.columns = data.columns.str.replace('[^A-Za-z0-9]+', '_')
    #Remove accents
    data.columns = data.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return data