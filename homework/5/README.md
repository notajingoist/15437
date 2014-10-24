Jing Xiao 
10/23/14

-Didn't finish implementing the polling of new grumbls. Couldn't figure out how to convert timestamp strings in ISO 8601 format to something that I could compare to a timestamp so I couldn't filter out the posts that were created before that time stamp. Also, I realized that I use Django templates to generate each of my text posts and all the comment/dislike links and stuff attached to the text post. I didn't have time to figure out a way to translate all that into something I could just inject into the DOM via jquery/javascript without copying and pasting a huge long string. Didn't even have time to hack that together....ah well..
-When you go to settings and change your password, it logs you out so you have to log back in.
-Pagination and video grumblrs are not real
-Misnamed a generic post as a TextPost in my models early on... no time to refactor...
