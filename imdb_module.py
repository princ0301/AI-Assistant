import imdb

class IMDbAssistant:
    def __init__(self):
        self.movies_db = imdb.IMDb()

    def search_movie(self, query): 
        try: 
            clean_query = query.replace('search', '').strip()
            movies = self.movies_db.search_movie(clean_query)
             
            if not movies:
                return None
             
            first_movie = movies[0]
             
            self.movies_db.update(first_movie)
             
            title = first_movie['title']
            year = first_movie.get('year', 'Unknown')
             
            movie_info = self.movies_db.get_movie(first_movie.movieID)
             
            rating = movie_info.get('rating', 'Not available')
            
            return {
                'title': title,
                'year': year,
                'rating': rating,
                'movie_id': first_movie.movieID
            }
        
        except Exception as e:
            print(f"Error searching movie: {e}")
            return None

    def get_cast_info(self, movie_id):
        try: 
            movie = self.movies_db.get_movie(movie_id)
             
            cast = movie.get('cast', [])
            top_cast = [str(actor) for actor in cast[:5]]
             
            directors = movie.get('directors', [])
            director = str(directors[0]) if directors else 'Not available'
            
            return {
                'top_cast': top_cast,
                'director': director
            }
        
        except Exception as e:
            print(f"Error getting cast info: {e}")
            return None

    def get_movie_summary(self, movie_id):
        try: 
            movie = self.movies_db.get_movie(movie_id)
            plot = movie.get('plot outline', ['No summary available'])[0]
            
            return {
                'plot': plot
            }
        
        except Exception as e:
            print(f"Error getting movie summary: {e}")
            return None