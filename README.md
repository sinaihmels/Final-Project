# MY HABITS
#### Video Demo:
#### Description:
My Habits is a Web application for tracking your habits and setting goals on your computer. The concept was inspired by habit trackers used in journals. The user can for example decide to track the habit meditation and set their goal to meditate for 10 minutes everyday. On My Habits the user can log their progress and hopefully reach their goal. 

The project consists of seven html pages (index, layout, login, logout, register, settingsmh, settingsuser), app.py, habits.py, security.py, settings.py and the database database.db
The project was created using flask. python, html, jinja and styled using css. 

The index page displays the habits selected by the user. The user will see several boxes depending on how many habits they choose to track. Each box consists of the goal the user wants to reach, a pixelart image, a statement about the progress already achieved, an input field and submit button to track more progress as well as a reset button to reset their progress back to 0. The image in each box changes depending on the progress the user has made. When the user reaches their goal the image shows a gif that displays the progress. If the user is not logged in index displays a default setting of habits with a set goal. The user cannot interact with the index page without being logged in. The user can navigate using the navbar to register or log in. On the register page they can input a username,  password and confirm that password. The password is hashed and stored with the username within the database. If the user already has an account they can log in with their username and password on the login page. Once a user is registered the habits are set to default. The user can change the habits tracked and the goals using the settings pages. The settings for the habits and goals are set on the page settingsmh. The user can select from 1 up to 6 habits between 9 possible habits. They can also set new goals for these habits. The user can change their user settings with settingsuser and change their username or password. 

# Let's look under the hood: 
## index
The index page is created based on the data from the database. If there is no user logged in, index is generated using the default set of data from the database using the getdefaultdata function. If there is a user logged in the index page is created with the users data that was retreived and formated using getuserdata. This formatting of the index page makes the webapplication more versatile. The index page can differ between different users based on the amount of habits they track, the different habits they track and the different goals they have set. 

## layout
The layout page is designed to ensure a coherence in the layout and the formatting between the different pages. Within the layout the navbar is designed which is different depending on if a user is logged in or not. If a user is not logged in it displays the options Home, Log In, Register. If a user is logged in it displays the options Home, Settings, Log Out. This ensures that only users who are logged in are able to change their settings due to the need of being able to save their settings within the database. 

## login
The login page consists of two input fields to input the username and the password as well as a button to submit the form. The input is validated, the username is compared to the username in the database and the password is hashed and compared to the hashed password in the database. The user_id is stored within the sqlite session in the database. 

## logout
When a user clicks on the logout button on the navbar the stored user id within the session is deleted and the user is logged out. 

## register
The register page is similar to the login page. It consists of three input fields to input a username, a password and confirm the password as well as a button to submit the form. The input is checked and the data is stored within the database. Once a user is registered the function setuser_habits sets the habits connected to the user within the database to the default settings. 

## settingsmh
The settingsmh page makes the web application more interactive. The user can choose 1-6 habits they want to track using checkboxes. Once they submit the form with the checkboxes the changehabits function changes the habits connected to the logged in user id within the database. Underneath the checkboxes the user can see the habits they chose and change the goal for each habit. If they choose the change a goal the update_goal function is called to update the goal within the database. 

## settingsuser
The settingsuser page gives the user an opportunity to change their username and their password. 

# Improvements for the Web application that will get implemented in the future
- [ ] Improve the pixelart for "outside time" and "clean"
- [ ] Automatically create the checkboxes on the settingsmh.html page 
- [ ] Implement a design settings page where the user can select the fonts and choose a dark mode 

