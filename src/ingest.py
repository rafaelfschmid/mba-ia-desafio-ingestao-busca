import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

def ingest_pdf():
    for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    print("📥 Starting PDF ingestion...")
    
    # Debug: Print the collection name being used
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    print(f"🔍 Using collection: {collection_name}")
    
    current_dir = Path(__file__).parent
    pdf_path = current_dir / ".." / os.getenv("PDF_PATH")

    docs = PyPDFLoader(str(pdf_path)).load()

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit(0)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]    

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

    print(f"📊 Adding {len(enriched)} documents to collection: {collection_name}")
    
    try:
        # Try to create a new store instance with explicit collection name
        print(f"🔍 Creating store with collection: {collection_name}")
        store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )
        
        print(f"🔍 Store created, now adding documents...")
        
        # Debug: Check what collection the store is actually using
        print(f"🔍 Store collection name: {store.collection_name}")
        print(f"🔍 Store collection metadata: {store.collection_metadata}")
        
        store.add_documents(documents=enriched, ids=ids)
        print(f"✅ Successfully ingested {len(enriched)} document chunks")
        
        # Verify the documents were added
        print(f"🔍 Verifying documents in collection: {collection_name}")
        verification_results = store.similarity_search("", k=1)
        print(f"📊 Found {len(verification_results)} documents in collection after ingestion")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    ingest_pdf()