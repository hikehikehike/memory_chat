import os

from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from default_template import _DEFAULT_TEMPLATE


load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
llm = OpenAI(temperature=0)
memory_file = "memory_file.txt"


def create_documents_history():
    """Load documents from a file and split them into chunks of 1000 characters each.

    Returns:
        A list of strings, each representing a document chunk.
    """
    loader = TextLoader(memory_file)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    doc = text_splitter.split_documents(documents)
    return doc


def create_memory():
    """Create a memory object for a conversation chain.

    Returns:
        A tuple of (memory object, vector database object).
    """
    doc = create_documents_history()
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb = Chroma.from_documents(documents=doc, embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs=dict(k=1))
    memory = VectorStoreRetrieverMemory(retriever=retriever)

    return memory, vectordb


def conversation():
    """Create a conversation chain object.

    Returns:
        A tuple of (conversation chain object, vector database object).
    """
    memory, vectordb = create_memory()

    prompt = PromptTemplate(
        input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
    )
    conversation_with_summary = ConversationChain(
        llm=llm, prompt=prompt, memory=memory, verbose=True
    )

    return conversation_with_summary, vectordb


def save_history(history):
    """Save the conversation history to a file and append a summarized version of it.

    Args:
        history: A list of strings, each representing a message in the conversation history.
    """
    docs = [Document(page_content=t) for t in history]
    chain = load_summarize_chain(llm, chain_type="stuff")
    summarization = chain.run(docs)
    with open(memory_file, "a") as f:
        f.write(summarization + "\n")
