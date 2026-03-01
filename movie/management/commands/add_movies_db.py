from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        #Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        #El path del archivo movie_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = 'movie/management/commands/movies.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        # Add products to the database
        added = 0
        for i in range(100):
            movie = movies[i]
            exist = Movie.objects.filter(title = movie.get('title')).first()  # ensure movie not already present
            if not exist:
                # some JSON entries have plot==null; description field is NOT NULL in model
                desc = movie.get('plot')
                if desc is None:
                    desc = ''  # fallback to empty string or provide a default message

                Movie.objects.create(title=movie.get('title','Unknown'),
                                     image='movie/images/default.png',
                                     genre=movie.get('genre',''),
                                     year=movie.get('year',''),
                                     description=desc)
                added += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {added} movies to the database'))
        
        #self.stdout.write(self.style.SUCCESS(f'Successfully added {cont} products to the database'))
                
                