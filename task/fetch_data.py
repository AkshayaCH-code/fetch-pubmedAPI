import requests
import pandas as pd
import argparse
import csv
import sys
import logging
from typing import List, Dict
import re

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
DB = "pubmed"


# Function to search PubMed for papers based on a query
def search_papers(query: str) -> List[str]:
    url = f"{PUBMED_API_URL}esearch.fcgi"
    params = {
        "db": DB,
        "term": query,
        "retmode": "json",  # Request JSON instead of XML
        "api_key": "08644cb8d7fe3482e79cea4c76b2fe841809",  # Add your API key here if needed
        "email": "akshaya.pdev@gmail.com"  # Optional: your email for identification
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error if status code is not 200

        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Content: {response.text}")

        if response.status_code == 200:
            # Parse the JSON response to get the list of PubMed IDs
            pmids = parse_pmids(response.json())  # Parse JSON response
            if not pmids:
                logging.info("No results found for the query.")
            return pmids
        else:
            logging.error(f"Unexpected status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API request: {e}")
        return []


# Function to parse PMIDs from the JSON response
def parse_pmids(json_response: Dict) -> List[str]:
    try:
        # Extract PMIDs from the JSON response
        pmids = json_response.get('esearchresult', {}).get('idlist', [])
        return pmids
    except KeyError as e:
        logging.error(f"Error parsing JSON: {e}")
        return []


# Function to fetch paper details using PubMed ID

def fetch_paper_details(pmid: str) -> Dict[str, str]:
    url = f"{PUBMED_API_URL}efetch.fcgi"
    params = {
        "db": DB,
        "id": pmid,
        "retmode": "text",  # Request plain text instead of JSON
        "rettype": "abstract",
        "api_key": "08644cb8d7fe3482e79cea4c76b2fe841809",
        "email": "akshaya.pdev@gmail.com"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error if status code is not 200

        # Debugging the raw response
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Content: {response.text}")  # Print the raw content

        if response.status_code == 200:
            # Check if the response body is empty
            if not response.text.strip():  # If response body is empty
                logging.error(f"Empty response for PubMed ID: {pmid}")
                return {}

            # Now extract paper details from the raw plain text response
            details = parse_paper_details_from_text(response.text)

            return details
        else:
            logging.error(f"Unexpected status code: {response.status_code}")
            return {}

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API request: {e}")
        return {}


def parse_paper_details_from_text(text: str) -> Dict[str, str]:
    """Extract details like title, authors, date, etc., from the raw text response."""
    details = {}

    # Example parsing patterns using regular expressions (you may need to adjust)
    try:
        # Title: Extract the first line, assuming it's the title
        title_match = re.search(r"^(.*?)(?=\n)", text)
        details["Title"] = title_match.group(1).strip() if title_match else "No title available"

        # Authors: Extract authors after the title
        authors_match = re.search(r"^(.*?)(?=\n)(?=.*Author information:)", text, re.DOTALL)
        details["Non-academic Author(s)"] = authors_match.group(1).strip() if authors_match else "No authors available"

        # Publication Date: Extract the date
        date_match = re.search(r"(\d{4} \w+ \d{1,2});", text)
        details["Publication Date"] = date_match.group(1).strip() if date_match else "No date available"

        # DOI: Extract DOI if available
        doi_match = re.search(r"doi:\s*(\S+)", text)
        details["DOI"] = doi_match.group(1).strip() if doi_match else "No DOI available"

        # PMID: Extract the PubMed ID
        pmid_match = re.search(r"PMID:\s*(\d+)", text)
        details["PubmedID"] = pmid_match.group(1).strip() if pmid_match else "No PMID available"

        # Corresponding Author Email: You can try to extract email if available
        email_match = re.search(r"Electronic address:\s*(\S+)", text)
        details["Corresponding Author Email"] = email_match.group(1).strip() if email_match else "No email available"

    except Exception as e:
        logging.error(f"Error parsing paper details from text: {e}")
        details = {"Error": "Unable to parse text properly"}

    return details


# Function to output data to CSV
def output_to_csv(data: List[Dict[str, str]], filename: str):
    keys = data[0].keys() if data else []
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Main function to handle the entire process
def get_papers_list(query: str, debug: bool, output_file: str):
    try:
        if debug:
            print("in debug")
            logging.debug(f"Searching for papers with query: {query}")

        pmids = search_papers(query)
        papers = []

        for pmid in pmids:
            if debug:
                logging.debug(f"Fetching details for PubMed ID: {pmid}")
            paper = fetch_paper_details(pmid)
            papers.append(paper)

        if output_file:
            output_to_csv(papers, output_file)
        else:
            for paper in papers:
                print(paper)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API call: {e}")
        sys.exit(1)


# Command-line argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed.")
    parser.add_argument("query", help="The query to search in PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("-f", "--file", help="The filename to save the results.")
    return parser.parse_args()


def main():
    args = parse_args()
    get_papers_list(args.query, args.debug, args.file)


if __name__ == "__main__":
    main()
