# Relatório de Análise: Generalização do ETL DBAcademic para Repositórios Abertos e Dados Conectados (Linked Data)

## 1. Introdução

O presente relatório tem como objetivo analisar o repositório **DBAcademic ETL** e avaliar o seu potencial para ser generalizado, com o intuito de estender suas capacidades originais de extração e conversão. Originalmente concebido para lidar estritamente com dados de Instituições de Ensino Superior (docentes, discentes, cursos, unidades), a análise foca na viabilidade de utilizar esta arquitetura para **qualquer repositório aberto** (como Portal da Transparência, CKAN genéricos, etc.) e na **conversão universal para dados conectados (RDF/Linked Data)**.

## 2. Visão Geral da Arquitetura Atual

A solução é fundamentada em uma arquitetura de extração, transformação e carga (ETL) baseada em **Apache Airflow**, operando com as seguintes engrenagens:

*   **Orquestração Dinâmica:** O arquivo `dags/dynamic_dag.py` constrói DAGs de extração, mapeamento e conversão baseadas nos metadados de configuração definidos em `dags/config.py`.
*   **Consumers (Extratores):** O arquivo `dags/utils/consumers.py` possui dois extratores essenciais:
    *   `CkanConsumer`: Lida de forma robusta com o padrão de APIs CKAN, inclusive manipulando paginações limitadas.
    *   `FileConsumer`: Lida com links diretos para CSV, XLS, ODS ou JSON, adaptando parâmetros como codificações e separadores.
*   **Transformação e Mapeamento:** Em `dags/utils/dag_utils.py` os dados são mapeados. A transformação atual tenta reconciliar várias nomenclaturas de colunas para um padrão definido nas configurações de `mapeamento` de `config.py`.
*   **Modelagem RDF (Linked Data):** A conversão para dados conectados ocorre em `dags/utils/models.py`. Utilizando a biblioteca `simpot`, a conversão injeta as informações em estruturas semânticas fixas usando as ontologias CCSO (Core Course Semantics Ontology), FOAF, SCHEMA.org e AIISO.
*   **Carga:** Os dados transformados são inseridos no MongoDB (`mongo.py`), ou salvos/enviados em arquivos `.ttl` (Turtle) nativamente no Airflow.

## 3. Avaliação de Generalização: Extração de Repositórios Abertos

### 3.1. Pontos Fortes
*   **Modularidade nos Consumers:** A implementação orientada a objeto dos `Consumers` (`CkanConsumer`, `FileConsumer`) permite plugar novos tipos de APIs sem alterar a lógica principal das DAGs.
*   **Configuração Centralizada:** Toda a malha de captura hoje advém do dicionário em `config.py`. Para generalizar, bastaria inserir novos portais ali, sem precisar de código imperativo no Airflow.
*   **Paginação e Tratamento de Erros no CKAN:** A paginação e a resiliência no `CkanConsumer` são fundamentais e excelentes para raspar bases públicas de dados em portais brasileiros governamentais (que majoritariamente usam CKAN).

### 3.2. Limitações e Gargalos
*   **Hardcoding no Mapeamento de Colunas:** A lógica em `config.py` para `mapeamento` assume *hardcoded* quais coleções importam (docentes, discentes, etc.) e quais chaves podem representar seus nomes. Isso quebra perfeitamente a premissa de generalização onde o sistema extrairá dados não estruturados de domínio desconhecido.
*   **Falta de Suporte a APIs Paginação Genéricas:** Se um portal governamental possuir uma REST API aberta (ex: OData, GraphQL, ou REST paginado customizado), a atual abstração `CkanConsumer` não conseguirá extraí-los. Será necessário criar um `GenericAPIConsumer`.
*   **Limpeza Específica:** Parâmetros de `query` (ex: `"cargo.str.contains('Professor')"`) são passados via pandas `df.query()`. Isso é útil, mas em ambientes generalizados precisaria de uma camada de metadados mais declarativa e menos amarrada à sintaxe pandas internamente.

## 4. Avaliação de Generalização: Conversão para Dados Conectados

### 4.1. Pontos Fortes
*   **Uso Consolidado de Ferramentas Semânticas:** O sistema confia no `rdflib` e na sua extensão (`simpot`) de anotações Python. O processo de serialização (JSON -> RDF) já está validado pelas rotinas de TTL.
*   **Geração de Identificadores Únicos Universais (URIs):** A estratégia em `models.py` (usando MD5 para gerar URI em cima do `instituição` + `coleção` + `código`) garante a imutabilidade e consistência, pré-requisitos essenciais em ecossistemas de *Linked Data*.

### 4.2. Limitações e Gargalos
*   **Rigidez Ontológica (`models.py`):** As classes Python mapeadas (`Docentes`, `Discentes`, `Cursos`, `Unidades`) possuem amarras a ontologias super específicas como a `CCSO` (Course Semantics Ontology).
    *   **Problema:** Se formos integrar dados de transações financeiras públicas (Portal da Transparência), a ferramenta não sabe qual Ontologia aplicar, visto que as classes base são engessadas.
*   **Regras de Domínio Intrusivas:** Em `models.py`, há validações engessadas, como o `formacao_dic` (dicionário que checa por Doutorado, Mestrado, etc). Este acoplamento impossibilita mapeamentos genéricos sem mexer no código Python nativo.
*   **A Abstração `simpot` não é Orientada a Configuração:** O `simpot` depende de *Annotations* (`@RdfsClass`, `@BNamespace`) instanciadas diretamente nas classes Python. Isso exige a recompilação ou adição manual de cada nova entidade mapeada.

## 5. Recomendações Arquiteturais para Generalização Total

Para converter o repositório **DBAcademic ETL** em um verdadeiro **Hub Semântico de Extração Genérica**, recomendo a implementação das seguintes frentes de trabalho:

### 5.1. Evolução para RML (RDF Mapping Language) ou Config-Driven RDF
*   Abandonar o uso estrito do `simpot` e classes de domínio hardcoded em `models.py`.
*   Empregar a adoção de Mapeamento via **RML (RDF Mapping Language)** ou **YARRRML**.
    *   *Como funciona:* Em vez de criar a classe `Docentes` no Python, o usuário cria um arquivo YAML/JSON descrevendo: *A coluna X vira a URI Y baseada na ontologia Z*.
    *   O Airflow apenas chamaria um conversor genérico de dados tabulares (Pandas DataFrame) que injetaria o *Mapping Document* da vez para cuspir o `.ttl`.

### 5.2. Mapeamento Semântico Guiado por Ontologias Múltiplas (SHACL/ShEx)
*   Criar um arquivo de configuração semântica em nível de DAG. Hoje existe o `config.py` contendo: `"consumer": "FileConsumer", "main_url": "..."`.
*   O ideal seria adicionar neste contrato as propriedades:
    *   `target_ontology`: ex: `http://schema.org/`
    *   `subject_template`: ex: `https://dadosabertos.gov/{id}`
    *   `property_mapping`: um dicionário de pares chave-valor `{ "nome_coluna_api": "foaf:name" }`.
*   Esse desacoplamento evita qualquer lógica Python específica de domínio (Docentes, Cursos) e torna a conversão universal.

### 5.3. Pipeline Dinâmica de Descoberta (Auto-Discovery)
*   Para portais CKAN, criar uma DAG de "Descoberta" que não extraia os dados logo de cara, mas raspe os *endpoints* e retorne um catálogo dos datasets disponíveis em um formato legível para facilitar ao mantenedor a elaboração de novos mapeamentos JSON-para-RDF.

### 5.4. Extensão dos Consumers
*   Adicionar um **`GenericRestConsumer`** que abstraia suporte a cabeçalhos de autenticação customizáveis (OAuth, Bearer Tokens), paginações baseadas em Link Headers (RFC 5988), entre outros.
*   Tratar o Pandas como um conector intermediário. Atualmente as transformações do Pandas poluem muito a memória ao carregar grandes datasets na íntegra. Considerar Polars (já sugerido no README mas não implementado) ou a conversão baseada em *streams* em blocos (*chunks*).

## 6. Conclusão

O repositório é incrivelmente bem formatado para a automação no escopo educacional universitário (onde as nuances das APIs governamentais CKAN e planilhas em Portais foram profundamente mapeadas).

No entanto, sua **generalização** exigirá a substituição do coração da modelagem semântica atual (com classes e ontologias `CCSO` fixas em código Python) por um mecanismo baseado puramente em configurações descritivas (declarativas), como RML ou dicionários de mapeamento dinâmico no `config.py`. Caso o motor de semântica seja reescrito para ignorar "o que" está sendo convertido, tornando-se apenas um tradutor Universal JSON->RDF orientado a regras JSON/YAML, este repositório tornar-se-á uma plataforma de ELT de Arquitetura de Dados de altíssimo nível.