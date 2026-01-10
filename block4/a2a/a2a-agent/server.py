######## Travel Agent ########
from a2a.server.apps import A2AFastAPIApplication
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from agent_executer import AgnoAgentExecutor

from agents import TravelPlannerAgent

AGENT_NAME = "travel planner agent"
AGENT_DESCRIPTION ="travel planner"

if __name__ == "__main__":

    agent_skill = AgentSkill(
        id='travel_planner',
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        tags=['travel planner'],
        examples=['hello', 'nice to meet you!'],
    )

    agent_card = AgentCard(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        url='http://localhost:10001/',  #This should be linked with ADN later?
        version='0.0.1',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[agent_skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=AgnoAgentExecutor(TravelPlannerAgent()),
        task_store=InMemoryTaskStore(),
    )

    server = A2AFastAPIApplication(
        agent_card=agent_card,
        http_handler=request_handler,
        )
    
    import uvicorn

    uvicorn.run(server.build(), host="0.0.0.0", port=10001)