---
title: "2PAC Project"
output: pdf_document
---

#2PAC Project
As part of the course, we were requested to write a final project using deep learning methods.
We decided to build a "song creator" in this project, we used lyrics of 2pac songs to create new song in the same style of the of 2PAC songs.

###Packages
We used the following packages while creating the "song creator":

1. sys
2. os
3. time
4. datetime
5. lxml.html
6. requests
7. numpy
8. nltk
9. theano
10. operator


###Data
Our data is the lyrics of more then 300 songs of 2Pac. We create the dataset by crawling the following website:
[2PAC Lyrics](http://www.allthelyrics.com/lyrics/2pac), we extracted a list of songs from the homepage, and we crawled about 300 other links in order to collect the lyrics of 2PAC songs.


The data was stored as nested list (list of lists), each item in the first list is a song, and each inner list is a row from the song. One of the main difficulties is that songs are not ordinary text, and there is high mining for the length of a line and the separation between song parts.
We chose specifically 2PAC because we wanted to create new song from singer that no longer with us. Also rap music is more randomly and not all rows have the same context so the result was very interesting.
We build an abstract system so if in any other time we will want to create new song for different artist we will just need to reconfigure the site for the crawler.

The code we used in order to extract the data, can be found in [Crawler.py](https://github.com/Innnon/SongCreator/blob/master/Crawler.py).


##Pre-processing
2PAC lyrics are different from other songs, especially because it's rap music and therefore there are more text, a lot of punctuation marks and word shortcuts, therefore the good pre-processing was vital in this project.
 
###Goals
1.	Simplify the vocabulary of the song.
2.	Remove unrelated tokens ( [, ] , ! , { , }, etc…)
3.	Convert sentence to indexes.

###Steps
1.	Go over all song and set special token:
	a. in the start and the end of the song.
	b. In the start and end of each section
	c. In the start and end of each row
2.	Remove unnecessary character using nltk tokenizer
3.	Create vocabulary of the most frequent words (5000 words)
4.	All word that are not in the vocabulary change to special token.

The code we used in the pre-processing stage, can be found in [Tokenizer.py](https://github.com/Innnon/SongCreator/blob/master/Tokenizer.py).

##RNN algorithm and building a model
###Train data
We created train data from the processed data, we stored the data in matrix that each row represent word and each column represent the possibility for the next word to be after the current one.

The code of this stage is within the Tokenizer file(used in the pre-processing stage).

###Model
Our model used theano library in order to compute the output and the hidden layer for the current step.
The model holds 3 vectors:
1.	U – represent input (X[i])
2.	W – this is the hidden layer
3.	V – the output vector
Those parameters used for calculating the next output.

At first those parameters stored random value and with each iteration on the training data we changed them in order to minimize our mistake from the outcome.

The code we used in this stage, can be found in [RNN.py](https://github.com/Innnon/SongCreator/blob/master/RNN.py).

###Train the model
We train the model within 20 iteration (more is better but take a lot of time). In each iteration we go over the matrix of the training data and activate the theano function using the model parameters (U,V and W) from the last iteration.

The code we used in this stage, can be found in [train.py](https://github.com/Innnon/SongCreator/blob/master/train.py).

###Create new song
We set the size of the new song to be 40 sentences. Each row need to be with at least 4 words.
The new song should start with start song token as set in the preprocessing and end with the appropriate token. Each time we create new song we request to start and end with the appropriate tokens.
In each iteration in order to get the next word we found the probability of the next word and get it using the numppy library. At the end we summarized the sentence.

The code we used for generating a song(using all the stages above), can be found in [create_2pac_song.py](https://github.com/Innnon/SongCreator/blob/master/create_2pac_song.py).

##The Output:
As we mention above the output of the project is a new song composed from 40 sentences, that each one of the sentences contains at least 4 words.

For example, here are some sentences from the output:

"Never , what I ever seem waiting

Ready to playa motherfuckin sent baby beings shinin ?

delano running me ."

You can see the full output [here](https://github.com/Innnon/SongCreator/blob/master/output%20example.txt).

##Calculating The Loss:
In order to calculate the loss, we used cosine similarity as we learned in class.
In the output presented above we got a value of 0.639487393264 similarity, which means that the value of the mistake is 0.3605.

The code we used for calculating the cosine similarity, can be found in [diff.py](https://github.com/Innnon/SongCreator/blob/master/diff.py).


As you can notice, the output song is very similar to 2PAC songs, we think that if we will enlarge the input, by providing the algorithm more lyrics we will get a better result, although we think this output is impressive.

