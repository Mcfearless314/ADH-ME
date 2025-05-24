import requests
from Demos.mmapfile_demo import offset

paperId = "649def34f8be52c8b66281af98ae884c09aef38b"

# Define the API endpoint URL
url = f"http://api.semanticscholar.org/graph/v1/paper/{paperId}"

# URL to fetch certain papers on a specific topic
# base_url = "https://api.semanticscholar.org/graph/v1/paper/search?query=procrastination&offset=100&limit=3"
base_url = "https://api.semanticscholar.org/graph/v1/paper/search?"

# Define the topic for the search
topic = "procrastination"

# Define options for the API request
offset = 0  # Offset for pagination
paper_limit = 3  # Limit the number of papers to fetch


def fetch_specific_papers(base_url, topic, offset=100, limit=3):
    url = f"{base_url}&query={topic}&offset={offset}&limit={limit}"

    # Send the API request for specific papers
    response = requests.get(url)

    # Check response status
    if response.status_code == 200:
        response_data = response.json()
        # Process and print the response data as needed
        print(response_data)
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")


def main():
    # Fetch specific papers on the topic of procrastination
    fetch_specific_papers(base_url, topic, offset, paper_limit)


if __name__ == "__main__":
    main()