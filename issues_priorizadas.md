# Issues Priorizadas para Generalização do DBAcademic ETL

Com base na análise arquitetural para a generalização do pipeline DBAcademic ETL para repositórios abertos e conversão para dados conectados, as seguintes *issues* foram extraídas e ordenadas por prioridade.

---

## 🔴 PRIORIDADE ALTA

### Issue 1: Refatoração da Conversão Semântica - Migração de `simpot` para `rdfmapper`
**Descrição:**
Atualmente, o mapeamento semântico no arquivo `models.py` utiliza a biblioteca `simpot`. Isso resulta em classes de domínio "engessadas" e acopladas à ontologia acadêmica CCSO, impedindo a generalização. A biblioteca `rdfmapper` (desenvolvida pela mesma equipe) deve ser adotada, pois oferece validação SHACL automática, um repositório dinâmico via SPARQL (`RDFRepository`) e suporte robusto a relacionamentos de entidades (One-to-One e One-to-Many).
**Critérios de Aceite:**
- [ ] Adicionar `rdfmapper-py` às dependências (`requirements.txt`).
- [ ] Refatorar os modelos existentes em `dags/utils/models.py` removendo as anotações do `simpot` e implementando os decoradores do `rdfmapper` (`@mapper.rdf_entity`, `@mapper.rdf_property`, etc.).
- [ ] Substituir o uso da função `serialize_to_rdf` pelas chamadas do `rdfmapper` (`to_rdf`).
- [ ] Implementar ao menos um teste de validação SHACL automática usando os dados transformados do Airflow.
**Tags:** `Refactor`, `Semantic-Web`, `High-Priority`

### Issue 2: Desacoplamento da Lógica Semântica com Mapeamento Dinâmico no `config.py`
**Descrição:**
Após integrar o `rdfmapper`, precisamos remover a necessidade de declarar estaticamente classes Python no Airflow para cada tipo de dado governamental extraído. O mapeamento semântico (qual coluna do JSON vira qual URI de qual Ontologia) deve passar a ser definido nas DAGs (`config.py`).
**Critérios de Aceite:**
- [ ] Adicionar um novo dicionário de mapeamento semântico (`property_mapping`, `target_ontology`) dentro das configurações das "colecoes" em `dags/config.py`.
- [ ] Criar uma função em `dags/utils/dag_utils.py` (ou `models.py`) capaz de gerar classes Python dinamicamente (meta-programação) baseadas no esquema do `config.py` e anotar essas classes virtuais com `rdfmapper`.
- [ ] Remover regras hardcoded (como o dicionário `formacao_dic` com validações puramente universitárias) e permitir validação universal via JSON de configuração e geração do *SHACL shape*.
**Tags:** `Feature`, `Airflow`, `Core`, `High-Priority`

---

## 🟡 PRIORIDADE MÉDIA

### Issue 3: Implementação de um `GenericRestConsumer` para Portais Genéricos
**Descrição:**
A malha de extração hoje é forte para dados CKAN e arquivos brutos (`FileConsumer`), porém portais governamentais abertos mais modernos costumam prover APIs REST com cabeçalhos de autenticação customizáveis e paginação no padrão Link Headers (RFC 5988). Para generalizar verdadeiramente, precisamos de um extrator genérico de REST.
**Critérios de Aceite:**
- [ ] Desenvolver a classe `GenericRestConsumer` dentro de `dags/utils/consumers.py`.
- [ ] Permitir a configuração de cabeçalhos genéricos (como `Authorization: Bearer <token>`) via dicionário da DAG.
- [ ] Implementar resiliência com suporte a controle de limites (Rate-Limiting) via status HTTP 429 e estratégias de recuo exponencial (*exponential backoff*).
- [ ] Garantir que o consumidor consiga tratar retornos JSON aninhados usando um parâmetro customizável para definir em qual "chave" reside o array de objetos principal.
**Tags:** `Feature`, `Data-Extraction`, `Medium-Priority`

---

## 🟢 PRIORIDADE BAIXA

### Issue 4: Implementação de Pipeline de Descoberta (Auto-Discovery)
**Descrição:**
Quando nos conectamos a um novo Portal Baseado em CKAN ou portal de transparência com catálogos vastos, mapear manualmente os `resource_ids` no `config.py` é extremamente moroso. Para automatizar o processo de inserção de novos conjuntos de dados, propõe-se criar uma DAG específica para "Descoberta".
**Critérios de Aceite:**
- [ ] Criar uma nova DAG (`discovery_dag.py`) cujo propósito não seja realizar ETL, mas sim chamar a API de *package_search* / *resource_search* do CKAN.
- [ ] O resultado da execução deve compilar e disponibilizar um relatório (JSON ou CSV) listando todos os datasets disponíveis na URL informada.
- [ ] O relatório deve conter informações sobre a estrutura e os tipos de dados do catálogo encontrado, de modo a servir de insumo prático para o desenvolvedor preencher o arquivo `config.py`.
**Tags:** `Enhancement`, `Airflow`, `Low-Priority`