import sys
import logging
import argparse
from task.fetch_data import get_papers_list  # Ensure this is the correct import path


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed based on query.")
    parser.add_argument('query', type=str, help="The query to search for papers.")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug logging.")
    parser.add_argument('-f', '--file', type=str, help="The filename to save the results.")

    args = parser.parse_args()  # Parse arguments

    # Configure logging based on debug flag
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG
    else:
        logging.basicConfig(level=logging.INFO)  # Default log level is INFO

    logging.debug("Debug logging is enabled.")

    try:
        # Now pass the parsed arguments to the get_papers_list function
        get_papers_list(args.query, args.debug, args.file)
    except Exception as e:
        logging.error(f"Error fetching papers: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
