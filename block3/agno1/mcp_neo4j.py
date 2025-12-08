import os
import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama

from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters

from instrumentation import instrument
instrument(service_name="agno-mcp", service_version="0.0.1", project_name="agno-mcp")

NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "test1234"
NEO4J_DATABASE = "neo4j"


server_params = StdioServerParameters(
    command="uvx",
    args=["mcp-neo4j-cypher@0.3.0", "--transport", "stdio"], #"streamable-http"
    env={
        "NEO4J_URI": os.getenv("NEO4J_URI", NEO4J_URI),
        "NEO4J_USERNAME": os.getenv("NEO4J_USERNAME", NEO4J_USERNAME),
        "NEO4J_PASSWORD": os.getenv("NEO4J_PASSWORD", NEO4J_PASSWORD),
        "NEO4J_DATABASE": os.getenv("NEO4J_DATABASE", NEO4J_DATABASE),
        },
    ) 

neo4j_mcp_server = MCPTools(server_params=server_params)

model = Ollama(id="qwen3-coder:480b-cloud") # use a strong model for generating cypher queries

async def run(message):

    try:
        
        await neo4j_mcp_server.connect()

        agent = Agent(
            name="SoftwareArchitect",
            role="An AI agent that answers questions about software programms.",
            model=model,
            tools=[neo4j_mcp_server], 
            instructions=["You are a software architect specialized in anylyzing a software systems."
                            "Answer questions helpfully.",
                            "Use always neo4j mcp server as tool for your research to answer questions about a software system.",
                            "You are in readonly mode, don't modify, create or remove any files or databases."]
        )
        await agent.aprint_response(message, stream=True)
    
    finally:
        await neo4j_mcp_server.close()



#message = "show me all applications that use the TextAtom from UI library"
#message = "how many bmw specific libraries contains each application of the software system?"

message = "how many applications contains the software system and how many classes do each application uses?"

if __name__ == "__main__":
    asyncio.run(run(message=message))
