import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, \
    ScrapeWebsiteTool, RagTool
from langchain_openai import OpenAIEmbeddings  # Or a different embedding model
from langchain_community.document_loaders import PyPDFLoader, TextLoader, \
    DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

MAX_ITERATIONS = 5
TEMPERATURE = 1
TOP_P = 0.9

DATA_DIR = './data'
CHROMA_DB_PATH = './chroma_db'

embeddings = OpenAIEmbeddings()

# Define the tools used by the agents
huggingface_docs_tool = DirectoryReadTool(directory='./data/HuggingFace')
openai_docs_tool = DirectoryReadTool(directory='./data/OpenAI')
google_docs_tool = DirectoryReadTool(directory='./data/Google')
meta_docs_tool = DirectoryReadTool(directory='./data/Google')
docs_tool = openai_docs_tool

file_tool = FileReadTool()
search_tool = SerperDevTool()
# web_rag_tool = WebsiteSearchTool()
scrape_tool = ScrapeWebsiteTool()


def load_and_process_documents(data_dir, chroma_db_path):
    """
    Loads documents from a directory, chunks them, and stores them in a ChromaDB vector store.
    Returns a LangChain retriever.
    """
    if os.path.exists(chroma_db_path) and os.listdir(chroma_db_path):
        print("ChromaDB already exists. Loading existing vector store.")
        vectorstore = Chroma(persist_directory=chroma_db_path,
                             embedding_function=embeddings)
    else:
        print("Creating ChromaDB from documents...")
        documents = []

        # Load all .txt files
        text_loader = DirectoryLoader(data_dir, glob="**/*.txt",
                                      loader_cls=TextLoader)
        documents.extend(text_loader.load())

        # Load all .pdf files
        pdf_loader = DirectoryLoader(data_dir, glob="**/*.pdf",
                                     loader_cls=PyPDFLoader)
        documents.extend(pdf_loader.load())

        if not documents:
            print(
                f"No documents found in {data_dir}. Please ensure files are "
                f"present.")
            return None

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,
                                                       chunk_overlap=256)
        chunks = text_splitter.split_documents(documents)
        print(
            f"Loaded {len(documents)} documents and split into {len(chunks)} "
            f"chunks.")

        # Create vector store and persist it
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=chroma_db_path
        )
        vectorstore.persist()
        print("ChromaDB created and persisted.")

    # Return a retriever from the vector store
    return vectorstore.as_retriever()


# --- Initialize Tools ---
# Set up the RAG tool using the vector store retriever
local_rag_retriever = load_and_process_documents(DATA_DIR, CHROMA_DB_PATH)

if not local_rag_retriever:
    raise Exception(
        "Failed to load or create document retriever. Ensure 'data' directory "
        "has files.")

rag_tool = RagTool(retriever=local_rag_retriever)

# Define the manager agent
manager = Agent(
    role="Coordinator",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced Coordinator, skilled in overseeing "
              "complex projects and guiding teams to success. Your role is "
              "to coordinate the efforts of all members, ensuring that"
              "each task is completed to the highest standard. You need to "
              "restrict yourself to company websites or open source websites. "
              "Avoid multimedia or links to non-text websites.",
    allow_delegation=True,
    max_iter=MAX_ITERATIONS,  # Maximum number of iterations for a final answer
)


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class OpInnoStrat():
    """OpInnoStrat crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def ceo(self) -> Agent:
        return Agent(
            config=self.agents_config['ceo'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            # tools=[docs_tool, search_tool, scrape_tool, file_tool,
            #        web_rag_tool],
            tools=[rag_tool, search_tool, scrape_tool],
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
        )

    @agent
    def cto(self) -> Agent:
        return Agent(
            config=self.agents_config['cto'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools=[rag_tool, search_tool, scrape_tool],
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
        )

    @agent
    def product_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['product_strategist'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools=[rag_tool, search_tool, scrape_tool],
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
        )

    @agent
    def product_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['product_designer'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools=[rag_tool, search_tool, scrape_tool],
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
        )

    @agent
    def coo(self) -> Agent:
        return Agent(
            config=self.agents_config['coo'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools=[rag_tool, search_tool, scrape_tool],
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
        )

    @agent
    def cmo(self) -> Agent:
        return Agent(
            config=self.agents_config['cmo'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools=[rag_tool, search_tool, scrape_tool],
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
        )

    @agent
    def qualitative_researcher1(self) -> Agent:
        return Agent(
            config=self.agents_config['qualitative_researcher1'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
            tools=[rag_tool, search_tool, scrape_tool],
        )

    @agent
    def qualitative_researcher2(self) -> Agent:
        return Agent(
            config=self.agents_config['qualitative_researcher2'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            max_iter=MAX_ITERATIONS,  # Max iterations for an agent
            tools=[rag_tool, search_tool, scrape_tool],
        )

    # TASKS

    @task
    def ceo_task(self) -> Task:
        return Task(
            config=self.tasks_config['ceo_task'],
            output_file='2. ceo.md'
        )

    @task
    def cto_task(self) -> Task:
        return Task(
            config=self.tasks_config['cto_task'],
            output_file='2. cto.md'
        )

    @task
    def product_strategist_task(self) -> Task:
        return Task(
            config=self.tasks_config['product_strategist_task'],
            output_file='2. product_strategy.md'
        )

    @task
    def product_designer_task(self) -> Task:
        return Task(
            config=self.tasks_config['product_designer_task'],
            output_file='2. product_designer.md'
        )

    @task
    def coo_task(self) -> Task:
        return Task(
            config=self.tasks_config['coo_task'],
            output_file='2. coo.md'
        )

    @task
    def cmo_task(self) -> Task:
        return Task(
            config=self.tasks_config['cmo_task'],
            output_file='2. cmo.md'
        )

    @task
    def qualitative_researcher_task1(self) -> Task:
        return Task(
            config=self.tasks_config['qualitative_researcher_task1'],
            output_file='3. qualitative_researcher-1.md'
        )

    @task
    def qualitative_researcher_task2(self) -> Task:
        return Task(
            config=self.tasks_config['qualitative_researcher_task2'],
            output_file='3. qualitative_researcher-2.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Open Innovation Strategy crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            # manager_agent=manager,
            verbose=True,
            respect_context_window=True,
            memory=True,  # Enable memory usage for enhanced task execution
            planning=True,  # Enable planning feature for pre-execution strategy
            cache=False
        )
