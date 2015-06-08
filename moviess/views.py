from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
import json
import hashlib
from models import *
from django.db.models import Q

def getJsonStr(movies):
	movies_json = list()
	for movie in movies:
		movie_dict = {}
		movie_dict['id'] = str(movie.id)
		movie_dict['name'] = str(movie.name)
		movie_dict['director'] = str(movie.director)
		movie_dict['genre'] = list(movie.genre)
		movie_dict['rating'] = float(movie.rating)
		movie_dict['popularity'] = float(movie.popularity)
		movies_json.append(movie_dict)
	json_str = json.dumps(movies_json)
	return json_str

def render_json(json_str):
	template = get_template("hello")
	t = template.render(Context({"movies": json_str}))
	return t

def renderHome(request):
	template = get_template("home")
	t = template.render()
	return HttpResponse(t)

def get_all(request):
	movies = Movies.objects.all()
	for movie in movies:
		genre = Genre.objects.filter(movie = movie).values_list('genere', flat=True)
		movie.genre = genre
	json_str = getJsonStr(movies)
	t = render_json(json_str)
	return HttpResponse(t)
	

def getMovieById(request, movieId):
	movies = Movies.objects.filter(pk = movieId)
	if movies:
		movies[0].genre = Genre.objects.filter(movie = movies[0]).values_list('genere', flat=True)
		movies_json = getJsonStr(movies)
		t = render_json(movies_json)
		return HttpResponse(t)
	t = render_json('[{"movie" : "not_found"}]')
	return HttpResponse(t)
	

def getMovie(request):
	movies = None
	if 'genre' in request.GET:
		if not movies:
			movies = Movies.objects.all()
		genre_list = request.GET['genre'].split(',')
		genre_movies = Genre.objects.filter(genere__in = genre_list).values('movie').distinct()
		movies_id = [str(genre_movie['movie']) for genre_movie in genre_movies]
		movies = movies.filter(pk__in = movies_id)	
	if 'rating' in request.GET:
		if not movies:
			movies = Movies.objects.all()
		movies = movies.filter(rating = float(request.GET['rating']))
	else:
		if not movies:
			movies = Movies.objects.all()
		if 'rating_lte' in request.GET:
			movies = movies.filter(rating__lte = float(request.GET['rating_lte']))
		if 'rating_gte' in request.GET:
			movies = movies.filter(rating__gte = float(request.GET['rating_gte']))
	if 'popular' in request.GET:
		if not movies:
			movies = Movies.objects.all()
		movies = movies.filter(popularity = float(request.GET['popular']))
	else:
		if not movies:
			movies = Movies.objects.all()
		if 'popular_lte' in request.GET:
			movies = movies.filter(popularity__lte = float(request.GET['popular_lte']))
		if 'rating_gte' in request.GET:
			movies = movies.filter(popularity__gte = float(request.GET['rating_gte']))
	if 'name' in request.GET:
		if not movies:
			movies = Movies.objects.all()
		movies = movies.filter(name__contains = request.GET['name'])
	if 'director' in request.GET:
		if not movies:
			movies = Movies.objects.all()
		movies = movies.filter(director__contains = request.GET['director'])	
	
	if movies:
		for movie in movies:
			movie.genre = Genre.objects.filter(movie = movie).values_list('genere', flat=True)
		movies_json = getJsonStr(movies)
		t = render_json(movies_json)
		return HttpResponse(t)
	t = render_json('[{"movie" : "not_found"}]')
	return HttpResponse(t)
	
def addMovie(request):
	if 'authId' in request.GET:
		admin = Admin.objects.filter(authId = request.GET['authId'])
		if admin:
			if 'name' in request.GET and 'director' in request.GET and 'rating' in request.GET and 'popularity' in request.GET and 'genre' in request.GET:
				movie = Movies(name = request.GET['name'], director = request.GET['director'], rating = float(request.GET['rating']), popularity = float(request.GET['popularity']))
				movie.save()
				genres = request.GET['genre'].split(',')
				for genre in genres:
					genre_new = Genre(movie = movie, genere = genre)
					genre_new.save()
				return redirect('/movies/' + str(movie.id) + '/')
			else:
				t = render_json('[{"movie" : "not_added"}, {"error": "some parameters skiped"}]')
				return HttpResponse(t)
		else:
			t = render_json('[{"movie" : "not_added"}, {"error": "not authorized"}]')
			return HttpResponse(t)
	else:
		t = render_json('[{"movie" : "not_added"}, {"error": "not authorized"}]')
		return HttpResponse(t)
		
def updateMovie(request, movieId):
	if 'authId' in request.GET:
		admin = Admin.objects.filter(authId = request.GET['authId'])
		if admin:
			movie = Movies.objects.get(pk = movieId)
			if movie:
				if 'genre' in request.GET:
					genre_list = request.Get['genre'].split(',')
					Genre.objects.filter(movie = movie).delete()
					for genre in genre_list:
						genre_new = Genre(movie = movie, genere = genre)
						genre_new.save()
				if 'rating' in request.GET:
					movie.rating = float(request.GET['rating'])
					movie.save()
				if 'popularity' in request.GET:
					movie.rating = float(request.GET['popularity'])
					movie.save()	
				if 'name' in request.GET:
					movie.name = request.GET['name']
					movie.save()
				if 'director' in request.GET:
					movie.director = request.GET['director']
					movie.save()
				return redirect('/movies/' + str(movie.id) + '/')
			else:
				t = render_json('[{"movie" : "not_updated"}, {"error": "movie_not_found"}]')
				return HttpResponse(t)
		else:
			t = render_json('[{"movie" : "not_added"}, {"error": "not authorized"}]')
			return HttpResponse(t)
	else:
		t = render_json('[{"movie" : "not_added"}, {"error": "not authorized"}]')
		return HttpResponse(t)
			

def deleteMovie(request, movieId):
	if 'authId' in request.GET:
		admin = Admin.objects.filter(authId = request.GET['authId'])
		if admin:
			movie = Movies.objects.get(pk = movieId)
			if movie:
				genre = Genre.objects.filter(movie = movie)
				genre_list = genre.values_list('genere', flat=True)
				movie.genre = genre_list
				json_str = getJsonStr([movie])
				movie.delete()
				genre.delete()
				return HttpResponse(render_json("Deleted Movie: " + json_str))
			else:
				t = render_json('[{"movie" : "not_deleted"}, {"error": "movie_not_found"}]')
				return HttpResponse(t)
		else:
			t = render_json('[{"movie" : "not_added"}, {"error": "not authorized"}]')
			return HttpResponse(t)
	else:
		t = render_json('[{"movie" : "not_added"}, {"error": "not authorized"}]')
		return HttpResponse(t)

		
def manageAdmin(request, name):
	try:
		admin = Admin.objects.get(name = name)
	except Admin.DoesNotExist:
		admin = None
	if not admin:
		auth_id = hashlib.sha256(name).hexdigest()
		admin = Admin(name = name, authId = auth_id)
		admin.save()
	admin_dict = {}
	admin_dict['name'] = str(admin.name)
	admin_dict['auth_id'] = str(admin.authId)
	json_str = json.dumps(admin_dict)
	return HttpResponse(render_json(json_str))

def createDummyDB(request):
	movies = Movies.objects.all()
	if not movies:
		movie_json_str = open('imdb.json').read()
		movie_json = json.loads(movie_json_str)
		for movie in movie_json:
			m = Movies(name = movie['name'], director = movie['director'], rating = float(movie['imdb_score']), popularity = float(movie['99popularity']))
			m.save()
			for g in movie['genre']:
				genre = Genre(movie = m, genere = g)
				genre.save()
				
	return redirect('/movies/all/')	
	
