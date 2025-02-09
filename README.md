# Web Scraper Chatbot with RAG & LLM

## Overview
This project is a full-stack web scraper that extracts content from a user-provided URL and enables a chatbot to answer queries based on the scraped data. The chatbot leverages **Retrieval-Augmented Generation (RAG)** using **ChromaDB** as a vector database and **Groq API** as the LLM.

## Features
- Scrapes text content from a given URL.
- Stores extracted content in a **vector database (ChromaDB)** for efficient retrieval.
- Implements **RAG** to retrieve relevant data and generate meaningful chatbot responses.
- Uses **Groq API** for LLM responses.
- Provides a **CLI interface** for user interaction.
- Includes **source citation** in chatbot responses.
- Optimized with **async & multi-threading** techniques.

---
## **Setup & Installation**
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/web-scraper-chatbot.git
cd web-scraper-chatbot
```

### **2. Create a Virtual Environment (Optional, but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate    # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the project directory and add your **Groq API Key**:
```bash
echo "GROQ_API_KEY=your_api_key" > .env
```

---
## **Vector Database (ChromaDB) Setup**
### **1. What is ChromaDB?**
ChromaDB is an open-source vector database used to efficiently store and retrieve text embeddings.

### **2. How to Initialize & Use ChromaDB?**
- Run this script once to set up the database:
```bash
python setup_db.py
```
- The script automatically initializes **ChromaDB** at `./vector_db`.
- Scraped content is stored as embeddings in the database.
- The chatbot queries ChromaDB to retrieve the most relevant information.
- To clear the database, delete the `vector_db/` folder:
```bash
rm -rf vector_db/
```

---
## **Usage**
### **1. Run the Web Scraper Chatbot**
```bash
python main.py <URL>
```
Example:
```bash
python main.py https://example.com
```

### **2. Ask the Chatbot Questions**
Once the scraping process is complete, you can chat with the bot.
```bash
Ask your question (type 'exit' to quit): What services does this company provide?
Chatbot: The company offers software development and cloud solutions. 

Source: https://example.com
```

---
## **Examples of Chatbot Responses**
**User:** "What does this company do?"

**Chatbot:** "The company specializes in AI and cloud computing solutions. 

Source: [example.com](https://example.com)"

---
## **Edge Cases Handled & Not Handled**
### ✅ **Handled:**
- Websites without `https` (auto-fallback to `http` if needed).
- Websites with JavaScript-rendered content (warns users that data might be incomplete).
- Handling `403`, `404`, and `500` errors gracefully.
- Duplicate content detection in ChromaDB.

### ❌ **Not Handled:**
- JavaScript-heavy sites that require Selenium for scraping.
- Websites with CAPTCHA protections.
- Multi-page scraping.



