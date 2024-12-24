from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import re
import json

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata
    
    def __repr__(self):
        return f"Document(page_content='{self.page_content[:50]}...', metadata={self.metadata})"

def read_doc(file_paths: List[str]) -> List[Document]:
    documents = []
    for path in file_paths:
        with open(path, 'r') as file:
            content = file.read()
            slides = content.split("Slide Number:")
            print(f"Reading {path}: found {len(slides)-1} slides")
            for slide in slides[1:]:
                slide_number, *slide_content = slide.split("\n", 1)
                slide_content = slide_content[0] if slide_content else ""
                documents.append(Document(
                    page_content=slide_content.strip(),
                    metadata={
                        'source': path.split('/')[-1], 
                        'page': slide_number.strip()
                    }
                ))
    return documents

def read_json(file_paths: List[str]) -> List[Document]:
    documents = []
    for path in file_paths:
        with open(path, 'r') as file:
            slides = json.load(file)
            # content = file.read()
            # slides = content.split("Slide Number:")
            # print(f"Reading {path}: found {len(slides)-1} slides")
            for image_name, content in slides.items():
                # slide_number, *slide_content = slide.split("\n", 1)
                # slide_content = slide_content[0] if slide_content else ""
                documents.append(Document(
                    page_content=content,
                    metadata={
                        'source': image_name,
                    }
                ))
    return documents


def chunk_data(docs: List[Document], chunk_size: int = 800, chunk_overlap: int = 50) -> Dict[str, List[Document]]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks_per_file = {}
    for doc in docs:
        source = doc.metadata['source']
        if source not in chunks_per_file:
            chunks_per_file[source] = []
        chunks_per_file[source] += text_splitter.split_documents([doc])
    
    for source, chunks in chunks_per_file.items():
        print(f"Total chunks created for {source}: {len(chunks)}")
    return chunks_per_file

def clean_document_content(docs: Dict[str, List[Document]]) -> Dict[str, List[Document]]:
    for source, documents in docs.items():
        for doc in documents:
            doc.page_content = re.sub(r'\n+', '\n', doc.page_content).strip()
        print(f"Cleaning completed for {source}.")
    return docs
import os

def list_text_files(base_dir):
    text_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.txt'):
                text_files.append(os.path.join(root, file))
    return text_files

def list_json_files(base_dir):
    json_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

file_paths = list_text_files("Lecture_Notes") + ["syllabus.txt"]

docs = read_doc(file_paths)
chunks_per_file_docs = chunk_data(docs)

cleaned_docs_per_file = clean_document_content(chunks_per_file_docs)

json_paths = list_json_files("Lecture_Notes")

jsons = read_json(json_paths)
chunks_per_file_json = chunk_data(jsons)

# # Display metadata and cleaned content for the first 3 slides of each file
# for source, documents in cleaned_docs_per_file.items():
#     print(f"\nMetadata and cleaned content for the first 3 slides of {source}:")
#     for i, doc in enumerate(documents[:3]):
#         print(f"\nSlide {i+1} Metadata: {doc.metadata}")
#         print(f"Cleaned Content Preview: {doc.page_content[:100]}...")

# print(cleaned_docs_per_file['HadoopHDFS.txt'][5])
        
from langchain_openai import OpenAIEmbeddings
import pinecone 
from langchain_pinecone import PineconeVectorStore
import time
from dotenv import load_dotenv
load_dotenv()
import os 

## Embedding Technique Of OPENAI
embeddings=OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
# print(embeddings)
# initialize connection to pinecone (get API key at app.pc.io)
api_key = os.environ.get('PINECONE_API_KEY')
environment = os.environ.get('PINECONE_ENVIRONMENT') or 'PINECONE_ENVIRONMENT'

# configure client
pc = pinecone.Pinecone(api_key=api_key)
index_name = 'ddm-eta'
index = pc.Index(index_name)
# pc.Index(name=index_name).create_namespace(namespace="lecture_content")
# pc.Index(name=index_name).create_namespace(namespace="image_content")
# wait a moment for connection
time.sleep(1)

print(index.describe_index_stats())

from tqdm.auto import tqdm  # for progress bar
import uuid

batch_size = 100

dataset = cleaned_docs_per_file
for i in dataset:
    data = dataset[i]
    for i in tqdm(range(0, len(data), batch_size)):
        i_end = min(len(data), i+batch_size)
        # get batch of data
        batch = data[i:i_end]
        # generate unique ids for each chunk
        ids = [str(uuid.uuid4()) for _ in batch]
        # get text to embed
        texts = [x.page_content for x in batch]
        # embed text
        embeds = embeddings.embed_documents(texts)
        # get metadata to store in Pinecone
        metadata = [
            {'text': x.page_content,
             'source': x.metadata['source'],
             'page': x.metadata['page']} for x in batch
        ]
        # add to Pinecone
        index.upsert(vectors=zip(ids, embeds, metadata), namespace="lecture_content")

image_dataset = chunks_per_file_json

for i in image_dataset:
    image_data = image_dataset[i]
    for i in tqdm(range(0, len(image_data), batch_size)):
        i_end = min(len(image_data), i+batch_size)
        # get batch of data
        batch = image_data[i:i_end]
        # generate unique ids for each chunk
        ids = [str(uuid.uuid4()) for _ in batch]
        # get text to embed
        texts = [x.page_content for x in batch]
        # embed text
        embeds = embeddings.embed_documents(texts)
        # get metadata to store in Pinecone
        metadata = [
            {'text': x.page_content,
             'source': x.metadata['source']} for x in batch
        ]
        # add to Pinecone
        index.upsert(vectors=zip(ids, embeds, metadata), namespace="image_content")
