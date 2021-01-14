# Spotipy project 
The goal of this project is to provide a terminal based version of spotify, including new features that are not available in the normal spotify app. 

This project uses the spotify Web API (https://developer.spotify.com/documentation/web-api/) which is based on simple REST principles, the Spotify Web API endpoints return JSON metadata about music artists, albums, and tracks, directly from the Spotify Data Catalogue.

Spotipy will also be used, which is the lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform.

Before you can use this spotify project, you will have to do the following:
* You need a Spotify user account (Free or Premium)
* Go to: https://developer.spotify.com/dashboard/ and log in with your spotify account. There you will have to "Create an app" in order to get 
"SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" keys, which you must set as environment variables (for example in .bashrc).
 

The main focus with this project is to create easy and quick terminal code to achieve maximum Spotify experience from terminal (which is what we all want). 

The goal is to provide one single python file which provides a terminal interface where different spotify functions are provided. This can be to search for artists, add current songs to queue, modify playback and so on. This will be found in everything.py. As with all the scripts, commenting, grammar skills, puns and coding skills, they will continuously be improved. 
 
The following modules will also have to be installed: 
* spotipy
* tqdm
* colorama
* os, unicodedata, argparse, sys, operator
* random, time, json


The individual scripts are best served with a nice alias :)
https://linuxize.com/post/how-to-create-bash-aliases/
