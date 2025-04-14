import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from macrosurfer.database import Database
from dotenv import load_dotenv
from macrosurfer.agent.query_agent import QueryAgent
load_dotenv()

db = Database()

# Load environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Create LLM (you can switch to any model)
llm = ChatOpenAI(temperature=0, model="gpt-4o")

# Create SQL Agent
query_agent = QueryAgent(db, llm)

# Run your agent
question = "What are some economic events coming up next week in the US?"
response = query_agent.query(question)

print(response)
