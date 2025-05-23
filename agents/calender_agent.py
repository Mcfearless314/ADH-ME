load_dotenv()
api_key = os.getenv('API_KEY')


tavily_client = TavilyClient(api_key)