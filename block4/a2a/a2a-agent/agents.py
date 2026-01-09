import sys

from collections.abc import AsyncGenerator
from typing import Any

######## AGNO ########
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools

######## LOGGING #####
import logging
from pathlib import Path
from agno.utils.log import configure_agno_logging, log_info
custom_logger = logging.getLogger("file_logger")

# Ensure tmp directory exists
log_file_path = Path(".log/log.txt")
log_file_path.parent.mkdir(parents=True, exist_ok=True)

# Use FileHandler to write to file
handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.INFO)
custom_logger.propagate = False

# Configure Agno to use the file logger
configure_agno_logging(custom_default_logger=custom_logger)

####### INSTRUMENTATION #######
from instrumentation import instrument
instrument(service_name="a2a", service_version="0.0.1", project_name="a2a")

SYSTEM_MESSAGE = """
                You are an expert travel assistant specializing in trip planning, destination information, 
                and travel recommendations. Your goal is to help users plan enjoyable, safe, and 
                realistic trips based on their preferences and constraints.
                
                When providing information:
                - Be specific and practical with your advice
                - Consider seasonality, budget constraints, and travel logistics
                - Highlight cultural experiences and authentic local activities
                - Include practical travel tips relevant to the destination
                - Format information clearly with headings and bullet points when appropriate
                
                For itineraries:
                - Create realistic day-by-day plans that account for travel time between attractions
                - Balance popular tourist sites with off-the-beaten-path experiences
                - Include approximate timing and practical logistics
                - Suggest meal options highlighting local cuisine
                - Consider weather, local events, and opening hours in your planning
                
                Always maintain a helpful, enthusiastic but realistic tone and acknowledge 
                any limitations in your knowledge when appropriate.
                """


class TravelPlannerAgent:
    """Travel Planner Agent"""

    def __init__(self):
        """Initialize the model and the agent"""
        log_info("Initialize the Travel Planner Agent")
        try:
            self.model = Ollama(id="granite4:3b")
            self.agent = Agent(model=self.model,
                               instructions=[SYSTEM_MESSAGE],
                               tools=[DuckDuckGoTools(fixed_max_results=5, 
                                                      timeout=3, 
                                                      backend="duckduckgo")],
                               stream_events=False,
                               add_datetime_to_context=True)
            log_info(f'Model: {self.model.name}')
            log_info(f'Agent: {self.agent.name}')
        except Exception as e:
            log_info(f'Something went wrong: {e}')
            sys.exit()
            
    async def stream(self, query: str, **kwargs) -> AsyncGenerator[dict[str, Any], None]:
        """Stream the response of the model back to the client.
            How to handle sesson id, user id and memory? 
        """
        log_info(f'Stream: {query}')
        try:
            # Invoke the model in streaming mode to generate a response.
            async for output in self.agent.arun(input=query, stream=True):
                # Return AsyncIterator[RunOutputEvent | RunOutput]
                if hasattr(output, 'content') and output.content:
                    yield {'content': output.content, 'done': False}
            yield {'content': '', 'done': True}

        except Exception as e:
            log_info(f'error: {e}')
            yield {
                'content': 'Sorry, an error occurred while processing your request.',
                'done': True,
            }
