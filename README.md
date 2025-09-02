# Desafio MBA Engenharia de Software com IA - Full Cycle

## Sobre o Projeto

Este é um sistema de **RAG (Retrieval-Augmented Generation)** que implementa um chatbot inteligente capaz de responder perguntas baseado no conteúdo de documentos PDF. O sistema utiliza técnicas avançadas de processamento de linguagem natural e busca semântica para fornecer respostas precisas e contextualizadas.

### Funcionalidades Principais

- **Ingestão de Documentos PDF**: Extrai e processa documentos PDF, dividindo-os em chunks otimizados para busca semântica
- **Geração de Embeddings**: Utiliza modelos de IA da OpenAI para criar representações vetoriais do conteúdo dos documentos
- **Armazenamento Vetorial**: Armazena os embeddings em um banco de dados PostgreSQL com extensão pgvector para busca
- **Chatbot Inteligente**: Interface de conversação que permite fazer perguntas sobre o conteúdo dos documentos ingeridos
- **Busca Semântica**: Encontra as informações mais relevantes para responder às perguntas do usuário

### Arquitetura do Sistema

O projeto é composto por três componentes principais:

1. **`ingest.py`**: Script responsável pela ingestão e processamento de documentos PDF
2. **`search.py`**: Módulo de busca semântica que localiza informações relevantes
3. **`chat.py`**: Interface de chat que integra busca e geração de respostas

### Tecnologias Utilizadas

- **LangChain**: Framework para desenvolvimento de aplicações de IA
- **OpenAI API**: Modelos de embeddings e geração de texto
- **Google Gemini**: API alternativa para processamento de linguagem natural
- **PostgreSQL + pgvector**: Banco de dados com suporte a busca vetorial
- **PyPDF**: Processamento de documentos PDF
- **Docker**: Containerização do banco de dados

## Configuração do Ambiente

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar as dependências:**

   **Opção A - A partir do `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

   **Opção B - Instalação direta dos pacotes principais:**
   ```bash
   pip install langchain langchain-openai langchain-google-genai langchain-community langchain-text-splitters langchain-postgres psycopg[binary] python-dotenv beautifulsoup4 pypdf && pip freeze > requirements.txt
   ```
   Este comando também instalará todas as dependências automaticamente e gerará o arquivo `requirements.txt`.

3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais obtidas conforme instruções abaixo

## Requisitos para Execução dos Códigos

Para executar os códigos fornecidos no curso, é necessário criar chaves de API (API Keys) para os serviços da OpenAI e do Google Gemini. 

**Nota:** Certifique-se de não compartilhar suas chaves de API publicamente e de armazená-las em locais seguros, pois elas concedem acesso aos serviços correspondentes.

## Ordem de execução

1. **Subir o banco de dados:**
   docker compose up -d

2. **Executar ingestão do PDF:**
   python src/ingest.py

3. **Rodar o chat:**
   python src/chat.py 