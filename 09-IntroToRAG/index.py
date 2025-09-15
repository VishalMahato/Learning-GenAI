from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()
pdf_path= Path(__file__).parent / "../indian_law.pdf"

# loader
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# print(docs[0])

# chunking - spliting the doc
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents=docs)
# print(chunks)

# ingestion - vector embedding
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

qdrant = QdrantVectorStore.from_documents(
    embedding=embeddings,
    documents=chunks,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

