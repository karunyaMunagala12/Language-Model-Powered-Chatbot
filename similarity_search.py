from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import pinecone 
from langchain_pinecone import PineconeVectorStore
import os
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

mapping_file_path = 'image_s3_locations.csv'
video_df = pd.read_csv("video_link_map.csv")
df = pd.read_csv(mapping_file_path)
image_to_url_map = pd.Series(df['S3 Location'].values, index=df['Image Name']).to_dict()
video_link_map = pd.Series(video_df["youtube_link"].values, index = video_df["video_file_name"]).to_dict()


from dotenv import load_dotenv
load_dotenv()

embeddings=OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
api_key = os.environ.get('PINECONE_API_KEY')
environment = os.environ.get('PINECONE_ENVIRONMENT') or 'PINECONE_ENVIRONMENT'

# configure client
pc = pinecone.Pinecone(api_key=api_key)
index_name = 'ddm-eta'
index = pc.Index(index_name)
text_field = "text"  

# initialize the vector store object
vectorstore = PineconeVectorStore(
    index, embeddings, text_field
)

def augment_prompt(query: str):
    # get top 3 results from knowledge base
    results = vectorstore.similarity_search(query, k=3, namespace = "lecture_content")
    # get the text from the results
    source_knowledge = "\n".join([x.page_content for x in results])
    # feed into an augmented prompt
    augmented_prompt = f"""Using the contexts below, answer the query.

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augmented_prompt



from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)



messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
    HumanMessage(content="I'd like to understand Foundations of Data Management.")
]


chat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo'
)

def get_image_source(query):
    image_data = vectorstore.similarity_search(query, k=1, namespace = "image_content")
    # get the text from the results
    image_name = image_data[0].metadata["source"]
    parts = image_name.split('-')

    # Extract the topic name (left of the hyphen)
    topic_name = parts[0].strip()

    print("\n\nTopic Name : " + topic_name)

    # Extract the slide number (right of the hyphen) and remove the ".png" extension
    slide_number = parts[1].rstrip('.png')

    print("\nSlide Number : " + slide_number + "\n\n")

    image_url = image_to_url_map[image_name]

    return image_url

def get_timestamp(query):
    transcript_info = vectorstore.similarity_search(query, k=1, namespace = "lecture_transcripts")
    video_source = transcript_info[0].metadata["source"]
    timestamp = transcript_info[0].metadata["timestamp"]
    video_link = video_link_map[video_source]

    hours, minutes, seconds = map(int, timestamp.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds

    timestamped_url = f"{video_link}?t={total_seconds}&autoplay=1"


    return timestamped_url


while True:
    query = input("\n\nQuery: ")
    if query == 'exit':
        break
    # create a new user prompt
    prompt = HumanMessage(
        content=augment_prompt(query)
    )
    # add to messages
    messages.append(prompt)

    res = chat.invoke(messages)

    # ans = AIMessage(content = res)

    print(res.content)

    image_url = get_image_source(query)
    # Fetch the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Display the image
    img.show()

    video_url = get_timestamp(query)
    print(video_url)