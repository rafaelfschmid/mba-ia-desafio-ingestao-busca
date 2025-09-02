import os
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector


from dotenv import load_dotenv
load_dotenv()

session_store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


@tool("document_search")
def document_search(query: str) -> dict[str, str]:
  """
  Runnable tool to search the database
  """
  embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

  store = PGVector(
      embeddings=embeddings,
      collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
      connection=os.getenv("DATABASE_URL"),
      use_jsonb=True,
  )
  docs = store.similarity_search_with_score(query, k=2)
  
  if not docs:
      err = "No documents found for this query."
      print(err)
      return err
  
  return docs

def prepare_inputs(payload: dict) -> dict:
  input = payload.get("input", "")
  raw_history = payload.get("raw_history", [])
  
  print(f"🔍 Input: {input}")
  print(f"📚 Raw history length: {len(raw_history)}")
  print(f"📚 Raw history: {raw_history}")
      
  trimmed = trim_messages(
      raw_history,
      token_counter = len,
      max_tokens=3,
      strategy="last",
      start_on="human",
      include_system=True,
      allow_partial=False,
  )

  docs = document_search.invoke(input = input)
  prepared_docs = "\n\n".join([f"Document:{doc.id} (Score: {score:.2f}): {doc.page_content}" for i, (doc, score) in enumerate(docs)])

  return {"pergunta": input, "contexto": prepared_docs, "history": trimmed}


prompt = ChatPromptTemplate.from_messages([
    ("system", PROMPT_TEMPLATE),
    MessagesPlaceholder(variable_name="history"),
    ("human", "Pergunta: {pergunta}\n\nContexto: {contexto}")
])

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-5-nano"), temperature=0) 

prepare = RunnableLambda(prepare_inputs)
chain = prepare | prompt | llm

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="raw_history",
    output_messages_key="output"
)

def search_prompt(query):
    config = {"configurable": {"session_id": "demo-session"}}
    result = conversational_chain.invoke({"input": query}, config=config)
    return result.content

    