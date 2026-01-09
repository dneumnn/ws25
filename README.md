# Intelligente Informationssysteme mit Python

Wahlfach im Wintersemester WI Master Hochschule Reutlingen und Knowledge Foundation PSE Jahrgang 2024

Intelligent information systems expand traditional information systems with AI components. Generative Artificial Intelligence (also known as GenAI) plays a particularly important role here. With its help, traditional information systems can be expanded to include natural language processing and understanding, as well as reasoning. As a result, machine learning takes a back seat and information systems are expanded and redesigned with existing AI components. 

The lecture focuses on the design principles of intelligent information systems. A basic understanding of relevant fundamentals from NLP, Neural Networks, and Transformer Architecture as the basis for Large Language Models is provided at the beginning. 

The lecture covers practical examples and current frameworks. Students can apply the knowledge they have acquired to the development of an intelligent information system.

## Installation

We use different python environments for each lesson.

### block1: neural networks and deep learning

The first lesson starts with an introduction into python, pytorch and neural networks.

```bash
conda create --name ws25_1 python=3.12
conda activate ws25_1
pip install jupyter numpy torch matplotlib pandas scikit-learn
```

goto block1 and start jupyter notebook.

```bash
conda activate ws25_1
cd block1
jupyter notebook
```

### block2: large language model and computer vision

#### Language Models

```bash
conda create --name ws25_2 python=3.12
conda activate ws25_2
pip install jupyter
pip install nltk
```

#### Large Language Models with Transformer

```bash
conda create --name ws25_3 python=3.12
conda activate ws25_3
pip install jupyter
pip install torch transformer tiktoken
```

#### ConversationalAI with Chainlit and Ollama

```bash
conda create --name ws25_4 python=3.12
conda activate ws25_4
pip install chainlit ollama
cd convAI
```

### block3: agentic ai

```bash
conda create --name ws25_5 python=3.12
conda activate ws25_5
pip install jupyter
pip install torch transformers
pip install accelerate
pip install torchvision numpy
```

#### Agents with Agno

<https://github.com/agno-agi/agno>

```bash
conda create --name ws25_6 python=3.12
conda activate ws25_6
pip install agno
cd agno
```

#### MCP

<https://gofastmcp.com/getting-started/quickstart>

```bash
conda create --name ws25_7 python=3.12
conda activate ws25_7
pip install fastmcp
cd mcp
```


#### Agent2

```bash
conda create --name agent2 python=3.12
conda activate agent2
pip install agno ollama
pip install yfinance
cd agno
```

### block4: agentic infrastructure

```bash
conda create --name agntcy python=3.13
conda activate agntcy
```

#### wsgi

- <https://wsgi.readthedocs.io/en/latest/index.html>
- <https://gunicorn.org>

```bash
pip install gunicorn
pip install requests
````

Start server at <http://127.0.0.1:8000>

```bash
cd wsgi
gunicorn main:app
```

#### asgi

ASGI (Asynchronous Server Gateway Interface) is a spiritual successor to WSGI, intended to provide a standard interface between async-capable Python web servers, frameworks, and applications.

- <https://asgi.readthedocs.io/en/latest/>
- <https://uvicorn.dev>

```bash
pip install uvicorn
pip install requests
````

Start server at <http://127.0.0.1:8000>

```bash
cd asgi
uvicorn main:app
```

#### asyncio

cd asyncio

#### a2a

### block5:

#### predictive coding theory

prdictive coding theory offers a unified theory that bridges numerous aspects of brain function, from perception and motor control to learning and memory.

Furthermore, predictive coding has significant implications for artificial intelligence and machine learning, providing insights into how algorithms might mimic human learning and perception.

At the heart of predictive coding lies a fundamental concept: the brain constructs internal representations of the world to predict sensory inputs, and these predictions are continuously updated based on sensory feedback.

The mathematical intuition behind this process is encapsulated in the model’s loss function, which quantifies the discrepancy between the predicted sensory inputs and the actual sensory inputs received by the brain.

The loss function in predictive coding is often conceptualized as the sum of prediction errors across different levels of a hierarchical system

Each level of this hierarchy makes predictions about the level below, and discrepancies between predictions and actual observations are fed back up the hierarchy to update and refine the predictions. This process is driven by the goal of minimizing the overall prediction error across the system.

We use the predictive_coding library found at: <https://github.com/Bogacz-Group/PredictiveCoding.git> which is based on <https://github.com/YuhangSong/Prospective-Configuration>.

and move the library your repo.

```bash
conda create --name ws25_8 python=3.12
conda activate ws25_8
pip install jupyter 
pip install torch torchvision matplotlib tqdm pandas seaborn
pip install scikit-learn

```

#### Retrieval Augmented Generation

```bash
conda create --name ws25_9 python=3.12
conda activate ws25_9
pip install jupyter 
pip install chromadb
pip install llama-index
pip install llama-index-readers-web
pip install llama-index-embeddings-ollama
pip install llama_index-embeddings-huggingface
pip install llama-index-llms-ollama
pip install llama-index-vector-stores-chroma
pip install requests
pip install beautifulsoup4

pip install wikipedia-api
```
