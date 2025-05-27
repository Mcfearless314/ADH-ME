from autogen import AssistantAgent
from config import LLM_CONFIG
from tools.research_tool import ResearchTool
# from user_info_tool import user_info # This would be given to the agent as context, but it would
                                       # overwhelm the local LLM if included in this proof of concept.


class SummarizerTool:
    summarizer_agent = AssistantAgent(
        name="SummarizerAgent",
        llm_config=LLM_CONFIG,
        system_message=f"""
        You are a text summarization agent. Your task is to create concise summaries of provided texts 
        and extract main points that the reader can act upon.
        
        For each text you receive:
        1. Identify and extract the most important information with simple and direct language
        2. Create a clear, cohesive summary that captures the essence of the original text
        
        Respond only with the summary text and nothing else.
        """
    )

    def summarize_text(self, text: str) -> str:
        prompt = f"Text to summarize: {text}"

        messages = [{"role": "user", "content": prompt}]
        response = self.summarizer_agent.generate_reply(messages)

        if isinstance(response, dict):
            return response.get("content", "")
        else:
            return response


def main():
    summarizer_tool = SummarizerTool()
    research_tool = ResearchTool()
    research_paper = ""
    topic = "Procrastination"
    offset = 1
    paper_limit = 1
    max_attempts = 5
    attempts = 0

    while not research_paper and attempts < max_attempts:
        research_paper = research_tool.search_papers(topic, offset=offset, paper_limit=paper_limit)
        if not research_paper:
            print(f"No results found in attempt {attempts + 1}. Trying with next offset...")
            offset += paper_limit
            attempts += 1

    if research_paper:
        print(research_paper)
        summary = summarizer_tool.summarize_text(research_paper)
        print(f"Summary: {summary}")
    else:
        print("Could not find any relevant papers after multiple attempts.")


if __name__ == "__main__":
    main()