import os
import time
import logging
from dotenv import load_dotenv
from cortex.src.client import TMDBClient
from cortex.src.service import TMDBService
from cortex.src.exporter import CSVExporter
from cortex.src.processor import MovieProcessor

if __name__ == "__main__":

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    API_KEY = os.environ.get(key="API_KEY")

    client = TMDBClient(api_key=API_KEY)
    movie_service = TMDBService(client=client)
    exporter = CSVExporter(filename="cortex/data/raw/movies_tmdb.csv")

    start = time.time()

    data = movie_service.get_full_dataset_by_count(total_movies=100000)
    processed_data = MovieProcessor.process_movies(data=data)

    exporter.save(data=processed_data)

    end = time.time()

    logging.info("Dataset created successfully")
    logging.info(f'Execution time: {end - start:.2f} seconds')