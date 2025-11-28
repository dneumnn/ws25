###############################################################################
#
# Agents are AI programs where a language model controls the flow of execution.
#
# The core of an Agent is a model (LLM) with access to tools, guided by 
# instructions:
# - Model: the LLM controlling the flow of execution. It decides when to 
#          reason, use tools or respond.
# - Instructions: prompts guiding the model on how to use tools and respond.
# - Tools: enable Agents to take actions and interact with external systems.
###############################################################################

import os

from agno.agent import Agent
from agno.models.ollama import Ollama

from instrumentation import instrument
instrument(service_name="stock-trader-service", service_version="0.0.1", project_name="stock-trader")

from broker import sent_order_to_broker

model = Ollama(id=os.getenv("MODEL_ID", "granite4:3b"))

trader_agent = Agent(model=model,
              name="Stock Trader",
              instructions=['You are a stock trader agent'],
              tools=[sent_order_to_broker],
              )

trader_agent.print_response("Please buy 5 stocks of Apple")

