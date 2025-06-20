import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain_core.tools import create_retriever_tool
import logging

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Configure logging for MediBlaze medical bot
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [MediBlaze] %(message)s'
)
logger = logging.getLogger(__name__)

# Configure DuckDuckGo search for medical queries only
wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
duckduckgo_search = DuckDuckGoSearchResults(api_wrapper=wrapper)

@tool
def medical_web_search(query: str) -> str:
    """
    🔍 Search the web for comprehensive medical, health, and wellness information.
    Use this for ALL health-related topics including:
    - Medical conditions, diseases, symptoms, treatments
    - Nutrition, diet, lifestyle, fitness, and wellness
    - Mental health, hygiene, preventive care
    - Health trends, research, and general health questions
    - Topics where current, diverse medical perspectives would be valuable
    This tool provides broader, up-to-date health information beyond the knowledge base.
    """
    try:        # Enhance search query for better health results
        medical_query = f"{query} health medical wellness site:who.int OR site:mayoclinic.org OR site:webmd.com OR site:healthline.com OR site:medlineplus.gov OR site:cdc.gov OR site:nih.gov"
        logger.info(f"🔍 [MediBlaze] Executing medical web search for: {query}")
        
        # Indicate search is happening
        search_indicator = "🔍 **Searching web for latest medical information...**\n\n"
        
        results = duckduckgo_search.invoke(medical_query)
        
        if not results or len(str(results).strip()) < 20:
            logger.warning("⚠️ [MediBlaze] No relevant medical web results found")
            return f"{search_indicator}I couldn't find current web information about that health topic. Please consult with a healthcare professional for the most accurate information."
        
        logger.info("✅ [MediBlaze] Medical web search completed successfully")
        return f"{search_indicator}**🌐 Latest Health Information from Web:**\n\n{results}"
        
    except Exception as e:
        logger.error(f"❌ [MediBlaze] Error during medical web search: {str(e)}")
        return "⚠️ An error occurred while searching for health information online. Please try again or consult with a healthcare professional."

@tool
def rag_tool(query: str) -> str:
    """
    📚 Retrieve relevant health information from the MediBlaze knowledge base.
    This contains comprehensive medical documents and health information covering diseases, treatments, symptoms, and wellness.
    """
    try:
        logger.info("🔧 [MediBlaze] Initializing health knowledge embeddings...")
        embeddings = PineconeEmbeddings(model="multilingual-e5-large")
        
        index_name = "mediblaze-bot"
        logger.info(f"🔗 [MediBlaze] Connecting to health knowledge base: {index_name}")
        
        # Connect to Pinecone health knowledge base
        vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=embeddings,
            pinecone_api_key=PINECONE_API_KEY
        )
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": 7})  # Get more relevant health docs
        
        _rag_tool_instance = create_retriever_tool(
            retriever,
            "search_health_knowledge_base",
            "🏥 Searches MediBlaze health knowledge base for comprehensive information about diseases, treatments, medications, symptoms, prevention, diagnosis, lifestyle health, and wellness information."
        )
        
        logger.info(f"📖 [MediBlaze] Executing health knowledge search for: {query}")
        result = _rag_tool_instance.invoke(query)        
        # If no relevant results found, provide helpful fallback
        if not result or len(str(result).strip()) < 20:
            logger.warning("⚠️ [MediBlaze] No relevant results found in health knowledge base")
            return "📚 I couldn't find specific information about that in our health knowledge base. Let me search for current health information online to help you better."
        
        logger.info("✅ [MediBlaze] Health knowledge search completed successfully")
        return f"**📚 From MediBlaze Health Knowledge Base:**\n\n{result}"
    
    except Exception as e:
        logger.error(f"❌ [MediBlaze] Error during health knowledge search: {str(e)}")
        return "⚠️ An error occurred while searching our health knowledge base. Please try again or ask a different health question."