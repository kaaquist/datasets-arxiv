import time
import arxiv
import click
from tqdm import tqdm
from urllib.error import HTTPError


def collect_papers(search_str: str, amount: int) -> None:
	"""
	Create the steps to be able to download the papers that will meet the criteria for the search term.

	Args:
		search_str (str) - search string to make a query for the papers. I. E. Machine Learing.
		amount (int) - amount of papers that will be downloaded.
	Returns:
		None
	"""
	client = arxiv.Client()
	search = arxiv.Search(
		query=search_str,
		max_results=amount,
		sort_by=arxiv.SortCriterion.SubmittedDate
	)

	for result in tqdm(client.results(search)):
		while True:
			try:
				print(f"Downloading: {result.title}")
				result.download_pdf(dirpath=f"./data/arxiv_pdfs_{search_str.replace(' ', '_')}")
				break
			except FileNotFoundError:
				print("File not found")
				break
			except HTTPError:
				print("Forbidden - to download PDF")
				break
			except ConnectionResetError as e:
				print("connection reset by peer")
				# TODO: wait before retry - might be better with circute breaker patterne or its like.
				time.sleep(5)


if __name__ == '__main__':
	search_value = click.prompt('Please enter a search criteria', type=str, default="Machine Learning")
	number_of_samples = click.prompt('Please enter how many papers that should be fetched', type=int, default=10)

	collect_papers(search_str=search_value, amount=number_of_samples)
