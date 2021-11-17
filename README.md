## Scraping and Ranking RottenTomatoes
### UIUC: Fall’21 CS 410 - Text Information Systems

<b>Theme:</b> Intelligent Browsing<br/>
<b>Team Members:</b> Jeremy Wisuthseriwong (jrw7), Munesh Bandaru (muneshb2), Supriya Puri (puri6) <br/>
<b>Team Captain:</b> Munesh Bandaru (muneshb2) <br/>

This project is for the University of Illinois Urbana-Champaign CS-410 Text Informations Systems.

### Project Proposal
[Final Project Proposal](https://github.com/muneshb/CourseProject/blob/main/Project%20Proposal.pdf)

### Project Progress Report
[Final Project Progress Report](https://github.com/muneshb/CourseProject/blob/main/Progress%20Report.pdf)

### Abstract
Vertical search engines have become increasingly popular, now-a-days, as they sift through limited databases for information. A general web search cannot accommodate all of the users’ searches when it comes to specific topics without implicit assumptions. In particular, using a vertical search, a user can extensively use query based searches to get the desired results with high user ratings and reviews. One major example for searching a specific topic is “Rotten Tomatoes” - a review aggregation website for movies and television series. Its content is specialised for users browsing information on top rated movies and television entertainment -  genre, cast, network or the critic and user ratings. Results from services like Rotten Tomatoes allow a user to rank results by User Reviews, Critic Reviews, Genres, Audience Score. Being able to track user experience for various movies and tv series could lead to a larger audience and greater profits . 

### Introduction
Finding the right things on the internet is not easy - there isn’t a way to effectively search and rank a list of the top 100 movies for 2021 based on a given user query. Returning things that are of relevance to the user along with filtering the content based on the popularity is a challenge. Any general search engine would parse all the pages related to the query and search in a breadth-first manner to collect results. A query-specific search more efficiently searches a small subset of content by focusing on a particular requirement. <br/>
Through this project, we are trying to improve the user experience of browsing the content based on the user’s interests.  On the Rotten Tomatoes web page, users can find various pre-defines ratings and rankings for movies and TV series like Best Movies of 2021, Popular Shows on Netflix but there isn’t a way to effectively search and rank for a list of movies within that particular ranking matching the user query/interest.. Here we are making our system to provide an intelligent way of browsing the content within the top 100 movies filtered and sorted based on the user query.<br/>
<b>Example:</b><br/>
Lets say a user is browsing the “ [Top 100 movies of 2021, Rotten Tomatoes](https://www.rottentomatoes.com/top/bestofrt/?year=2021) ” on Rotten Tomatoes. <br/>
But he is more interested in looking for thriller movies available on Hulu from this ranking list of 100 movies. When looking further, he could not find a way to filter and sort this list and needed to go through each movie description to find out whether a movie meets his interests or not. <br/>
<br/>
<b>Sample query:</b> “thriller movies on Hulu”<br/>
<br/>
By using the web application, he can find the thriller movies available on Hulu (matching to the query) with movie information and tomatometer rating. Thus making it easier for him to explore his options and decide on the movie according to his liking.  

### Overview of the Tasks
1. Data Scraping and Refining:
   * Scraping the Main top 100 movies page
   * Scraping the description/content of each movie page: 
     - Title
     - synopsis
     - genres
     - where to watch 
     - tomatometer rating
     - reviews
2. Modelling & Evaluation
   * Create a ranker function to score each document per the sample query using BM25 parameters and other ranker algorithms 
   * Calculate ranking results for each sample query for the top10 movies
   * Perform initial evaluation by calculating average precision for each sample query and mean average precision for all the sample queries
   * Perform relevance testing and evaluation using other algorithms such as NDCG@10
   

4. Web Application for interaction
   * Create a web-application for the user to input a query related to the movie and get a list of top10 rank based movies matching the search criteria
   
5. End to end testing
   * Create a query judgements document by manually checking each movie for matching the input query and verify that the results from the search function are in sync with the user provided initial relevance. 
   

### References

* [Top 100 movies of 2021, Rotten Tomatoes](https://www.rottentomatoes.com/top/bestofrt/?year=2021)
* [Metapy Search and IR evaluation Tutorial](https://github.com/meta-toolkit/metapy/blob/master/tutorials/2-search-and-ir-eval.ipynb) 
* [Implementation of the ranker functions](https://github.com/meta-toolkit/meta/tree/master/include/meta/index/ranker)  
* [How to scrape websites with Python and BeautifulSoup](https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe)
* [The Flask Mega Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)  
* [Deploy Flask app on Heroku using GitHub](https://dev.to/lordofdexterity/deploying-flask-app-on-heroku-using-github-50nh)





