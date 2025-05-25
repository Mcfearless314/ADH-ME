import time
from io import BytesIO

import PyPDF2
import requests


def search_papers(topic, offset=0, paper_limit=3, download_pdfs=True):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    search_params = {
        "query": topic,
        "offset": offset,
        "limit": paper_limit,
        "fields": "title,year,authors,abstract,citationCount,isOpenAccess,openAccessPdf"
    }

    response = requests.get(base_url, params=search_params)
    results = []

    if response.status_code == 200:
        response_data = response.json()
        papers = response_data.get("data", [])

        for paper in papers:
            paper_data = {
                "title": paper.get("title"),
                "year": paper.get("year"),
                "abstract": paper.get("abstract"),
                "citation_count": paper.get("citationCount"),
                "is_open_access": paper.get("isOpenAccess"),
                "authors": [author.get("name") for author in paper.get("authors", [])]
            }

            # Check if paper is open access and has PDF URL
            pdf_url = None
            if paper.get("isOpenAccess") and paper.get("openAccessPdf"):
                pdf_url = paper.get("openAccessPdf").get("url")
                paper_data["pdf_url"] = pdf_url

                # Download and extract text from PDF if requested
                if download_pdfs and pdf_url:
                    paper_data["pdf_text"] = download_and_extract_pdf_text(pdf_url, paper.get("title"))

            results.append(paper_data)

        return results
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return []


def download_and_extract_pdf_text(pdf_url, title):
    """Download PDF and extract its text content"""
    try:
        # Download PDF
        pdf_response = requests.get(pdf_url, stream=True)

        if pdf_response.status_code == 200:
            # Read PDF content
            pdf_file = BytesIO(pdf_response.content)

            # Extract text using PyPDF2
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""

            for page_num in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page_num].extract_text()

            print(f"Successfully extracted text from PDF: {title}")
            return pdf_text
        else:
            print(f"Failed to download PDF: {title}, status code: {pdf_response.status_code}")
            return None
    except Exception as e:
        print(f"Error processing PDF {title}: {str(e)}")
        return None


def get_specific_paper(paper_id: str, timeout_seconds=10):
    # Define the API endpoint URL for a specific paper
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"

    attempts = 0

    # Initialize start time for timeout tracking
    start_time = time.time()

    # Continue trying until timeout is reached
    while time.time() - start_time < timeout_seconds:
        # Send the API request for the specific paper
        response = requests.get(url)

        attempts += 1
        print(f"Attempt {attempts}: Fetching paper with ID {paper_id}")

        # Check response status
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            return response_data
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            print(f"Retrying in 1 second...")

            # Wait for 1 second before the next attempt
            time.sleep(1)

    print(f"Request timed out after {timeout_seconds} seconds")
    return None


def main():
    # Example usage
    topic = "Procrastination"
    results = search_papers(topic=topic, paper_limit=3)
    print(f"Results: {results}")

    # test_paper_id = "6f8d79c9fa1bde18bad2fb5c5cf12b9e530d8829"
    # get_specific_paper(paper_id=test_paper_id, timeout_seconds=5)


if __name__ == "__main__":
    main()