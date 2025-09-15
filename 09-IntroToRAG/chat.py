from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient  # (optional, kept as-is)
from dotenv import load_dotenv
from openai import OpenAI

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

# keep prior (user, assistant) turns; system is injected fresh each loop
message_history = []

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

while True:
    # take user input
    user_query = input("Ask Something > ").strip()
    if not user_query:
        continue

    # vector similarity search
    search_results = vector_db.similarity_search(query=user_query, k=6)

    # build context from latest search results
    context = build_context(search_results)

    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant who answers the user's query based ONLY on the provided context retrieved from PDF files (with page contents and page numbers).
    Always cite the most relevant page numbers and point the user to the right pages to learn more.

    Context:
    {context}
    """

    # Build the message list for this turn: fresh system prompt + prior history + new user turn
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + message_history + [
        {"role": "user", "content": user_query}
    ]

    response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
    )
    output = response.choices[0].message.content

    print(output)

    # Persist convo history (without the system prompt)
    message_history.extend(
        [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": output},
        ]
    )
