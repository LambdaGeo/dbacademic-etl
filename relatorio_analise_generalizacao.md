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
*   **Uso Consolidado de Ferramentas Semânticas:** O sistema confia na sua extensão de anotações Python. O processo de serialização (JSON -> RDF) já está validado pelas rotinas de TTL.
*   **Geração de Identificadores Únicos Universais (URIs):** A estratégia em `models.py` (usando MD5 para gerar URI em cima do `instituição` + `coleção` + `código`) garante a imutabilidade e consistência, pré-requisitos essenciais em ecossistemas de *Linked Data*.

### 4.2. Limitações e Gargalos da Abordagem Atual (`simpot`)
*   **Rigidez Ontológica (`models.py`):** As classes Python mapeadas (`Docentes`, `Discentes`, `Cursos`, `Unidades`) possuem amarras a ontologias super específicas como a `CCSO` (Course Semantics Ontology).
    *   **Problema:** Se formos integrar dados de transações financeiras públicas (Portal da Transparência), a ferramenta não sabe qual Ontologia aplicar, visto que as classes base são engessadas.
*   **Regras de Domínio Intrusivas:** Em `models.py`, há validações engessadas, como o `formacao_dic` (dicionário que checa por Doutorado, Mestrado, etc). Este acoplamento impossibilita mapeamentos genéricos sem mexer no código Python nativo.
*   **A Abstração `simpot` não é Orientada a Configuração:** O `simpot` exige a recompilação ou adição manual de cada nova entidade mapeada e não fornece validação semântica integrada nem ferramentas flexíveis de *querying*.

## 5. Recomendações Arquiteturais para Generalização Total

Para converter o repositório **DBAcademic ETL** em um verdadeiro **Hub Semântico de Extração Genérica**, recomendo a implementação das seguintes frentes de trabalho:

### 5.1. Migração de `simpot` para `rdfmapper`
A substituição de `simpot` por **`rdfmapper`** (desenvolvida nativamente pela mesma equipe, LambdaGEO) traz enormes benefícios para escalar a generalização:
*   **Manutenção da Abordagem Declarativa:** O `rdfmapper` mantém a familiaridade com decoradores (como `@mapper.rdf_entity` e `@mapper.rdf_property`), reduzindo a curva de aprendizado da refatoração.
*   **Validação Automática (SHACL):** O `rdfmapper` gera *SHACL shapes* diretamente dos metadados da classe Python. Ao extrair bases genéricas (ex: despesas de prefeituras), poderemos definir as entidades e imediatamente garantir que os dados aderem ao formato esperado sem escrever validações manuais (como os *ifs* usados em `models.py` hoje).
*   **Repositório Dinâmico (`RDFRepository`):** Em cenários genéricos onde não sabemos com certeza como as queries serão formadas, o `RDFRepository` introduz *queries* dinâmicas via SPARQL (`find_by_*`, `count_by_*`). Isso permite que os dados extraídos pelo Airflow sejam validados e consultados imediatamente na malha de DAGs.
*   **Relacionamentos (One-to-One e One-to-Many):** A anotação fluida de relacionamentos do `rdfmapper` (`@mapper.rdf_one_to_many`) facilitará expressar ontologias complexas. Por exemplo, ligar um `Contrato` governamental a múltiplas `Licitacoes` ou `Empresas` torna-se muito simples em um ambiente generalizado.

### 5.2. Mapeamento Semântico Desacoplado
Embora o `rdfmapper` abstraia a complexidade em Python, para uma generalização "Low Code", as DAGs dinâmicas em `config.py` poderiam ser estendidas para ler configurações como:
*   `target_ontology`: ex: `http://schema.org/`
*   E a criação (meta-programação) dinâmica de classes decoradas com `rdfmapper` em tempo de execução dentro do Airflow, com base nesse JSON de configuração. Assim, o usuário apenas declararia o *schema* no JSON, e o Python do Airflow geraria a classe, aplicaria o `rdfmapper` e validaria os dados extraídos automaticamente contra o SHACL correspondente.

### 5.3. Pipeline Dinâmica de Descoberta (Auto-Discovery)
*   Para portais CKAN, criar uma DAG de "Descoberta" que não extraia os dados logo de cara, mas raspe os *endpoints* e retorne um catálogo dos datasets disponíveis em um formato legível.

### 5.4. Extensão dos Consumers
*   Adicionar um **`GenericRestConsumer`** que abstraia suporte a cabeçalhos de autenticação customizáveis (OAuth, Bearer Tokens) e paginações baseadas em Link Headers (RFC 5988).
*   Tratar o Pandas como um conector intermediário (ou migrar para *Polars* para processamento em *chunks*).

## 6. Conclusão

O repositório está excelentemente estruturado para a extração do escopo educacional universitário. No entanto, para ser um **hub genérico de Dados Abertos e Conectados**, a modelagem semântica atual deve ser refatorada.

A substituição de `simpot` por **`rdfmapper`** é o passo ideal. O `rdfmapper` preenche as lacunas arquiteturais ao fornecer **validação SHACL nativa** e suporte fluído a **relacionamentos**. Se aliado a uma rotina de *meta-programação* onde as classes do `rdfmapper` são instanciadas baseadas nas configurações do arquivo `config.py` (desacoplando regras *hardcoded* como as da ontologia CCSO), este repositório tornar-se-á uma plataforma *ELT* de Dados Abertos e Semântica de altíssimo nível.