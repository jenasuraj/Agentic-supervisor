import hashlib
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()




DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file")




document = Document(
    page_content=os.getenv("DOC_TEXT_PROMPT"),
    metadata={
        "source": "in-memory-doc"
    }
)

text_splitter = RecursiveCharacterTextSplitter( chunk_size=500, chunk_overlap=50)
docs_split = text_splitter.split_documents([document])

primary_id = 1
for doc in docs_split:
    doc.metadata["id"] = primary_id
    primary_id += 1 

embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-mpnet-base-v2" )


vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_textbase",
    connection=DATABASE_URL,
    use_jsonb=True,
)



vector_store.add_documents( #when we pass ids, we are saying these has to be the PK, otherwise many times chunks gets loaded and tuple gets exceeded always, now only id's gets replaced only not added more .
    documents=docs_split,
    ids= [doc.metadata["id"]  for doc in docs_split])