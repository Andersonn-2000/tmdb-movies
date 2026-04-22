from cortex.src.client import TMDBClient
from concurrent.futures import ThreadPoolExecutor, as_completed

class TMDBService:
    def __init__(self, client: TMDBClient):
        self.client = client
    
    def get_details(self, movie_id: int):
        return self.client._get(endpoint=f"/movie/{movie_id}")

    def get_popular(self, pages: int) -> list:
        movies = []

        for page in range(1, pages + 1): 
            data = self.client._get(endpoint="/movie/popular", params={"page": page})
            movies.extend(data["results"])
        
        return movies
    
    def get_popular_by_count(self, total_movies: int) -> list:
        
        movies = []
        page = 1

        while len(movies) < total_movies:
            data = self.client._get(
                endpoint="/movie/popular",
                params={"page": page})
            
            results = data["results"]

            if not results:
                break

            movies.extend(results)
            page += 1

        return movies[:total_movies]

    def get_full_dataset_by_count(self, total_movies: int) -> list:
        basic_movies = self.get_popular_by_count(total_movies=total_movies)

        full_movies = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self.get_details, movie["id"])
                for movie in basic_movies]
            
            for future in as_completed(futures):
                try:
                    full_movies.append(future.result())
                except Exception as error:
                    print(f'Error: {error}')

        return full_movies
    
    def get_full_dataset(self, pages: int) -> list:
        basic_movies = self.get_popular(pages=pages)

        full_movies = []
        for movie in basic_movies:
            details = self.get_details(movie["id"])
            full_movies.append(details)
        
        return full_movies