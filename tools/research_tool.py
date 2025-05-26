import time
import requests


def search_papers(topic, offset=0, paper_limit=1, timeout=5):
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

                return results
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(1)

    print(f"Request timed out after waiting for {timeout} seconds.")
    return None


def main():
    topic = "Procrastination"
    results = search_papers(topic=topic, offset=2, paper_limit=1)
    print(f"Results: {results}")


if __name__ == "__main__":
    main()