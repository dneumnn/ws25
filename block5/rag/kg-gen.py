###### KG Gen #####
from kg_gen import KGGen



import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia(user_agent='GraphRAG Project Reutlingen University (dominik.marc.neumann@icloud.com)', language='en')
page = wiki_wiki.page('Albert Einstein')

import pdb; pdb.set_trace()

# Initialize KGGen with optional configuration
kg = KGGen(
  model="ollama_chat/devstral-2:123b-cloud", 
  temperature=0.0,        # Default temperature
)

"""
            input_data: Text string or list of message dicts
            model: Name of OpenAI model to use
            api_key (str): OpenAI API key for making model calls
            chunk_size: Max size of text chunks in characters to process
            context: Description of data context
            output_folder: Path to save partial progress
"""
output_folder = "./graph"
graph = kg.generate(
  input_data=page.text,
  context="Family relationships",
  output_folder=output_folder
)

KGGen.visualize(graph, output_path="./test.html", open_in_browser=True)