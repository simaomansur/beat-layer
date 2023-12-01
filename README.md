
====================================================================================================================================
# Parker - 11/20/23 
# before running the app:
    export SECRET_KEY="pikachu" (mac) / $env:SECRET_KEY="pikachu" (windows)
    pip install -r requirements.txt
    hweaclfuatojowlh (google app pw)

# what I did today:
- setup the template pretty much as before, except with a slightly different file structure (source code files are all in 'src' for organization)
    ** this makes python do some weird stuff -- we can play around with this if it ends up not being the move, but if importing, you might need to do absolute imports -> 'from src.app import models' (***instead of 'from from app import models').

Setup a basic template for the file structure - Beat (one to many ->) Layer (one to many ->) Stem
- index, base, signin, signup, beats (.html)
- models.py
- forms.py
- routes.py
Setup sign in / sign up / sign out routes
initialized Alembic (handy python package that helps with db migrations)
Some basic testing to make sure the routes were somewhat in working condition

# Simao - 11/24/23
# what I did today:
- changed the 'Beat' model but may be subject to more changes
- added 'beats' 'beats_new' and 'beat_detail' to routes.py
- added 'BeatForm' to forms.py
- added beats.html, beats_new.html, and beat_detail.html to templates
- created function to create new beats
- modified signin and signup slightly
- after sign in takes you to the beats page where you can create a new beat, this adds it to the beats page but no functionality past that yet
- basic testing and so far it looks good just need to add more functionality to the beats page

# Parker - 11/28/23
testing notes:
----
    - would be nice if the post signin flash was a bit more descriptive
        - adding a header and footer could make me feel less lost
    - back to home should take you back to beats page, not to sign in page
    - add profiles ?
    
done:
- added new description under overview (below in readme)
- referenced user id's in created by fields users table (foreign key)
- changed date to datetime for specifity
- back to home goes to 'beats' instead of index
- added audio_file stuff 
    takes audio file from form
    saves it to src/app/uploads
    you can play the song from beat-detail page

# Simao - 11/29/23
- few chabges to beats page for better readability
- added ability to comment on the beats detials page
- did some overall testing and everything seems to be working fine (so far)

notes:
    - wanted to change the Beat model to add genres but didnt want to have to delete the database and start over
    - this is something we should probably do in the future and work on together to figure out what we need to do
====================================================================================================================================

# beat-layer

# Overview
Beat Layer is a dynamic online platform designed for musicians and artists seeking collaborative synergy. By allowing users to contribute their unique 'layers' to existing beats, the app facilitates a musical dialogue where each addition enriches the original track. This virtual studio space not only fosters creativity but also archives the evolution of a beat as it transforms with each new contribution. It's a place where the solitary act of music creation becomes a communal journey, resulting in a tapestry of sounds that reflects the collective genius of its contributors.

# Design

## User Stories

Describe the user stories designed for the project, including clear acceptance criteria and point estimate for each of them. User stories must be consistent with the use case diagram. Refer to the user stories using US#1, US#2, etc. At least one of the user stories, not related to user creation or authentication, must be detailed by a sequence diagram. 

## Model 

At a minimum, this section should have a class diagram that succinctly describes the main classes designed for this project, as well as their associations.

# Development Process 

This section should be used to describe how the scrum methodology was used in this project. As a suggestion, include the following table to summarize how the sprints occurred during the development of this project.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2, ...|mm/dd/23|mm/dd/23|US#1|...|

Use the observations column to report problems encountered during a sprint and/or to reflect on how the team has continuously improved its work.

Feel free to use your own format for this section, as long as you are able to communicate what has been described here.

# Testing 

Share in this section the results of the tests performed to attest to the quality of the developed product, including the coverage of the tests in relation to the written code. There is no minimum code coverage expectation for your tests, other than expecting "some" coverage through at least one white-box and one black-box test.

# Deployment 

The final product must demonstrate the integrity of at least 5 of the 6 planned user stories. The final product must be packaged in the form of a docker image. In this section, describe the steps needed to generate that image so that others can deploy the product themselves. All files required for the deployment must be available, including the docker file, source/binary code, external package requirements, data files, images, etc. Instructions on how to create a container from the docker image with parameters such as port mapping, environment variables settings, etc., must be described (if needed). 
