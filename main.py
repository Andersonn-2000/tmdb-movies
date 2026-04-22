import os
import logging
import time
from dotenv import load_dotenv

from cortex.src.client import TMDBClient
from cortex.src.service import TMDBService
from cortex.src.exporter import CSVExporter
from cortex.src.processor import MovieProcessor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":

    load_dotenv()
    API_KEY = os.environ.get("API_KEY")

    client = TMDBClient(api_key=API_KEY)
    service = TMDBService(client)
    exporter = CSVExporter("cortex/data/raw/movies_tmdb.csv")

    start_total = time.time()

    start_date = "2000-01-01"
    end_date = "2021-12-31"

    logging.info(f"Collecting data: {start_date} → {end_date}")

    try:
        movies = service.get_discover_range_safe(start_date, end_date)
    except Exception as e:
        logging.error(f"Error collecting data: {e}")
        exit()

    logging.info(f"{len(movies)} movies collected")

    seen_ids = set()
    filtered = []

    for m in movies:
        if m["id"] not in seen_ids:
            seen_ids.add(m["id"])
            filtered.append(m)

    chunk_size = 200
    total_movies = 0

    for i in range(0, len(filtered), chunk_size):
        chunk = filtered[i:i + chunk_size]

        processed = MovieProcessor.process_movies(chunk)
        exporter.save(processed)

        total_movies += len(chunk)

        logging.info(
            f"Chunk {i//chunk_size + 1} | {len(chunk)} movies"
        )
    
    logging.info("Dataset successfully created")
    logging.info(f"Total movies saved: {total_movies}")
    logging.info(f"Total time: {time.time() - start_total:.2f}s")