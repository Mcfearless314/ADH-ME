import json
from autogen import AssistantAgent
from config import LLM_CONFIG
from tools.calendar_tool import CalendarTool
from datetime import datetime

today_utc = datetime.utcnow().strftime("%Y-%m-%d")

SYSTEM_MESSAGE = f"""
Today is {today_utc} UTC.

You are an intelligent assistant that extracts detailed calendar event information from user inputs that may be vague, incomplete, or ambiguous.

Your goal is to produce a JSON object with the following fields:

{{
  "summary": string,
  "description": string,
  "start": "YYYY-MM-DD HH:MM",
  "end": "YYYY-MM-DD HH:MM"
}}

If the user wants to schedule multiple events (for example, over several days), respond with a JSON array where each element is a JSON object representing one event. For example:
[
  {{
    "summary": "Morning Workout",
    "description": "Daily exercise routine.",
    "start": "2025-05-24 06:00",
    "end": "2025-05-24 07:00"
  }},
  {{
    "summary": "Morning Workout",
    "description": "Daily exercise routine.",
    "start": "2025-05-25 06:00",
    "end": "2025-05-25 07:00"
  }}
]

You must only produce results in the JSON-format specified.

Instructions:

- Analyze the user's input carefully to determine the purpose of the event and create a concise, meaningful title (summary) that reflects the event.

- Compose a brief, clear description that elaborates on the event's purpose or context, inferred from the input or implied by the user's intent.

- Interpret any time references, such as relative dates ("tomorrow"), durations ("two hours"), or vague time periods, and convert them into exact start and end times in UTC.  
  - If the user does not specify exact times, choose reasonable default times to cover the duration mentioned or inferred.

- Ensure all datetime values use the format "YYYY-MM-DD HH:MM" in 24-hour UTC time.

- If the user mentions a deadline or an event time, schedule your event to finish before that time.

Example:  
If the user says, "I need to put two hours off for studying tomorrow," you should infer that the event is about studying, create an appropriate title and description, and assign a two-hour block on the next day with reasonable start and end times in UTC.
"""

class CalendarAgent:
    def __init__(self):
        self.agent = AssistantAgent(
            name="CalendarAgent",
            llm_config=LLM_CONFIG,
            system_message=SYSTEM_MESSAGE
        )
        self.tool = CalendarTool()

    def run(self, prompt: str):
        self.tool.get_credentials()
        response = self.agent.generate_reply(messages=[{"role": "user", "content": prompt}])

        if isinstance(response, dict) and "content" in response:
            result_str = response["content"]
        elif isinstance(response, str):
            result_str = response
        else:
            raise ValueError("Unexpected LLM response format")

        event_data = json.loads(result_str)

        if isinstance(event_data, list):
            events_to_create = []
            for event in event_data:
                start_dt = datetime.strptime(event["start"], "%Y-%m-%d %H:%M")
                end_dt = datetime.strptime(event["end"], "%Y-%m-%d %H:%M")
                events_to_create.append({
                    'summary': event['summary'],
                    'description': event['description'],
                    'start_dt': start_dt,
                    'end_dt': end_dt
                })
            links = self.tool.create_events(events_to_create)
            return links
        else:
            start_dt = datetime.strptime(event_data["start"], "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(event_data["end"], "%Y-%m-%d %H:%M")
            return self.tool.create_event(
                event_data["summary"],
                event_data["description"],
                start_dt,
                end_dt
            )
