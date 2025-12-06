import os

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.yfinance import YFinanceTools # needs pip install yfinance

from instrumentation import instrument
instrument(service_name="my-agno-trader", service_version="0.0.1", 
           project_name="my-agno-trader-project")

model = Ollama(id="granite4:3b")

def buy_stocks(amount: int, symbol: str):
    """
    Use this function for buying stocks
    
    :param amount: amount of stocks to buy
    :type amount: int
    :param symbol: stock symbol
    :type symbol: str
    """
    print(f"i will buy {amount} stocks of {symbol}!")

agent = Agent(model=model,
              instructions=["You are a trader agent always helping users to trade stocks."],
              tools=[YFinanceTools(), buy_stocks])

agent.print_response("Buy 5 stocks of Apple.")