# multi_agent/rag_agent.py
import chromadb
import google.generativeai as genai
import os
from google.adk.agents import Agent
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGService:
    """RAG service using ChromaDB and Google Gemini."""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )
        
        # Configure Google Generative AI
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(name="uniplexity_collection")
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def rag_answer(self, question: str, k: int = 1, model_name: str = "gemini-2.5-flash") -> Dict[str, Any]:
        """
        Perform RAG (Retrieval-Augmented Generation) to answer a question.
        
        Args:
            question: The user's question
            k: Number of documents to retrieve
            model_name: Name of the model to use
            
        Returns:
            Dictionary containing retrieved docs, model response, and raw response
        """
        # 1) Retrieve top-k docs from Chroma (Chroma will embed query_texts for you)
        results = self.collection.query(query_texts=[question], n_results=k)
        
        # Extract retrieved documents safely
        try:
            retrieved_docs = results['documents'][0]   # list of docs for the first query
        except Exception:
            # fallback: some clients return .documents
            retrieved_docs = getattr(results, "documents", [[]])[0]

        # join retrieved docs to include in prompt (limit size if necessary)
        joined_docs = "\n\n---\n\n".join(retrieved_docs) if retrieved_docs else ""

        # 2) Compose the RAG prompt for the model
        prompt = f"""You are an expert assistant. Use the retrieved documents below to answer the user's question.
If the documents don't contain enough info, say so and answer with what you can infer.

Retrieved documents:
{joined_docs}

User question:
{question}

Answer concisely and cite the document snippet you used (by quoting it).
"""

        # 3) Call Gemini to generate the final answer
        response = self.model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=512  # adjust as needed
            )
        )

        # Extract model response safely
        try:
            model_text = response.text
        except Exception:
            # some SDKs return a more nested structure
            model_text = getattr(response, "output", None) or str(response)

        return {
            "retrieved_docs": retrieved_docs,
            "model_response": model_text,
            "raw_response": response
        }


# Initialize RAG service instance
rag_service = RAGService()


def rag_search(question: str, k: int = 1) -> dict:
    """
    RAG search tool function for the agent.
    
    Args:
        question: The question to search for
        k: Number of documents to retrieve (default: 1)
        
    Returns:
        Dictionary with status and result
    """
    try:
        result = rag_service.rag_answer(question, k)
        return {
            "status": "success",
            "question": question,
            "retrieved_documents": result["retrieved_docs"],
            "answer": result["model_response"],
            "num_docs_retrieved": len(result["retrieved_docs"])
        }
    except Exception as e:
        return {
            "status": "error",
            "question": question,
            "error": str(e),
            "answer": f"Sorry, I encountered an error while searching for information about '{question}': {str(e)}"
        }


def add_document(content: str, metadata: Optional[dict] = None) -> dict:
    """
    Add a document to the RAG knowledge base.
    
    Args:
        content: The document content to add
        metadata: Optional metadata for the document
        
    Returns:
        Dictionary with status and result
    """
    try:
        # Generate a simple ID based on content hash or timestamp
        import hashlib
        import time
        doc_id = hashlib.md5(f"{content}_{time.time()}".encode()).hexdigest()
        
        # Add document to collection
        rag_service.collection.add(
            documents=[content],
            ids=[doc_id],
            metadatas=[metadata or {}]
        )
        
        return {
            "status": "success",
            "message": f"Document added successfully with ID: {doc_id}",
            "document_id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to add document: {str(e)}"
        }


# Create the RAG agent
root_agent = Agent(
    name="rag_agent",
    model="gemini-2.0-flash",
    description="Performs RAG (Retrieval-Augmented Generation) to answer questions using stored knowledge.",
    instruction="""You are a RAG (Retrieval-Augmented Generation) agent that can search through stored documents 
    to answer questions. Use the rag_search tool to find relevant information from the knowledge base and provide 
    comprehensive answers. You can also add new documents to the knowledge base using the add_document tool.
    
    When answering questions:
    1. Use rag_search to find relevant information
    2. Provide detailed answers based on the retrieved documents
    3. Cite the sources when possible
    4. If no relevant information is found, say so clearly
    """,
    tools=[rag_search, add_document],
)


# Example usage and testing
if __name__ == "__main__":
    # Test the RAG functionality
    question = "What is Uniplexity AI?"
    result = rag_search(question, k=1)
    
    print("=== RAG Search Result ===")
    print(f"Status: {result['status']}")
    print(f"Question: {result['question']}")
    
    if result['status'] == 'success':
        print(f"Number of documents retrieved: {result['num_docs_retrieved']}")
        print("\n=== Retrieved Documents ===")
        for i, doc in enumerate(result['retrieved_documents'], 1):
            print(f"Document {i}:")
            print(doc)
            print("---")
        
        print("\n=== Answer ===")
        print(result['answer'])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")