# Reed Time: An Online Assistant for Oboists

Video link: https://youtu.be/4LyZX_-a_Jg

The bane of most oboists' commitment to their musical craft is making the double reeds we have to play on. It is incredibly difficult to make a reed, start to finish, without mistakes that dramatically change its sound, and since reeds are made of wood (or more specifically, the cane plant), each reed behaves differently. There are many steps in the process of making a reed, and it is easy to get too hung up on one step to the detriment of another. This is why I decided to design a helpful tool that would keep me on track while making my oboe reeds: Reed Time. 

Before delving into the features of Reed Time, the website does require registration and login so that multiple users can keep track of their reedmaking data. Running "flask run" in the terminal opens up the login page of the website, where one can input their username and password to access the rest of the website. If one wants to make a new account, there is a link to the registration page in the navigation bar at the top of the page. On this page, the user is asked to create a username that does not already exist and a password before confirming the password. The user will be directed to an apology page if they do not input into all of the fields, if the username already exists, or if the passwords do not match.

Once logging in, the user is automatically directed to the homepage, or index.html, which displays a table titled "My Reed Log." This table contains all the data that a user inputs on the "Log" page after they finish making an oboe reed. The most recent entries in the table are displayed at the top. There are eight different data points: Date made, Staple number, Shape, Cane, Tie Length, Response, Crow, and Notes, and there are input fields for all of them on the log webpage. Once hitting “submit” on the log page, the user is redirected to the homepage, where their new input data will be displayed as the top row of the table. When the user is on a different page of the website, they can return to the homepage by clicking the "Reed Time" link in the top left of the navigation bar.

Another significant feature of Reed Time is a countdown timer, which can be accessed by clicking "Timer" in the navigation bar. Clicking "Timer" will take the user to a page with an input field where they can choose the number of minutes that the timer should count down from. There is also a table on the page with some suggestions for how many minutes to set the timer based on what step the user is on in the reedmaking process. Since these guidelines are only suggestions and are not strict requirements, there is no need for an option to control how many seconds to count down from in the timer; in other words, there is only a need for integer values of minutes. If one does not input a time before hitting the Set Timer button, or if one enters a negative number, an apology page will pop up. The upper bound for the timer is 60 minutes because one should not be spending more than an hour on one oboe reed. When the timer runs out, the webpage plays a notification sound.

The third feature of Reed Time is a graphical display of the more quantifiable data collected from the Reed Log. First, we have a doughnut graph that compares how many reeds the user makes that have a response ("Yes" in the response column of the log) and how many reeds that do not have a response. The second graph is a bar chart that displays how many reeds the user has made that have a flat crow, a crow that is up to pitch (or in tune), or a sharp crow. These graphs are by no means predictors or complete summarizers of one's reedmaking ability, but they help one look at a bigger picture of the more quantifiable data in the log; it can be difficult to scroll through all the entries in the log.

Finally, the last page of the Reed Time website is a fun page where I share two of my Spotify playlists and offer a form to people to submit song recommendations. Reedmaking can get very frustrating without some fun or inspiring music playing in the background, so this page serves to offer some musical suggestions. There are two Spotify playlists embedded on the webpage that display all the songs, play previews of the songs, and serve as links to Spotify. There is also an input field where one can input a song recommendation to the designer of the website (me!), and a Javascript alert will pop up once the user hits "Submit." After submitting, the input field will be cleared so that one can enter another song title.

One bonus feature that is right next to the link to log out is an "Affirmation" button; clicking this button will make a Javascript alert pop up that says "You got this :)" because reedmaking is a very challenging and frustrating process. Despite how small and simple this feature is, it can be comforting to an oboist who is struggling with a particular reed. 

I designed this website based on what could help me the most while I am making my oboe reeds. I foresee myself using the countdown timer to keep me on track and the log to monitor different aspects of the reeds I make. I hope that this project can help some of my oboist friends as well! Thank you for reading this documentation.

*Note: I cite the sources I reference in DESIGN.md. 



