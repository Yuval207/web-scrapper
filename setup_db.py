import chromadb

# Initialize ChromaDB Persistent Client
db = chromadb.PersistentClient(path="./vector_db")

# Create or get the collection
collection = db.get_or_create_collection(name="scraped_content")

print("Vector database initialized successfully!")
