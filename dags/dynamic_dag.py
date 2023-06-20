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
                "docentes" : {"resource_id": "4286a4d5-9de7-4f88-bb37-f0f064415118", "q": "Professor"},
                "cursos"   : {"resource_id": "6096d836-9160-43ae-bbbd-8712d4b202ca"},
                "unidades" : {"resource_id": "d49b7765-b19a-4d4e-9e2d-feb9f7520beb"}
            },
        },
        "unifesspa": {
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
                "docentes" : {"resource_id": "a8ca7f30-0824-489b-8c70-faddcbd74f53","q": "Professor do Magisterio Superior"},
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
                "docentes" : {"resource_id": "4ccd20e6-703d-4682-a300-26a0e3788a4f"},
                "discentes": {"resource_id": "7d7650fe-84a3-4927-8285-b1d48c766f6b"},
                "cursos"   : {"resource_id": "b1913941-fcd6-4216-882f-fc2a81121bcc"}

            },
        },


        "ufma": {
            "consumer": "CkanConsumer",
            "main_url": "https://dadosabertos.ufma.br/",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Maranhão",
            "colecoes": {
                "docentes" : {"resource_id": "55a2d103-d73b-449e-85bc-655df7dfc45a"},
                "cursos"   : {"resource_id": "1ec5679f-67b8-449d-8b10-dc955350ade4"},
                "discentes": {"resource_id": "d7107434-4280-4208-b831-2efa9572ff87"}
            },
        },

        "ifap": {
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ifap.edu.br/",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Amapá",
            "colecoes": {
                "docentes" : {"resource_id": "f121d410-9bf1-446d-9304-c0822905b5b3"},
                "cursos"   : {"resource_id": "f121d410-9bf1-446d-9304-c0822905b5b3"},
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
                "cursos"   : {"resource_id": "96ef79b5-a8d7-4aa6-b0ad-24607bb7eda5"}
            },
        },

        "unifei": { 
            "consumer": "CkanConsumer",
            "main_url": "https://dados.unifei.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Itajubá",
            "colecoes": {
                "docentes": {"resource_id": "50024421-d377-4184-ac23-e7f0ee3ad2c1", "q": "Professor"},
                "cursos"   : {"resource_id": "04e316c3-4278-41da-a299-980921a5a5fa"}
            },
        },

        "ufpel": { 
            "consumer": "CkanConsumer",
            "main_url": "http://dados.ufpel.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Pelotas",
            "colecoes": {
                "docentes": {"resource_id": "b63c24da-d96d-4ee2-bdaf-f7a8c37f0007", "q" : "Professor"},
                "cursos"   : {"resource_id": "335bed66-d18b-40e1-9ac1-0db6d4f50a99"}
            },
        },

        "ifsuldeminas": { 
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ifsuldeminas.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Sul_de_Minas",
            "colecoes": {
                "docentes" : {"resource_id": "7db2014f-577f-4ec3-a6ab-2c7da2015f8b"},
                "cursos"   : {"resource_id": "f3ebccba-3a38-4bf2-9b0f-80096f79a2a2"},
                "discentes": {"resource_id": "0dab4d92-316a-4b97-8e93-1c8ab0a26b25"},
            },
        },
        "ufsb": { 
            "consumer": "CkanConsumer",
            "main_url": "http://dadosabertos.ufsb.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Instituto_Federal_do_Sul_de_Minas",
            "colecoes": {
                "cursos"   : {"resource_id": "c723411f-7156-4a46-8769-425a8e60c2b9"},
                "discentes": {"resource_id": "9572074b-ce46-4d9b-8a4b-f8ddc7507ac3"}
            },
        },
        "unilab": { 
            "consumer": "CkanConsumer",
            "main_url": "http://dadosabertos.unilab.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_da_Integração_Internacional_da_Lusofonia_Afro-Brasileira",
            "colecoes": {
                "docentes" : {"resource_id": "d3a942b0-a579-4645-b559-6e97d0dc4a70"},
                "cursos"   : {"resource_id": "570a4151-95a6-44bc-9129-170a792fb314"},
                "discentes": {"resource_id": "3b947be4-2ca2-4b9c-9c88-e06396576394"}
            },
        },
        "ufpe": { #Não atualizavel
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufpe.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Pernambuco",
            "colecoes": {
                "docentes" : {"resource_id": "a5729061-f9ee-4d44-92ea-61e3c7722fc0"},
                "cursos"   : {"resource_id": "29bc7c28-0c74-46ac-8151-d9e39245f7ff"},
                "discentes": {"resource_id": "3ec70513-eca6-453d-95d1-fde1f1972a11"}
            },
        },
        "ufersa": {
            "consumer": "CkanConsumer",
            "main_url": "https://dadosabertos.ufersa.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_Rural_do_Semi-Árido",
            "colecoes": {
                "cursos"   : {"resource_id": "98e89cf8-4f36-451f-994a-29179c018ee0"}
            },
        },
        "ufscar": {
            "consumer": "CkanConsumer",
            "main_url": "https://dados.ufscar.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_São_Carlos",
            "colecoes": {
                "docentes" : {"resource_id": "8ffe29fe-415e-43d0-bb95-887e0b209cef","q": "Professor"},
                "cursos"   : {"resource_id": "f6f03301-42c9-4d23-80c3-75b1582a8020"},
                "discentes": {"resource_id": "50578feb-70c6-44ee-8425-a7b5b15c8bd5"}
            },
        },
        "utfpr": {
            "consumer": "CkanConsumer",
            "main_url": "http://dados.utfpr.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Tecnológica_Federal_do_Paraná",
            "colecoes": {
                "docentes" : {"resource_id": "3475ec4b-c807-411f-a134-a07862eb403f","q": "Professor"},
                "cursos"   : {"resource_id": "270d0fce-380f-4db8-899f-cde38630af9b"},
                "discentes": {"resource_id": "fd63c8e9-2295-4ee8-9e09-aaad17dc508d"}
            },
        },
        "uffs": {
            "consumer": "CkanConsumer",
            "main_url": "https://dados.uffs.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_da_Fronteira_Sul",
            "colecoes": {
                "docentes" : {"resource_id": "1e801321-6e0b-4716-ba1d-ce79919e87da","q": "PROFESSOR"},
                "cursos"   : {"resource_id": "96ef79b5-a8d7-4aa6-b0ad-24607bb7eda5"}
            },
        },
        "unila": {
            "consumer": "CkanConsumer",
            "main_url": "https://dados.unila.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_da_Integração_Latino-Americana",
            "colecoes": {
                "cursos"   : {"resource_id": "8fb54233-582c-4604-90db-318a0aaf3d4a"},
                "discentes": {"resource_id": "194dacdd-d152-41db-9c5b-7ed33d24e58a"}
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
                "cursos": {
                    "resource": "dataset/f2902132-dfc9-4fba-98ab-40346075224e/resource/47c6e782-6ef9-4942-8361-38d8aac22922/download/cursos.json"
                }
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
                "cursos": { #Estão dentro de um array chamado componentes_curriculares
                    "resource": "dataset/7b48f9d0-205d-46b1-8225-a3cc7d3973ff/resource/fe0e9d2c-1c02-4625-b692-13edcc3380ae/download/dados_extraidos_recursos_cursos-ofertados.json"
                },
                "discentes": {
                    "resource": "dataset/d5adda48-f65b-4ef8-9996-1ee2c445e7c0/resource/00efe66e-3615-4d87-8706-f68d52d801d7/download/dados_extraidos_recursos_alunos-da-instituicao.json"
                }
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
        "ufs": { #Dando timeout
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
        "unb": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dados.unb.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_de_Brasília",
            "colecoes": {
                #"docentes": { Arquivo zipado
                #    "resource": "dataset/9b6891b9-3c87-4337-b1d7-6c4187b10d00/resource/4cf8c882-82ea-4a19-a775-3f062cd1cc62/download/dados_institucionais_docentes.7z",
                #},
                'cursos': {
                    "resource": "dataset/cbae3cab-650f-487e-b936-0a5576ff757b/resource/539c24bf-e67f-4cd7-920a-6fd461435f88/download/cursos-de-graduao-03-2023.json",
                },
            }
        },
        "ufg": { #Não atualizável, apenas stricto_sensu
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufg.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Goiás",
            "colecoes": {
                "docentes": {
                    "resource": "dataset/c4d928ed-77e9-44c4-9c0d-77852b19c4c1/resource/b84f8ffb-aabd-4355-b41c-2d8843f579d9/download/da_servidores.csv",
                    "data_type" : "csv"
                },
                'cursos': {
                    "resource": "dataset/0d60fcf7-2bdb-41bd-86f4-327d6d91c34e/resource/c84060e7-920a-4072-8e14-fdfc45d37b9d/download/da_cursos_pos_graduacao.csv",
                    "data_type" : "csv"
                },
                'discentes': {
                    "resource": "dataset/6c3df25f-34ee-498a-8d79-4a071559b87e/resource/c2154e26-ea4b-4fcc-9c28-e03f28ea7851/download/da_discentes_stricto.csv",
                    "data_type" : "csv"
                }
            }
        },
        "ufba": {
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufba.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_da_Bahia",
            "colecoes": {
                "docentes": {
                    "resource": "dataset/4ba39fb2-470d-45df-8e7c-be0faeb5c8a1/resource/e95d0d5e-e9f0-4821-915d-6b31a95d272e/download/docentes.csv",
                    "data_type" : "csv"
                },
                'cursos': { #Stricto Sensu
                    "resource": "dataset/bf507a53-2299-498c-a7f0-7e1e807aa149/resource/e9acf9fc-ce5b-449e-b639-207d93872888/download/cursos_pos.csv",
                    "data_type" : "csv"
                }
            }
        },
        "ufpb": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dadosabertos.ufpb.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_da_Paraíba",
            "colecoes": {
                'cursos': {
                    "resource": "dataset/1af8700e-9f5e-4672-8017-ea93a934bcaf/resource/93214e98-e5cc-4cc5-aa74-db0f31564138/download/ensino_graduacao_curso_20221008.csv",
                    "data_type" : "csv",
                    "sep": ";"
                }
            }
        },
        "ufc": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufc.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Ceará",
            "colecoes": {
                'docentes': {
                    "resource": "dataset/e24b8acd-ee61-4027-9b9e-ede00a7311bc/resource/75aec4c5-bfee-4692-94c6-0767c60c080b/download/estrutura_de_pessoal_6_2023.csv",
                    "data_type" : "csv",
                    "q" : "cargo.str.contains('PROFESSOR')"
                },
                'cursos': {
                    "resource": "dataset/d1cde4bc-593d-4bb7-a086-4386140761d2/resource/a00652cc-9b73-46ec-a6ae-821a549a7bde/download/cursosofertadosgraduacao_2018.csv",
                    "data_type" : "csv"
                },
                'discentes': {
                    "resource": "dataset/7d220f71-b11c-4c72-8cd1-f537f335d8ab/resource/b78b2a16-c905-4cb8-9c82-8678856e14f0/download/discentes_da_graduao_6_2023.csv",
                    "data_type" : "csv"
                }
            }
        },
        "ufob": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://ufob.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Oeste_da_Bahia",
            "colecoes": {
                'cursos': {
                    "resource": "acesso-a-informacao/dados-abertos/api/2018/cursos-de-graduacao-2018.csv",
                    "data_type" : "csv"
                }
            }
        },
        "ufrpe": {
            "consumer": "FileConsumer",
            "main_url": "http://dados.ufrpe.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_Rural_de_Pernambuco",
            "colecoes": {
                'cursos': {
                    "resource": "dataset/d9a5a8f5-365e-480b-8578-1d5395490662/resource/4fa5ff11-0b7c-45ae-b934-2a6b82118a27/download/cursos.csv",
                    "data_type" : "csv"
                }
            }
        },
        "ufra": {
            "consumer": "FileConsumer",
            "main_url": "http://dados.ufra.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_Rural_da_Amazônia",
            "colecoes": {
                'docentes': {
                    "resource": "dataset/989c10bc-c2db-41ae-863a-e262760d8e6a/resource/af629a3e-c70c-452a-a1b0-617ec31a9cb5/download/servidores.csv",
                    "data_type" : "csv",
                    "sep": ";",
                    "q" : "cargo.str.contains('PROFESSOR')"
                },
            }
        },
        "unifesp": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "http://dadosabertos.unifesp.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_São_Paulo",
            "colecoes": {
                'docentes': {
                    "resource": "dataset/ed21a3c9-e8b4-4821-b1a5-3b7444eb32eb/resource/0c0a4411-f256-43c4-9674-f2cd2a34d081/download/lista-servidores-exercicio-portal-transparencia.xls_20230602.xls",
                    "data_type" : "xlsx",
                    "q" : "cargo.str.contains('PROFESSOR')"
                },
                'cursos': {
                    "resource": "dataset/17d76964-13c9-4faa-b484-f4093706966c/resource/e545a42a-07be-42eb-bcc1-3f78d619b828/download/cursos_unifesp_20230330.xls",
                    "data_type" : "xlsx"
                },
                'discentes': {
                    "resource": "dataset/93b05220-e073-4b0f-bad3-3b3262f85597/resource/5eab3163-c19b-4403-a066-8f6a9371fd88/download/discente_ingressantes_2023_20230529.xls",
                    "data_type" : "xlsx"
                }
            }
        },
        "ufu": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_de_Uberlândia",
            "colecoes": {
                'docentes': {
                    "resource": "https://dados.ufu.br/node/342/download",
                    "data_type" : "csv",
                    "q" : "cargo.str.contains('PROFESSOR')"
                }
            }
        },
        "ufabc": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufabc.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_ABC",
            "colecoes": {
                'docentes': {
                    "resource": "images/ufabc/sugepe/bases_sugepe/bd_sugepe03_2020.csv",
                    "data_type" : "csv",
                    "q" : "CARGO.str.contains('PROFESSOR MAGISTÉRIO SUPERIOR')"
                }
            }
        },
        "ufes": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dados.ufes.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Espírito_Santo",
            "colecoes": {
                'docentes': {
                    "resource": "dataset/3e0c2b10-259f-4cdf-acd2-78497f09d441/resource/8e0ab64a-f294-409b-b576-0f2d8398bc4d/download/docentes.csv",
                    "data_type" : "csv",
                    "q" : "cargo.str.contains('PROFESSOR')"
                },
                'discentes': {
                    "resource": "dataset/37ba75f0-333d-475a-b60a-8b87ac7e2129/resource/2682595c-5ed9-48a7-bb79-01135dfe3681/download/alunos.csv",
                    "data_type" : "csv",
                }
            }
        },
        "unirio": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "http://dados.unirio.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Estado_do_Rio_de_Janeiro",
            "colecoes": {
                'cursos': {
                    "resource": "dataset/bfc6f424-6137-4feb-9c4e-5512f8821415/resource/83d0d21f-63e1-4295-959a-1683e6a21937/download/cursosunirio2.csv",
                    "data_type" : "csv",
                }
            }
        },
        "ufmt": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://sistemas.uftm.edu.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_do_Triângulo_Mineiro",
            "colecoes": {
                'docentes': {
                    "resource": "integrado/?to=RTZjcGZxTGFsSkFOOXRhSkpVdm5ELzBmWjZPUjNwZVNDdzA3NzFoRzcxenlYcG9nTDdyZ3YyT1QyanU0Y2pMYXk3Q21DTUMySS9PWXlYWklyM2NaellvRlVTRVVZeVhodnBGZ2RVQkw0VkJza3Y3b2VhV2NmVmZIN1I5VmFCNng3K1ZpV1BLMnNrZE84dmk3NW1YNGVRK0FHWTBOTEQzNXk3MmE5SVhRR2NwRmN0QWV2dVd0ZHI5Z00zVTQ3ZTNq&secret=uftm",
                    "data_type" : "csv",
                },
                'cursos': {
                    "resource": "integrado/?to=RTZjcGZxTGFsSkFOOXRhSkpVdm5ELzBmWjZPUjNwZVNDdzA3NzFoRzcxenlYcG9nTDdyZ3YyT1QyanU0Y2pMYXk3Q21DTUMySS9PWXlYWklyM2NaellvRlVTRVVZeVhodnBGZ2RVQkw0VkJza3Y3b2VhV2NmVmZIN1I5VmFCNng3K1ZpV1BLMnNrZE84dmk3NW1YNGVUNjJWWWVwblVDb2hBaHFBYkQrZ3VHckNLdTZCWHAwNEVZbGpacUpqR3Nn&secret=uftm",
                    "data_type" : "csv",
                },
                'discentes': {
                    "resource": "integrado/?to=RTZjcGZxTGFsSkFOOXRhSkpVdm5ELzBmWjZPUjNwZVNDdzA3NzFoRzcxenlYcG9nTDdyZ3YyT1QyanU0Y2pMYXk3Q21DTUMySS9PWXlYWklyM2NaellvRlVTRVVZeVhodnBGZ2RVQkw0VkJza3Y3b2VhV2NmVmZIN1I5VmFCNng3K1ZpV1BLMnNrZE84dmk3NW1YNGVZeWJjeS8vNTRjanVvYnAvK09nQjNaRVpGeU9wZjlydlRETzZOZXBzWXBW&secret=uftm",
                    "data_type" : "csv",
                }
            }
        },
        "uff": { #Não atualizável
            "consumer": "FileConsumer",
            "main_url": "https://dados.uff.br",
            "dbpedia_pt": "http://pt.dbpedia.org/resource/Universidade_Federal_Fluminense",
            "colecoes": {
                'docentes': {
                    "resource": "dataset/be9ff610-b4ec-4f8a-8fee-b6bb9fc55d7a/resource/4b96d1f1-c4f1-4de9-b0e8-bb6f2c98fbc7/download/rh-docentes-2022-2.csv",
                    "data_type" : "csv",
                },
                'cursos': {
                    "resource": "dataset/e4cab554-8023-4562-8a5f-623439076b45/resource/1f73421a-d377-4b4d-bcd5-004a0a590ee5/download/grad-cursos-2022-2.csv",
                    "data_type" : "csv",
                }
            }
        }

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