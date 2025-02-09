import argparse
import asyncio
import os
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
import groq
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Load environment variables
load_dotenv()

# Secure API Key Handling
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Error: Groq API key is missing. Set it in a .env file or environment variable.")

# Initialize Vector Database
db = chromadb.PersistentClient(path="./vector_db")
collection = db.get_or_create_collection(name="scraped_content")

# Initialize Embedding Model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize LLM Client
groq_client = groq.Client(api_key=GROQ_API_KEY)

async def scrape_website(url):
    """Scrapes text content from the given URL with error handling."""
    try:
        session = requests.Session()
        response = session.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Failed to fetch {url} (Status Code: {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p") if p.get_text()]
        content = "\n".join(paragraphs)

        return content if content else None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

async def store_in_vector_db(url, content):
    """Stores scraped content in ChromaDB with embeddings."""
    sentences = [s.strip() for s in content.split(". ") if s.strip()]
    
    if not sentences:
        print("No valid sentences found for storage.")
        return

    embeddings = embed_model.encode(sentences).tolist()
    collection.add(
        ids=[str(i) for i in range(len(sentences))],
        metadatas=[{"url": url} for _ in range(len(sentences))],
        embeddings=embeddings,
        documents=sentences
    )
    print(f"Stored {len(sentences)} sentences in the vector database.")

async def chatbot_query(user_query):
    """Retrieves relevant content from ChromaDB and generates an LLM response."""
    query_embedding = embed_model.encode([user_query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=3)

    if not results["documents"] or not results["metadatas"]:
        return "I'm sorry, but I couldn't find relevant information for your query."

    context = "\n".join(results["documents"][0])
    source_links = "\n".join(set([meta["url"] for meta in results["metadatas"][0]]))

    prompt = f"""
    Use the following context to answer the question:
    {context}
    
    User question: {user_query}
    """

    try:
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        chatbot_response = response.choices[0].message.content.strip()
        return f"{chatbot_response}\n\nSource: {source_links}"
    except Exception as e:
        return f"Error generating response: {e}"

async def main():
    parser = argparse.ArgumentParser(description="Web Scraper Chatbot")
    parser.add_argument("url", type=str, help="Website URL to scrape")
    args = parser.parse_args()

    print(f"Scraping website: {args.url}...")
    content = await scrape_website(args.url)

    if content:
        await store_in_vector_db(args.url, content)
        print("Scraped content stored successfully.")
    else:
        print("No content found. Exiting.")
        return

    while True:
        query = input("\nAsk your question (type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting chatbot.")
            break
        response = await chatbot_query(query)
        print("\nChatbot:", response)

if __name__ == "__main__":
    asyncio.run(main())
