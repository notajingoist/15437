Homework 4 - Jing Xiao
10/3/14

-You can dislike and comment on your own posts
-Comments appear directly beneath the post (eventually I want to hide/show them upon clicking on 'comments')
-The only evidence that something was disliked is the counter on the post going up. Otherwise, I haven't found a way to show dislikes yet. Perhaps also I will hide/show them upon clicking 'dislikes'
-I didn't find a way to show a default profile picture yet. However you can upload a picture on the edit profile page and that will show fine
-The first few users I registered on the site don't properly display their follower/following count. So for testing, maybe only try following and blocking the new users you create (or users with later ids). I didn't flush the database because it took me a long time to accumulate all these users and posts
-Searching for terms in the stream will only search for the keyword in your follower posts (and excluding those who have blocked you); searching in home will only search in your posts; searching in profile will only search in that person's posts
-You can't reset the password yet. Only confirmation email upon registering
-You can't follow or block yourself
-ALSOOOOO just fixed something. Don't know if you'll read this because it's past midnight. But. Profile pictures for other users now display after the 12:04am commit.... I had copied the code from the videos and wasn't retrieving the given user's profile picture. Instead, I was specifying the user as the current user. But 1 line change and now you can see others' pictures! 