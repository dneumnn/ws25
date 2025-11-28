import os
import time
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools

from ddgs import DDGS

def ddg_search(query: str):
    """Uses DuckDuckGo search for searching web sites."""
    return retry_ddg(query, max_results=5) 

def retry_ddg(query, max_results=5, retries=3):
    for i in range(retries):
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                if results:
                    return results
        except:
            time.sleep(1)
    return []


from instrumentation import instrument
instrument(service_name="resoning-service", service_version="0.0.1", project_name="apple-report")

model = Ollama(id=os.getenv("MODEL_ID", "granite4:3b"))
 
agent = Agent(model=model,
              instructions=["Use duckduck go web search and yahoo finance tools for information retrieval.", "Only include the report in your response. No other text."],
              tools=[ReasoningTools(add_instructions=True),
                     YFinanceTools(),
                     ddg_search],
              markdown=True,
              )

agent.print_response("Write a report on Apple and IBM and analyze which company has the better large language model in place", 
                     show_full_reasoning=True,
                     stream_intermediate_steps=True)