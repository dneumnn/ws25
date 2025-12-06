import os

import chainlit as cl

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.yfinance import YFinanceTools # needs pip install yfinance
from agno.tools.reasoning import ReasoningTools

from agno.db.in_memory import InMemoryDb

from instrumentation import instrument
instrument(service_name="stock-trader-service", service_version="0.0.1", project_name="stock-trader")

from broker import sent_order_to_broker


# Global variables
agent = None

@cl.on_chat_start
async def on_chat_start():
    """Initialize the agent when a new chat session starts."""
    model = Ollama(id=os.getenv("MODEL_ID", "granite4:3b"))

    db = InMemoryDb()

    agent = Agent(model=model,
              name="Stock Trader",
              instructions=['You are a stock trader agent', 
                            'If stock price > limit place order with limit'],
              tools=[YFinanceTools(), sent_order_to_broker],
              stream=True,
              markdown=True,
              db=db,
              add_history_to_context=True,
              num_history_runs=5,
              )

    # Store the agent in the session
    cl.user_session.set("agent", agent)


@cl.on_message
async def on_message(message: cl.Message):
    # Get the agent from the session
    agent = cl.user_session.get("agent")

    response_msg = cl.Message(content="")
    await response_msg.send()

    async for event in agent.arun(message.content, stream=True):
        response_msg.content += event.content
        await response_msg.update()


#if __name__ == "__main__":
#    cl.run_chainlit(__file__)