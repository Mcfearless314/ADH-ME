from autogen import AssistantAgent
from config import LLM_CONFIG
from calendar_agent import CalendarAgent

adh_me_agent = AssistantAgent(
    name="ADH-ME-Agent",
    llm_config=LLM_CONFIG,
    system_message="""
You are a neurodivergent-friendly productivity assistant.
Your core goal is to help the user stay focused, break big tasks into manageable steps, manage distractions,
and provide motivation and structure.

You respond in a concise, supportive tone.

If the user mentions tasks that involve specific dates, durations, or time management:

- Ask them if they would like help scheduling it.
- Only if they say yes, then send a scheduling prompt to CalendarAgent.
- Do not send anything to CalendarAgent without user confirmation.


After consulting another agent, summarize the answer clearly and return it to the user.

NEVER say "I can't help." Instead, always either:
- solve the task yourself, or
- call another agent for help and deliver the result to the user.

Examples:
- If the user says “I have an exam next week and I’m overwhelmed,” help them break it into smaller steps. Then ask CalendarAgent to help schedule study sessions.
- If the user says “I need a paper on dopamine and motivation,” ask ResearchAgent and return a clean summary.

Stay empathetic and pragmatic. You’re here to help the user succeed.
"""
)


class ADHMeAgent:
    def __init__(self, adh_me_agent, calendar_agent):
        self.adh_me_agent = adh_me_agent
        self.calendar_agent = calendar_agent
        self.awaiting_confirmation = False
        self.pending_schedule_prompt = None
        self.chat_history = []

    def handle_user_input(self, user_input: str) -> str:
        self.chat_history.append({"role": "user", "content": user_input})

        if self.awaiting_confirmation:
            if any(word in user_input.lower() for word in ("yes", "y", "sure", "ok", "please", "yeah")):
                self.calendar_agent.run(self.pending_schedule_prompt)

                self.awaiting_confirmation = False
                self.pending_schedule_prompt = None

                self.chat_history.append({"role": "assistant", "content": "Got it! I've scheduled your event."})

                return "Got it! I've scheduled your event."

            else:
                self.awaiting_confirmation = False
                self.pending_schedule_prompt = None
                return "Okay, I won't schedule anything now. Let me know if you want to later."

        adh_me_response = self.adh_me_agent.generate_reply(messages=self.chat_history)
        if isinstance(adh_me_response, dict):
            reply = adh_me_response.get("content", "")
        else:
            reply = adh_me_response

        self.chat_history.append({"role": "assistant", "content": reply})

        if "would you like help scheduling" in reply.lower():
            self.pending_schedule_prompt = user_input
            self.awaiting_confirmation = True

        return reply

    def run_chat(self):
        print("Hello, how can I help you today?")
        while True:
            user_input = input("You: ")
            response = self.handle_user_input(user_input)
            print("ADH-Me:", response)

if __name__ == "__main__":
    calendar_agent = CalendarAgent()
    adhme = ADHMeAgent(adh_me_agent, calendar_agent)
    adhme.run_chat()
