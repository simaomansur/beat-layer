# Beat-Layer

## Overview
Beat Layer is a dynamic online platform designed for musicians and artists seeking collaborative synergy. By allowing users to contribute their unique 'layers' to existing beats, the app facilitates a musical dialogue where each addition enriches the original track. This virtual studio space not only fosters creativity but also archives the evolution of a beat as it transforms with each new contribution. It's a place where the solitary act of music creation becomes a communal journey, resulting in a tapestry of sounds that reflects the collective genius of its contributors.

## Design

### User Stories

#### US#1
As a songwriter, I want to upload my guitar track with a title and description, so other musicians can understand my vision and add their layers. (DONE)

#### US#2
As a collaborator, I want to leave feedback on tracks in progress, so I can help improve the collaboration and engage with other users. (DONE)

#### US#3
As a new user, I want to easily navigate through the app so that I can quickly understand its functionalities.(DONE)

#### US#4
As a song uploader, I want to receive constructive feedback on my unfinished tracks, so I can make informed decisions on how to develop them further. (DONE)

#### US#5
As a musician, I want to easily share my recordings with collaborators, so we can quickly exchange ideas and work on the tracks. (DONE)

#### US#6
As a musician, I want to search for songs by genre or artist, so I can find collaborations that match my interests and skills. (IP)

#### US#7
As a collaborator, I want to track the progress of songs I'm involved in, so I can see how they evolve over time. (NOT DONE)

#### US#8
As a returning user, I want to see highlighted collaborations or trending songs on the home page, so I can explore popular content. (NOT DONE)

#### US#9
As a collaborator, I want to be able to download the final version of a song, so I can use it in my own projects. (NOT DONE)

### Model

#### Use Case Diagram

![Use Case Diagram](src/static/pictures/UseCase.png)
```
# @startuml
# !define ICONURL https://raw.githubusercontent.com/rabelenda/cicon-plantuml-sprites/v1.0

# !define USERURL ICONURL/user1/white/person_white_48dp.png
# !define COMPUTERURL ICONURL/dev/computer_screen_dev_48dp.png
# !define DATABASEURL ICONURL/data/database_data_48dp.png
# !define CONTROLLERURL ICONURL/device/device_hub_device_hub_48dp.png
# !define ACTORURL ICONURL/avatar/avatar_48dp.png
# !define MAILURL ICONURL/communication/mail_outline_communication_48dp.png
# !define LIKEURL ICONURL/action/thumb_up_thumb_up_48dp.png

# !define AUTHUSER actor

# actor User as AUTHUSER #white

# rectangle "Web Application" {
#   [Home]
#   [Signup]
#   [Signout]
#   [Beats]
#   [New Beat]
#   [Beat Detail]
#   [Add Comment]
#   [User Profile]
#   [Forgot Password]
#   [Reset Password]
#   [Like Beat]

#   [Home] --> (AUTHUSER)

#   [Signup] --> (AUTHUSER)

#   [Signout] --> (AUTHUSER)

#   [Beats] --> (AUTHUSER)

#   [New Beat] --> (AUTHUSER)

#   [Beat Detail] --> (AUTHUSER)

#   [Add Comment] --> (AUTHUSER)

#   [User Profile] --> (AUTHUSER)

#   [Forgot Password] --> (AUTHUSER)

#   [Reset Password] --> (AUTHUSER)

#   [Like Beat] --> (AUTHUSER)
# }

# @enduml
```

#### Class Diagram

![Class Diagram](src/static/pictures/BLJ1JE1.PNG)
```
(code goes here)
```
# @startuml
# class User {
#   - id: String
#   - email: String
#   - passwd: String
# }

# class Beat {
#   - id: String
#   - title: String
#   - genre: String
#   - artist: String
#   - description: String
#   - audio_file: String
#   - date_added: DateTime
# }

# class Comment {
#   - id: String
#   - content: String
#   - date_posted: DateTime
# }

# class Like {
#   - id: String
#   - user_id: String
#   - beat_id: String
# }

# class SignUpForm {
#   + id: String
#   + email_address: String
#   + passwd: String
#   + passwd_confirm: String
# }

# class SignInForm {
#   + id: String
#   + passwd: String
# }

# class BeatForm {
#   + title: String
#   + genre: String
#   + description: String
#   + audio_file: File
# }

# class ForgotPasswordForm {
#   + email: String
# }

# class ResetPasswordForm {
#   + password: String
#   + password_confirm: String
# }

# class HomeForm {
#   + id: String
#   + passwd: String
# }

# User "1" -- "0..*" Beat : has
# User "1" -- "0..*" Comment : writes
# User "1" -- "0..*" Like : likes
# SignUpForm --|> User
# SignInForm --|> User
# BeatForm --|> Beat
# ForgotPasswordForm --|> User
# ResetPasswordForm --|> User
# HomeForm --|> User
# @enduml
```

#### Sequence Diagram

BLJ1JE1.png

![Sequence Diagram](src/static/pictures/Sequence.PNG)


```
# @startuml

# actor User

# database Database

# User -> FlaskApp: Open website
# activate FlaskApp
# FlaskApp --> FlaskApp: Check if user is authenticated
# note right: If authenticated, redirect to beats
# FlaskApp -> FlaskApp: Redirect to home
# FlaskApp --> FlaskApp: Render home page
# FlaskApp -> User: Display home page

# User -> FlaskApp: Login
# activate FlaskApp
# FlaskApp -> FlaskApp: Validate form
# FlaskApp -> Database: Query user
# Database --> FlaskApp: Return user data
# FlaskApp -> FlaskApp: Check password
# FlaskApp -> FlaskApp: Log in user
# FlaskApp -> FlaskApp: Redirect to beats
# FlaskApp --> User: Display beats

# User -> FlaskApp: View beat details
# activate FlaskApp
# FlaskApp -> Database: Query beat details
# Database --> FlaskApp: Return beat details
# FlaskApp -> FlaskApp: Render beat details
# FlaskApp --> User: Display beat details

# User -> FlaskApp: Add comment
# activate FlaskApp
# FlaskApp -> FlaskApp: Validate comment
# FlaskApp -> Database: Add comment to database
# Database --> FlaskApp: Confirm comment added
# FlaskApp --> User: Display success message

# deactivate FlaskApp

# @enduml
```

## Development Process 

This section should be used to describe how the scrum methodology was used in this project. As a suggestion, include the following table to summarize how the sprints occurred during the development of this project.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2|11/24/23|11/30/23|US#1, US#2|No troubles so far making progress but it seems that many stories might not get finished in the short time available|
|2|US#3, US#4, US#5|12/1/23|12/4/23|US#3, US#4, US#5|Steady progress is still being made. We had to throw out some features to get the project done on time but everything is working so far.|
|3|US#6, US#7, US#8, US#9|12/5/23|12/8/23|IP|IP|

Use the observations column to report problems encountered during a sprint and/or to reflect on how the team has continuously improved its work.

Feel free to use your own format for this section, as long as you are able to communicate what has been described here.

## Testing 

Share in this section the results of the tests performed to attest to the quality of the developed product, including the coverage of the tests in relation to the written code. There is no minimum code coverage expectation for your tests, other than expecting "some" coverage through at least one white-box and one black-box test.

## Deployment 

The final product must demonstrate the integrity of at least 5 of the 6 planned user stories. The final product must be packaged in the form of a docker image. In this section, describe the steps needed to generate that image so that others can deploy the product themselves. All files required for the deployment must be available, including the docker file, source/binary code, external package requirements, data files, images, etc. Instructions on how to create a container from the docker image with parameters such as port mapping, environment variables settings, etc., must be described (if needed). 


```
# Parker - 11/20/23 
## before running the app:
    export SECRET_KEY="pikachu" (mac) / $env:SECRET_KEY="pikachu" (windows)
    pip install -r requirements.txt
    hweaclfuatojowlh (google app pw) (in practice we wouldnt put this in the code but for now its fine)

## what I did today:
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
## what I did today:
- changed the 'Beat' model but may be subject to more changes
- added 'beats' 'beats_new' and 'beat_detail' to routes.py
- added 'BeatForm' to forms.py
- added beats.html, beats_new.html, and beat_detail.html to templates
- created function to create new beats
- modified signin and signup slightly
- after sign in takes you to the beats page where you can create a new beat, this adds it to the beats page but no functionality past that yet
- basic testing and so far it looks good just need to add more functionality to the beats page

# Parker - 11/28/23
## testing notes:
- would be nice if the post signin flash was a bit more descriptive
    - adding a header and footer could make me feel less lost
- back to home should take you back to beats page, not to sign in page
- add profiles ?
    
## done:
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

## notes:
- wanted to change the Beat model to add genres but didnt want to have to delete the database and start over
- this is something we should probably do in the future and work on together to figure out what we need to do

# Parker - 11/30/23
- lots of styling: menu bar, dark mode, UX stuff
- forgot password mostly implemented but still not updating the users password. it sends an email though 😄
added genres drop down menu
- cleaned up some file structure stuff (got rid of sign in page. now it's 'home'. if you're already signed in, 'home' returns 'beats'.)

# Simao - 12/1/23
- added likes to beats
    - user can only like a beat once
- changed some layouts and added some styling
- made pages scrollable
- footer is now at the bottom of the page
- header is now fixed at the top of the page
- signup page style fix
- create new beat page style fix
- beats page style fix
    - still could use some work

# Needed Changes
## Parker
- update the beat cards
- add a profile page
- add a profile picture 
- add a bio
- fix create new beat form page so input field widths are not the whole page
## Simao
- add sorting to beats page
- make functionable with docker
## Rye
- create a use case diagram
- create a class diagram
- create a sequence diagram
- create a vision statement (The project must have a vision statement that describes what the purpose of the software is, the type of problem it tries to solve, and the target audience.)
- At least one white-box and one black-box test, none of them related to user creation or authentication, must be provided.
## All
- The main branch must be protected and require a code review before a pull request approval.
- All source code must have a consistent header comment with a brief description and its author.
- Code written for this project must comply to PEP8 code style standards
- Test coverage report must be generated using Python's coverage.
```
