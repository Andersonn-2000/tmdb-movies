class MovieProcessor:

    @staticmethod
    def process_movies(data: list[dict]) -> list[dict]:

        processed = []
        for m in data:
            processed.append({
                "title": m.get("title"),
                "genres": ", ".join([g["name"] for g in m.get("genres", [])]),
                "original_language": m.get("original_language"),
                "release_date": m.get("release_date"),
                "revenue": m.get("revenue"),
                "runtime": m.get("runtime"),
                "status": m.get("status")
            })
        
        return processed