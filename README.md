# Facebook group downloader

#### Usage
Simply use `docker-compose up` and navigate to localhost:8000 using browser of your choice.

#### Introduction
Nowadays Facebook is the main medium for exchanging opinions and thoughts. Hundreds of thousands of people uses Facebook groups daily treating them as once popular Internet forums. They conduct discussions there, often creating posts several thousand characters long. Unfortunately, everything posted on Facebook is at the mercy of Zuckerberg. Your thriving group can disappear in every moment for no reason - with years of discussions and exchanges of ideas.

This is why I made this simply tool to archive the Facebook groups.  As the web developer I used tools I'm familar with. 

#### How does it works?
There is a catch - only group admin or moderator can download the group - everyone else don't have right access to facebook graph API.
 
Just download the code from repo, write docker-compose up, navigate to localhost, choose your group, wait for the moment aaaand... its all. There is simply searching by author and post phrase included.

#### Future
##### Long-live tokens
I am going to create a remote service with flask that will generate facebook long-lived tokens. I can't provide my app secret client key for obvious reasons. 

##### Additional features
Right now this tool makes the job done, although it is very, very, very primitive - keep in mind that it was made fast under time pressure . I'm planning to make proper searching, improve the looks of webpage, add some kind of statistics - all utilities that would be great to have even if you wouldn't be scared of losing your group.

It would be nice to have some kind of interface for downloading\uploading the database to webapp. By this way the group admin would be able to share the archive with other users. 

##### Stand alone client
I'm also intend to make stan-alone "exe" client in rust.