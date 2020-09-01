# Sentiment Lexicon Builder for Turkish Language 

Using the movie reviews, I try to build a sentiment lexicon for Turkish Language. A sentiment lexicon assigns a sentiment score for each word. Here I use the movie reviews which include a comment as well as a rating. Given this data of comments and ratings, I train a statistical model that would attaches a rating to each word.

## beyazperde_urlbook.py
The website [beyazperde](http://www.beyazperde.com/) has user reviews in form of comments and numerical ratings. This file creates a urlbook containing list of urls for the movies.

## retrieve_comments.py
Using the urlbook, this file creates a corpus of comments and ratings.

## lexicon_builder.py
This main file has the statistical model that uses the corpus to create the lexicon.

## Sample Files
url_book.csv contains movie urls. corpus.csv contains the comments and ratings for each review posted on  [beyazperde](http://www.beyazperde.com/).
