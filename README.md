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