<h1 align="center" style="font-size: 3em; color: #FFB703;">LLM-Powered Chatbot for Education</h1>

<p align="center">
  <img src="https://github.com/karunyaMunagala12/Language-Model-Powered-Chatbot/raw/main/Project%20Banner.png" alt="Project Banner" width="800">
</p>

---

<h2 style="color: #FFB703;">Project Overview</h2>
<p>
  This project focuses on developing an <strong>AI-driven chatbot</strong> for educational purposes, designed to function as a <em>Virtual Teaching Assistant</em>. Its primary goal is to address the limited availability of human TAs, ensuring students receive real-time support for their queries on assignments, lectures, and general coursework.
</p>

---

<h2 style="color: #FFB703;">Architecture Diagram</h2>
<p align="center">
  <img src="https://github.com/karunyaMunagala12/Language-Model-Powered-Chatbot/raw/main/Architecture%20Diagram.png" alt="Architecture Diagram" width="600">
</p>

---

<h2 style="color: #FFB703;">Key Features</h2>
<ul>
  <li><strong>Multi-Modal Query Handling</strong>: Text, audio, and vector-based retrieval.</li>
  <li><strong>Retrieval-Augmented Generation (RAG)</strong>: Combines LLM responses with vector-based search.</li>
  <li><strong>Pinecone Integration</strong>: Efficient vector data storage and retrieval.</li>
</ul>

---

<h2 style="color: #FFB703;">Methodology</h2>
<ol>
  <li><strong>Data Collection and Preprocessing</strong>:
    <ul>
      <li>Sources: Lecture notes, Zoom recordings, and forums.</li>
      <li>Text converted into vector embeddings using embedding models.</li>
    </ul>
  </li>
  <li><strong>Core Technologies</strong>:
    <ul>
      <li>LangChain for pipeline setup.</li>
      <li>Pinecone as vector storage.</li>
      <li>OpenAI API for query processing.</li>
    </ul>
  </li>
</ol>

---

<h2 style="color: #FFB703;">Directory Structure</h2>
<pre>
├── RAG_Chatbot.ipynb            # Jupyter Notebook for main chatbot implementation
├── generate_json.py             # Converts data into JSON format for processing
├── images_to_s3.py              # Handles S3 uploads for visual/audio content
├── lecture_notes_to_vector.py   # Converts lecture notes to vector embeddings
├── requirements.txt             # Python dependencies
├── similarity_search.py         # Finds relevant data chunks based on user query
├── text_to_chunks.py            # Breaks long text data into retrievable chunks
└── README.md                    # Project documentation
</pre>

---

<h2 style="color: #FFB703;">Installation and Setup</h2>
<p>To set up the environment locally, follow these steps:</p>

<ol>
  <li>Clone the repository:</li>
  <pre>
  git clone https://github.com/karunyaMunagala12/Language-Model-Powered-Chatbot.git
  cd Language-Model-Powered-Chatbot
  </pre>
  <li>Install dependencies:</li>
  <pre>
  pip install -r requirements.txt
  </pre>
  <li>Run the chatbot:</li>
  <pre>
  # Execute the RAG_Chatbot.ipynb notebook or launch scripts in the repository
  </pre>
</ol>

---

<h2 style="color: #FFB703;">Demo</h2>
<p>Watch the complete project in action: <a href="https://www.youtube.com/watch?v=PFBdbaRxvLU" target="_blank">YouTube Demo</a></p>

---

<h2 style="color: #FFB703;">Future Improvements</h2>
<ul>
  <li>Enhanced classification using advanced models.</li>
  <li>Expanded data sources for greater knowledge.</li>
  <li>Scalability for larger deployments.</li>
</ul>
