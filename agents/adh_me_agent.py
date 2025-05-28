import warnings
warnings.filterwarnings("ignore", message="flaml.automl is not available.*")
from datetime import datetime, timezone
from autogen import AssistantAgent, UserProxyAgent
from config import LLM_CONFIG
from tools.calendar_tool import schedule_event_handler, get_credentials
from tools.research_tool import search_papers
from tools.summarizer_tool import summarize_text
# from tools.user_info_tool import user_info # This would be given to the agent as context, but it would
                                             # overwhelm the local LLM if included in this proof of concept.

PROMPT_RESEARCH_TOPIC = """
When the user asks for help finding academic papers related to a specific topic, 
use the `search_papers` tool to find relevant academic papers. If the user provides a topic, call the `search_papers` function with appropriate parameters.
Respond with the results in a clear, structured way.
"""

PROMPT_SUMMARIZE_TEXT = """
When the user asks and provides a text, analyze and extract main points that the reader can act upon.
For each text you receive:

    1. Identify and extract the most important information with simple and direct language
    2. Create a clear, cohesive summary that captures the essence of the original text
    
Respond only with the summary text and nothing else."""

today_utc = datetime.utcnow().strftime("%Y-%m-%d")

PROMPT_CREATE_EVENT = f"""Today is {today_utc} UTC.

Your task is to schedule calendar events based on the user's input. Follow these rules:

- Always output start and end times as precise timestamps in the format: YYYY-MM-DD HH:MM (24-hour time, zero-padded).
- Do not use relative or vague time expressions like "tomorrow", "next week", or "6 hours from now".
- Instead, interpret these phrases, reason about them, and convert them into exact timestamps in UTC.
- Try to derive the exact date and time from the user's input.
- If no exact time is provided or can be derived, make reasonable assumptions:
  - Default start time: 09:00 UTC.
  - Default duration: 1 hour.
- Always provide a title and a description.

Output the final event as a JSON object, which should like this:

{{
  "title": "",
  "description": "",
  "start": "2025-05-28 14:00",
  "end": "2025-05-28 16:00"
}}

Do not output any extra text—only the JSON object in this exact format.

Always ask the user for confirmation before using the `schedule_event_handler` tool to create the event.
"""

def create_adh_me_agent():
    adh_me_agent = AssistantAgent(
        name="ADH-Me Agent",
        llm_config=LLM_CONFIG,
        system_message="""
        You are a neurodivergent-friendly productivity assistant.
        Your core goal is to help the user stay focused, break big tasks into manageable steps, manage distractions,
        and provide motivation and structure.
        
        You respond in a concise, supportive tone.
        
        After using a tool, summarize the answer clearly and return it to the user.
        
         You have access to use the following tools:
        - `search_papers`: Search academic papers related to a query.
        - `summarize_text`: Summarize a given text and extract main points.
        - `schedule_event_handler`: Schedule an event based on user input.
        
        Examples:
        - If the user says “I have an exam next week and I’m overwhelmed,” help them break it into smaller steps. Then use `schedule_event_handler` to create study events.
        - If the user says “I need a paper on dopamine and motivation,” use `search_papers` to find relevant academic papers, then summarize them with `summarize_text`.
        
        Stay empathetic and pragmatic. You’re here to help the user succeed.
        
        ALWAYS ask the user for confirmation before using the schedule_event_handler tool.
        
        Start by greeting the user, and asking them how you can help them before calling any tools.
        """
    )

    adh_me_agent.register_for_llm(name="search_papers", description=PROMPT_RESEARCH_TOPIC)(search_papers)
    adh_me_agent.register_for_llm(name="summarize_text", description=PROMPT_SUMMARIZE_TEXT)(summarize_text)
    adh_me_agent.register_for_llm(name="schedule_event_handler", description=PROMPT_CREATE_EVENT)(schedule_event_handler)

    return adh_me_agent


def create_user_proxy():
    user_proxy = UserProxyAgent(
        name="User Proxy",
        llm_config=False,
        human_input_mode="ALWAYS",
        code_execution_config = {"use_docker": False},
        function_map = {
            "search_papers": search_papers,
            "summarize_text": summarize_text,
            "schedule_event_handler": schedule_event_handler
        }
    )

    return user_proxy


def main():
    get_credentials()
    adhme_agent = create_adh_me_agent()
    user_proxy_agent = create_user_proxy()
    user_proxy_agent.initiate_chat(adhme_agent, message="Hello, can you help me?")

if __name__ == "__main__":
    main()