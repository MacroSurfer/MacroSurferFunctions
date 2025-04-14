from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from macrosurfer.database import Database

class QueryAgent:
    def __init__(self, database: Database, llm: ChatOpenAI):
        self.__db = database
        self.__llm = llm
        db = SQLDatabase(engine=self.__db.get_engine())
        self.__toolkit = SQLDatabaseToolkit(db=db, llm=self.__llm)

    def query(self, question: str) -> str:
        
        agent = create_sql_agent(
            llm=self.__llm,
            toolkit=self.__toolkit,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

        return agent.run(question)
