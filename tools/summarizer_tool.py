import autogen
from config import LLM_CONFIG
from research_tool import search_papers
from user_info_tool import user_info


class SummarizerTool:
    def __init__(self):
        self.summarizer_agent = autogen.AssistantAgent(
            name="SummarizerAgent",
            llm_config=LLM_CONFIG,
            system_message=f"""
            You are a specialized text summarization agent. Your task is to help a certain user by
            creating concise summaries of provided texts and extract main points that the user can act upon.
            
            The user: {user_info}
            
            For each text you receive:
            1. Identify and extract the most important information
            2. Create a clear, cohesive summary that captures the essence of the original text
            3. Keep your summary brief while maintaining crucial details
            4. Use simple, direct language
            
            Respond only with the summary text and nothing else.
            """
        )

    def summarize_text(self, text: str, max_words: int = None) -> str:
        """
        Summarize the provided text

        Args:
            text: The text to summarize
            max_words: Optional maximum word count for the summary

        Returns:
            A concise summary of the text
        """
        prompt = f"Please summarize the following text in a clear and concise manner:"

        if max_words:
            prompt += f" Use approximately {max_words} words or less."

        prompt += f"\n\nText to summarize: {text}"

        messages = [{"role": "user", "content": prompt}]
        response = self.summarizer_agent.generate_reply(messages)

        if isinstance(response, dict):
            return response.get("content", "")
        else:
            return response


def main():
    # Example usage
    summarizer = SummarizerTool()

    # These are the texts the agent should summarize but research papers are most likely too long for
    # a local LLM to handle, so we will use a simple sample text instead.
    # research_paper = search_papers("Improve productivity with ADHD")
    # summary = summarizer.summarize_text(research_paper)

    simple_sample_text = """
    People with ADHD can boost their focus and productivity by breaking tasks into smaller steps, 
    using timers to stay on track, and minimizing distractions in their environment. Regular breaks, a 
    consistent routine, and organizing tasks with lists or 
    digital tools can also help maintain attention and improve efficiency.
    """
    summary = summarizer.summarize_text(simple_sample_text)
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()