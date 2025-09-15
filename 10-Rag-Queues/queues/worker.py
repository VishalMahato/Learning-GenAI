from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()
openai_client = OpenAI()

# ingestion - vector embedding
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)
# connection to vector db
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

def build_context(results):
    chunks = []
    for r in results:
        page = (
            r.metadata.get("page_label")
            or r.metadata.get("page")
            or r.metadata.get("loc", {}).get("page")
            or "NA"
        )
        src = r.metadata.get("source") or r.metadata.get("file_path") or "unknown"
        chunks.append(
            f"Page Content: {r.page_content}\n"
            f"Page Number: {page}\n"
            f"File Location: {src}"
        )
    return "\n\n\n".join(chunks)


def process_query(query:str):
    print("Searching Chunks ", query)

    search_results = vector_db.similarity_search(query=query, k=6)
    context = build_context(search_results)
    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant who answers the user's query based ONLY on the provided context retrieved from PDF files (with page contents and page numbers).
    Always cite the most relevant page numbers and point the user to the right pages to learn more.

    Context:
    {context}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
                {"role":"system", "content":SYSTEM_PROMPT },
                {"role" : "user", "content": query}
            ],
    )
    output = response.choices[0].message.content

    print(f"🤖 " ,output)
    return output

