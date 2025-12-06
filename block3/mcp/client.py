import asyncio
from fastmcp import Client
from fastmcp.client import StdioTransport

# ######## Remote Server #########
# client = Client("http://localhost:8000/mcp")

# ######## Local Server ##########
# "transport": "stdio",
# "command": "python",
# "args": ["./server.py", "--verbose"],
# "env": {"DEBUG": "true"},
# "cwd": "/path/to/server",

import os
cwd=os.getcwd()
print(cwd)

stdio = StdioTransport(command="python", cwd=f"{cwd}/block3/mcp", args=["server.py"])

client = Client(transport=stdio)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))