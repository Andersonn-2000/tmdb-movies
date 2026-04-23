from cortex.src.client import TMDBClient
from datetime import datetime, timedelta

class TMDBService:
    def __init__(self, client: TMDBClient):
        self.client = client
    
    def get_details(self, movie_id: int):
        return self.client._get(endpoint=f"/movie/{movie_id}")
    
    def discover_movies(self, start_date: str, end_date: str, page: int = 1):
        return self.client._get(
            endpoint="/discover/movie",
            params={
                "primary_release_date.gte": start_date,
                "primary_release_date.lte": end_date,
                "page": page,
                "sort_by": "primary_release_date.asc"
            }
        )
    
    def get_discover_range_safe(self, start_date: str, end_date: str, max_pages: int | None) -> list:

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if start >= end:
            return []

        data = self.discover_movies(start_date, end_date, page=1)
        total_pages = data.get("total_pages", 1)
        
        if max_pages is not None:
            total_pages = min(total_pages, max_pages)
            
        if total_pages >= 500:
            delta = (end - start).days // 2
            mid = start + timedelta(days=delta)

            movies = []
            movies.extend(
                self.get_discover_range_safe(start_date, mid.strftime("%Y-%m-%d"))
            )
            movies.extend(
                self.get_discover_range_safe(
                    (mid + timedelta(days=1)).strftime("%Y-%m-%d"),
                    end_date
                )
            )
            return movies

        movies = data.get("results", [])

        for page in range(2, total_pages + 1):
            data = self.discover_movies(start_date, end_date, page)
            movies.extend(data.get("results", []))

        return movies