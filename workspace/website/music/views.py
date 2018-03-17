# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Album, Song
##from django.template import loader
from django.shortcuts import render
# Create your views here.

def index(request):
	all_albums = Album.objects.all()
	"""html = ''
	for album in all_albums:
		url = '/music/'+ str(album.id)+'/'
		html += '<a href="'+url + '">'+album.album_title + '</a><br>'
	print html"""
	##template = loader.get_template('music/index.html')
	context = {
			'all_albums':all_albums,
			} # to pass information to a template in the form of dictionary
	##return HttpResponse(template.render(context, request))
	return render(request, 'music/index.html', context)

def detail(request, album_id):#USED IN URLS.PY
	#return HttpResponse("<h2>Details for Album id : " +str(album_id) + "</h2>")
	"""try:
		album = Album.objects.get(pk=album_id)
	except Album.DoesNotExist:
		raise Http404("Album does not exist") # include message for this built in function."""
	album = get_object_or_404(Album, pk=album_id)
	return render(request, 'music/detail.html', {"album":album})
def favourite(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	try:
		selected_song = album.song_set.get(pk=request.POST['song'])
	except (KeyError, Song.DoesNotExist):
		return render(request, 'music/detail.html', {"album":album, "error_message":"You did not select a valid song"})
	else:
		selected_song.is_favourite = True
		selected_song.save()
		return render(request, 'music/detail.html', {"album":album})
		
