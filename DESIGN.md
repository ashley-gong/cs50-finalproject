# Design of Reed Time

I decided to implement Reed Time as a web-based application using Python/Flask, HTML/CSS, and SQL, much like the implementation of the Finance problem set. I heavily referenced Finance, the Flask short on the CS50 website, and W3Schools in my implementation of Reed Time.


# SQL Components

One of the first things I did after starting this project was to create a SQL database called reedtime.db, which would store two tables: one for login information, and one for the information the user inputs into the reedmaking log. I created both tables by executing CREATE TABLE functions in the terminal while running SQLite3, as I did for the CS50 Finance pset, and I also included those functions as CREATE TABLE IF NOT EXISTS in app.py using db.execute. 


# Python: app.py and helpers.py

As we learned in the lecture on Flask, I created app.py and helpers.py to contain Python functions for the server-side. Helpers.py contains the helper functions for rendering an apology HTML page with a custom message, as well as the login.required decorator, both of which I took from helpers.py in Finance. In app.py, I copied many of the app configurations at the top of the file and more complex functions from Finance (after_request, errorhandler). 


# Register, Login, Logout, Apology, Layout

Other features of my project that reference Finance are the layout.html page and the HTML/Python combinations for Register, Login, and Logout. The register and login functions are similar; both involve obtaining the inputs from the username and password (and password confirmation) fields and rendering an apology if there are errors. Once a unique username and password have been submitted via POST, the register function generates a hash for the password, stores both the username and the password hash into the users table in reedtime.db, and redirects the user the login page. On the login page, the Python function will check if the input matches any of the rows in the users table (utilizing the check_password_hash function), and, if so, directs the user to the index homepage. 

I also took the logout function from Finance; by clicking the logout link in the navigation bar, the session is cleared, directing the user back to the login page.

The layout HTML page acts a template for all of the pages for the website; I coded the navigation bar and included the necessary < script > tags (for Bootstrap, JS graphs, etc.) and used Jinja to reference the code in the rest of the HTML files. 


# Timer and Timer2

The timer function was one of the more complex elements to implement. In app.py, I render two different pages with the render_template function based on the GET or POST routes; if the request.method is GET, the server renders timer.html, which is the page where the user sets how many minutes the timer should count down from. The timer.html file includes an input field to set the number of minutes for the countdown timer (which must be between 0 and 60), a button to submit, and a table underneath displaying timer suggestions. Not inputting any minutes, inputting negative minutes, or inputting a value above 59 will result in an apology. I store the input in the variable "minutes," which is rendered in the timer2.html template.

When the user hits the submit button, effectively using the POST route, the server renders timer2.html, which is the actual timer. I coded the timer using Javascript and based my design on the timer from https://www.codegrepper.com/code-examples/javascript/javascript+countdown+timer+minutes%2C+seconds. First, the window.onload event makes it so that the timer starts automatically after the page loads, with a delay of about one second. Then, I declare two variables for the starting number of minutes and seconds. For the minutes, I use document.getElementbyId().innerHTML to reference a hidden HTML element that contains the Jinja from the input field on the previous page because using the Jinja double curly braces in Javascript caused problems in the workspace of VScode. I initialize the number of seconds at 59 because of the one-second delay at the start of the timer. To make the seconds count down, I use the setInterval() function so that every 1 second (or 1000 milliseconds), the seconds variable (sec) decreases by 1, changing the display. I also initialize the minutes display to start from minute - 1; e.g. if I set a timer for 5 minutes, the page will first load 5:00 in the HTML before switching to 4:59 after the setInterval() function runs for the first time. The setInterval() function keeps running and decreases the minute by 1 after the seconds hit 0, and I also format single-digit seconds to appear with a "0" before the digit so that the timer looks like a standard digital timer. 

When the timer hits 0:00, I use the clearInterval() function to stop the setInterval() function from running, change the display to "Time's Up :)," and play an alert sound that I imported. The condition I designated checks whether the minutes become negative (if (minute <= 0)) and stops the clock before it becomes -1:59. Once the timer ends, the user can click the "Reset" link to direct back to timer.html and set a new timer, or the "Log" link to go to the form for inputting reedmaking data. As an extra display, I include two Bootstrap alerts: one with a link to a background music playlist, and one that clarifies that there is no pause button for the timer (there is no need for one during reedmaking). 


# Log and Index

Once the user is finished with making a reed, they can input data about the reed on the log.html page. In app.py, accessing the page via GET brings the user to the log form with 8 different input fields: date, staple, cane, shape, tie length, response, crow, and notes. I store the input values into variables in app.py using request.form.get() and after hitting submit (POST method), input these variables into the reeds table of my SQL database by using the INSERT INTO function. Hitting “submit” also redirects the user to the homepage, index.html.

The homepage directly displays the reeds table from the reedtime.db SQL database, using Bootstrap to make it more aesthetically designed. The app.py index function gets all the data from the table besides user_id using a SELECT query and returns this dictionary (called "reeds")for the index.html file. Crucially, I use "ORDER BY DESC" in my query so that the most recent table entries will appear on top. Then, I use a Jinja for loop to print each row of the table in index.html for the user to see. The text in each table row is the value for each key in the reeds dictionary.

# Patterns

Another feature of Reed Time is a page that displays graphs for two of the data points in the reedmaking: response and crow. Since the response of a reed is a yes or no data point, and there are only three options for the crow, I can display the former in a doughnut graph and the latter in a bar chart. To obtain the data for how many "yes" or "no" responses there are (and similarly for the crow data points), I used the COUNT() function in my SELECT queries, which returned a list that contained a dictionary with one element: the key was "COUNT(response)" (or "COUNT(crow)"), and the value was the number to input into the graph. As such, I accessed that value by doing (db.execute...)[0]["COUNT(____)"] and stored these numbers into variables that I passed into patterns.html. 

To display the graph, I used Javascript with documentation from W3Schools: https://www.w3schools.com/js/js_graphics_chartjs.asp. I first added a link to the CDN (content delivery network) in the <head> of layout.html, and then directly used Javascript and HTML on patterns.html. The <canvas> HTML tag displays the graph, while the < script > contains the attributes and data values for the graph. Just like the timer/timer2 pages, I used Jinja in hidden HTML elements to pass the data from the SQL database into the HTML file and then referenced the hidden HTML elements with 
document.getElementbyId().innerHTML. As the reeds table updates from more and more log entries, the graphs also change. 


# Music and Affirmation

The music.html page is the only static HTML page in which I do not use any Flask on the back-end for its implementation. To embed the Spotify playlists, I used the <iframe> tag and copied the code that Spotify provides. I do use Javascript for the song recommendation input form to make an alert appear when one hits the "submit" button, and I referenced the Trivia lab while implementing this feature. In the Javascript code, I added an event listener to the button after the DOMContentLoaded event, such that when the user clicks the button, the alert will pop up. Since I designed two different alerts based on whether the user entered anything into the song recommendation form, I used "if" statements and the document.querySelector on the input field to designate two different outcomes. Similarly, I use this Javascript alert for the bonus Affirmation button in the navigation bar, although there is only one alert for the Affirmation.


# Bootstrap, CSS, and other Design Attributes

For the aesthetic design of my project, I used both Bootstrap and my own CSS code. The Bootstrap docs I used were similar to the ones used in Finance, although I changed the color scheme and some fonts by using my own CSS, whether in styles.css or as a style attribute in the HTML. I also used the <center> tag frequently in my HTML to make elements center-aligned on the page. 
