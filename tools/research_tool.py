import json
import time
import requests
from typing import Annotated

def search_papers(
    topic: Annotated[str, "The topic to search academic papers for"],
    offset: Annotated[int, "The starting position in results"] = 0,
    paper_limit: Annotated[int, "Maximum number of papers to return"] = 1,
    timeout: Annotated[int, "Maximum time to wait for results (seconds)"] = 5
) -> str:
    """
    Search academic papers related to a query.
    """
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    search_params = {
        "query": topic,
        "offset": offset,
        "limit": paper_limit,
        "fields": "title,year,authors,abstract,citationCount,isOpenAccess,openAccessPdf"
    }

    start_time = time.time()

    while (time.time() - start_time) < timeout:
        try:
            print("i am searching for papers...")
            response = requests.get(base_url, params=search_params)

            if response.status_code == 200:
                response_data = response.json()
                papers = response_data.get("data", [])

                results = []
                for paper in papers:
                    paper_data = {
                        "title": paper.get("title"),
                        "url": paper.get("openAccessPdf", {}).get("url") if paper.get("openAccessPdf") else None,
                        "year": paper.get("year"),
                        "citation_count": paper.get("citationCount"),
                        "authors": [author.get("name") for author in paper.get("authors", [])],
                        "abstract": paper.get("abstract"),
                        "is_open_access": paper.get("isOpenAccess")
                    }
                    results.append(paper_data)

                return json.dumps(results, indent=2) if results else "No results found."
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(1)

    print(f"Request timed out after waiting for {timeout} seconds.")
    return "Request timed out. No results retrieved."