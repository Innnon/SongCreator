---
title: "HW3 - Grey Anatomy Grapgh"
output: pdf_document
---

#Deep learning 
In this project we used lyrics of 2pac songs to create new song in the same style of the rapper 2pac.

##Configuration
###Packages
sys, os , time, datetime, lxml.html, requests, numpy, nltk, theano, operator

###EC2 Configuration
![types](ec2.png)
#### Set Initalization Commands
- sudo apt-get update
- git clone https://github.com/Innnon/SongCreator.git
- cd SongCreator
- mkdir data
- sudo pip install nltk
- python nltk_down.py
- sudo apt-get install python-lxml
- cd ..
- echo -e "\n[global]\nfloatX = float32\ndevice = gpu0\n\n[nvcc]\nfastmath=True\n" >> ~/.theanorc
- sudo apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
- sudo pip install --upgrade theano
- cd  SongCreator
- python create_2pac_song.py

##Data
Our data compuse of more then 300 songs of the artist 2Pac. We create the data base by crawling from the website http://www.allthelyrics.com/lyrics/2pac
The data is list of list, each item in the first list is a song, and each inner list is a raw from the song. One of the main difficulties is that songs are not ordinary text, and there is high mining for the length of a line and the separation between song parts.
We chose the rapper 2pac cause we want to create new song from singer that no longer with us. Also rap music is more randomly and not all rows have the same context so the result could be very interesting.
We build the system in a way that, if later we will want to create new song for different artist we just need to reconfigure the site for the crawler.

##Pre-processing
###Goals
1.	Simplify the vocabulary of the song.
2.	Remove unrelated tokens ( [, ] , ! , { , }, etc…)
3.	Convert sentence to indexes.

###Steps
1.	Go over all song and set special token:
	a.	 in the start and the end of the song.
	b.	In the start and end of each section
	c.	In the start and end of each row
2.	Remove unnecessary character using nltk tokenizer
3.	Create vocabulary of the most frequent words (5000 words)
4.	All word that are not in the vocabulary change to special token.

##RNN algorithm and building a model  (section 4, 5, 6)
###Train data
Create train data compose from the processed data. Create matrix of word that each row represent word and each column represent the possibility for the next word to be after the current one.

###Model
Our model used theano library in order to compute the output and the hidden layer for the current step.
The model hold 3 vector:
1.	U – represent input (X[i])
2.	W – this is the hidden layer
3.	V – the output vector
Those parameters used for calculating the next output. At first those parameter hold random value and with each iteration on the training data we change them in order to minimize our mistake from the result outcome to the requested.

###Train the model
We train the model in 20 iteration (more is better but take a lot of time). In each iteration we go over all the metrix of the training data and activate the theano function using the model parameters (U,V and W) from the last iteration.

###Create new song
We set the size of the new song to be 40 sentences. Each row need to be with at least 4 words.
The new song should start with start song token as set in the preprocessing and end with the appropriate token. Each time we create new song we request to start and end with the appropriate tokens. Between we just domain to start and end with appropriate start and end sentence. 
In each iteration to get the next word we found the probability of the next word and get it using the numppy library. At the end we summarized the sentence.


