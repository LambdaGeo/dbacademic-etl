import sys
sys.path.append('/opt/airflow/')
from datetime import timedelta
from airflow.utils.dates import days_ago
from utils.dag_utils import *


import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['breno.nahuz@discente.ufma.br'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'schedule_interval' : '@once',
    'start_date': days_ago(0),
    'retry_delay': timedelta(minutes=5),
}



config_dags = {
    "mapeamento": {
        "docentes": {
            "nome": [
                "NOME",
                "nome",
                "servidor",
                "NOME SERVIDOR",
                "SERVIDOR",
                "Nome do Servidor",
                "Nome",
                "NOME_FUNCIONARIO",
                "nome_servidor",
                "NomeServidor",
                "nome_oficial"
            ],
            "id": ["SIAPE", 
                "Siape",
                "siape",
                "matricula",
                "Matrícula",
                "Matricula",
                "_id",
                "vinculo_servidor",
                "CodigoServidor",
            ],
            "matricula": ["Matrícula","SIAPE","Siape","MATRICULA","siape", "matricula", "vinculo_servidor", "CodigoServidor", "_id"],
            "sexo": ["sexo", "Sexo"],
            "formacao": [
                "formacao",
                "escolaridade",
                "TitulacaoServidor",
                "Escolaridade",
                "TITULAÇÃO",
                "NIVEL ESCOLARIDADE",
                "Titulacao",
                "TITULAÇÃO"
            ],
            "nome_lotacao": ["Órgão de Lotação (SIAPE)", "setor lotacao"],
            "codigo_lotacao": ["id_unidade_lotacao", "CÓDIGO DA UNIDADE ORGANIZACIONAL","setor_siape"],
            "email" : ["email"]
        },
        "discentes": {
            "nome": ["nome", "nome_discente"],
            "id": ["ra", "matricula"],
            "matricula": ["ra", "matricula"],
            "sexo": ["sexo"],
            "data_ingresso": ["data_inicio"],
            "codigo_curso": ["id_curso"],
            "nome_curso": ["curso"],
        },
        "cursos": {
            "nome": ["nome", "nome_curso", "nome curso"],
            "id": ["id_curso"],
            "codigo": ["id_curso","I N E P"],
            "codigo_unidade": ["id_unidade_responsavel"],
        },
        "unidades": {
            "nome": ["nome_unidade"],
            "id": ["id_unidade"],
            "codigo": ["id_unidade"],
        },
    },
    "instituicoes": {
        "ufrn": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Rio_Grande_do_Norte",
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufrn.br",
            "colecoes": {
                "docentes" : {"resource_id": "6a8e5461-e748-45c6-aac6-432188d88dde"},
                "discentes": {"resource_id": "a55aef81-e094-4267-8643-f283524e3dd7"},
                "cursos"   : {"resource_id": "a10bc434-9a2d-491a-ae8c-41cf643c35bc"},
                "unidades" : {"resource_id": "3f2e4e32-ef1a-4396-8037-cbc22a89d97f"},
            },
        },
        "ufca": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Cariri",
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufca.edu.br",
            "colecoes": {
                "docentes" : {"resource_id": "6b2dbca5-58f8-472e-bc6a-eb827e631873"},
                "unidades" : {"resource_id": "406c5ac5-a8ff-4a9a-b343-83e1eb804725"},
                "cursos"   : {"resource_id": "5f31e620-a366-42c9-a54c-96da666c93b7"}
            },
        },
        "ufpi": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Piauí",
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufpi.br",
            "colecoes": {
                "docentes" : {"resource_id": "a34d7d7e-30af-41f0-81cf-cd10b6f078bd"},
                "discentes": {"resource_id": "cae87438-1bc2-40a5-93e5-d2faec76696f"},
                "cursos"   : {"resource_id": "5e75981a-f647-49d2-95d6-ec6ddd60b0bb"}
            },
        },
        "ufcspa": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Ciências_da_Saúde_de_Porto_Alegre",
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufcspa.edu.br",
            "colecoes": {
                #"docentes" : {"resource_id": "4286a4d5-9de7-4f88-bb37-f0f064415118", "q": "Professor"},
                "docentes" : {"resource_id": "4286a4d5-9de7-4f88-bb37-f0f064415118"},
                "cursos"   : {"resource_id": "6096d836-9160-43ae-bbbd-8712d4b202ca"},
                "unidades" : {"resource_id": "d49b7765-b19a-4d4e-9e2d-feb9f7520beb"}
            },
        },
        "unifespa": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Sul_e_Sudeste_do_Pará",
            "consumer": "CkanConsumer",
            "main_url": "http://ckan.unifesspa.edu.br",
            "colecoes": {
                "docentes" : {"resource_id": "b013c8cf-67e7-4ec0-ae30-c280cbebc65e"},
                "cursos"   : {"resource_id": "9ee93dc4-9398-43fc-91c4-1173b9378fed"}
            },
        },
        "ufv": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Viçosa",
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufv.br",
            "colecoes": {
                "docentes" : {"resource_id": "a949a903-9536-4d20-87e5-cca5c217771a"},
                "discentes": {"resource_id": "f7128b4a-07fb-4a87-ac5d-cd73cb82dfbe"},
                "cursos"   : {"resource_id": "e569f2e0-8ba0-4922-b715-9928980ae9f2"}
            },
        },
        "ufsj": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_S%C3%A3o_Jo%C3%A3o_del-Rei",
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ufsj.edu.br",
            "colecoes": {
                "docentes" : {"resource_id": "8e2e35ed-e255-4894-b070-ad8857366faf"},
                "cursos"   : {"resource_id": "15625dc7-acc2-45e8-9189-46e4362c013f"},
                "unidades" : {"resource_id": "916cf54f-b4d2-402b-affe-aa7b156dd5ef"}
            },
        },
        "ufms": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Mato_Grosso_do_Sul",
            "consumer": "CkanConsumer",
            "main_url": "https://dadosabertos.ufms.br/",
            "colecoes": {
                #"docentes" : {"resource_id": "a8ca7f30-0824-489b-8c70-faddcbd74f53","q": "Professor do Magisterio Superior"},
                "docentes" : {"resource_id": "a8ca7f30-0824-489b-8c70-faddcbd74f53"},
                "cursos"   : {"resource_id": "ae830b77-fc5c-47fa-9717-5eb9ff4b4e40"},
                "discentes": {"resource_id": "ebaa630c-848d-4df6-80bb-d87370e757b3"}
            },
        },
        "ufop": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Ouro_Preto",
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ufop.br",
            "colecoes": {
                "docentes": {"resource_id": "04e65338-1b7f-45b7-893b-05470d17dcad"}
            },
        },
        "ifgoiano": {
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_Goiano",
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ifgoiano.edu.br",
            "colecoes": {
                "docentes": {"resource_id": "ecd0ad77-2125-42c4-a8d0-c3fe012731dd"}
            },
        },
        "ifms": {
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ifms.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_de_Mato_Grosso_do_Sul",
            "colecoes": {
                "docentes": {"resource_id": "4ccd20e6-703d-4682-a300-26a0e3788a4f"},
                "discentes": {"resource_id": "b8b4dfdf-98ef-4d57-baff-75c163be6e9a"},
            },
        },


        "ufma": {
            "consumer": "CkanConsumer",
            "main_url": "https://dadosabertos.ufma.br/",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Maranhão",
            "colecoes": {
                "docentes": {"resource_id": "55a2d103-d73b-449e-85bc-655df7dfc45a"},
            },
        },

        "ifap": {
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ifap.edu.br/",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Amapá",
            "colecoes": {
                "docentes": {"resource_id": "005896e4-2a0a-4ddb-8420-62258d231871"},
            },
        },

        "univasf": { 
            "consumer": "CkanConsumer",
            "main_url": "http://dados.univasf.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Vale_do_São_Francisco",
            "colecoes": {
                "docentes": {"resource_id": "de111b8a-9b29-460e-acd3-7fda0ac62e41"},
            },
        },

        "ufvjm": { 
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufvjm.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_dos_Vales_do_Jequitinhonha_e_Mucuri",
            "colecoes": {
                "docentes": {"resource_id": "0b9aa08a-e251-43d0-959a-e08de3d71e5a"},
            },
        },


        "ufgd": { 
            "consumer": "CkanConsumer",
            "main_url": "http://dadosabertos.ufgd.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_da_Grande_Dourados",
            "colecoes": {
                "docentes": {"resource_id": "2249c447-7ae3-440a-afca-aa8ac8bb0596"},
            },
        },


        "uffs": { 
            "consumer": "CkanConsumer",
            "main_url": "https://dados.uffs.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_da_Fronteira_Sul",
            "colecoes": {
                "docentes": {"resource_id": "1e801321-6e0b-4716-ba1d-ce79919e87da","q":"Professor"},
            },
        },

        "unifei": { 
            "consumer": "CkanConsumer",
            "main_url": "https://dados.unifei.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Itajubá",
            "colecoes": {
                "docentes": {"resource_id": "50024421-d377-4184-ac23-e7f0ee3ad2c1", "q": "Professor"},
            },
        },

        "ufpel": { 
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ufpel.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Pelotas",
            "colecoes": {
                "docentes": {"resource_id": "b63c24da-d96d-4ee2-bdaf-f7a8c37f0007", "q" : "Professor"},
            },
        },

        "ifsuldeminas": { 
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ifsuldeminas.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Sul_de_Minas",
            "colecoes": {
                "docentes": {"resource_id": "7db2014f-577f-4ec3-a6ab-2c7da2015f8b"},
            },
        },

        "ifpb": { 
            "consumer": "FileConsumer",
            "main_url": "https://dados.ifpb.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_da_Paraíba",
            "colecoes": {
                "docentes": {
                    "resource": "dataset/26d67876-0cb2-41a4-83ed-7bde06eb736c/resource/0d03ee6a-2af1-4dde-9b3d-90419c48fabe/download/servidores.json",
                    "q" : "cargo_emprego.str.contains('PROFESSOR')"
                    },
            },
        },


        "ifrn": { 
            "consumer": "FileConsumer",
            "main_url": "https://dados.ifrn.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Rio_Grande_do_Norte",
            "colecoes": {
                "docentes": {
                    "resource": "dataset/0c5c1c1a-7af8-4f24-ba37-a9eda0baddbb/resource/c3f64d5b-f2df-4ef2-8e27-fb4f10a7c3ea/download/dados_extraidos_recursos_servidores.json",
                    "q" : "cargo.str.contains('PROFESSOR')"
                    },
            },
        },

        "ifro": { 
            "consumer": "FileConsumer",
            "main_url": "https://dados.ifro.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Rio_Grande_do_Norte",
            "colecoes": {
                "docentes": {
                    "resource": "dataset/cefffa4b-b662-438f-b2fa-1ab9fa35471c/resource/41b84d9d-135a-47f2-80e5-9da63123073d/download/docentes_disciplina_de_ingresso.csv",
                    "data_type" : "csv"
                    },
            },
        },

        
        "ufs": { 
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufs.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Rio_Grande_do_Norte",
            "colecoes": {
                "docentes": {
                    "resource": "dataset/docentes/resource/doc-csv-docentes-da-ufs/download/doc-csv-docentes-da-ufs.csv",
                    "data_type" : "csv",
                    #"sep": ";",
                    #"decimals" : "."
                    },
            },
        },
        
    },
}


for institute, values in config_dags["instituicoes"].items():

    dag = dynamic_create_dag(
        dag_id = f'{institute}', 
        institute = institute,  
        conf = values , 
        generic_mapper = config_dags["mapeamento"],
        schedule_interval = '@once', 
        start_date = days_ago(0), 
        default_args = default_args)
    globals()[dag.dag_id] = dag

dag_ttl = create_dag_ttl ("transform_save_ttl", config_dags, '@once',  days_ago(0), default_args)
globals()[dag_ttl.dag_id] = dag_ttl