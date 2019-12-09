    SoulMatcher features a personality test that is designed to categorize people into personality types. The test, while based off of other personality tests such as Myers-Briggs,
is completely homemade. The test assesses five personality areas in each of the five different sections: introversion vs. extroversion, intuitive vs. sensing, feeling vs. thinking,
prospecting vs. judging, and confident vs. unconfident. Again, most of these personality measures are used in the Myers-Briggs test, but the types of questions we asked and what they
are exactly testing differ considerably from the Myers-Briggs. The answers to each multiple choice question are associated with a value that is used in the tally to determine whether
someone is more introverted or extroverted, intuitive or sensing, etc. For example, if someone answers "true (+1)", "true (+1)", "PARTY (+2)", "Not that interested (0)", "Only talk if
you are talked to (-1)", and "in your element (+2)", they will receive a total score of (1+1+2-1+2) 5 for the first section of the test, which is measuring extroversion (+) vs.
introversion (-). So in the final categorization, this element of their personality will be marked as E for extroversion. This process is repeated for all 5 sections of the test, and
based on the testing, you will be assigned one of thirty-two (2^5) personality types since there are 5 categories and 2 options for each category. For the assignment of the personality
type, we matched each letter combination (ENFPC, ISTJU, etc.) to a specific named personality type and gave each type a description. That is what is shown to the user on their personality
test results page. In order to create these custom types, names, and descriptions, we created a dictionary which can be found on application.py. You will notice that there is also a
description2 which is used in the match results page to describe a match's personality (since the "description" is personalized, using "you" and "you're").
    As for the matching algorithm that pairs users, it starts by classifying people into genders and sexual orientations, or preferred gender of partner. This is necessary in order to
see who is available to pair with each other. For example, if there is a male that is attracted to a female but the only other users on the database are females that are attracted to
females, the male would not have an available match. After people are given their personality type as described above, they are asked to fill out their Dealbreakers and Interests/Beliefs.
So in the pairing process, our algorithm classifies the person's ideal personality type based on whether the person selected to be matched with someone of their same personality type, their
ideal personality type that they are redirected to a shortened version of the test for, or their "SoulMatch". All of these personality type matches are based on the person's score on the
personality test, not just the text sequence associated with each person. To accomplish this matching algorithm and to efficiently store user data, we made a sql database called soulmatcher.db
with 5 tables. The users table stores the user information needed for login and to check if the user has taken the personality test yet. It has columns: id, username, hash, test (whether or not
the user has taken the test), and stores the user information. The bio table stores the user’s answers to the registration information and has columns: user_id, name, email, phone, height, age,
gender, prefsex, location. The dealbreakers table stores the user’s answers to the dealbreaker form and has columns: user_id, agemin, agemax, heightmin, heightmax, clean. The personality table
stores the user’s calculated personality trait stores and the user’s personality type (which are calculated using html and javascript on the front-end and then passed into the back-end Python
script). The personality table has columns: user_id, type, IE, NS, FT, PJ, UC. The interests table stores the user’s answers to the interests forms and has columns: user_id, humor, outdoors,
live, music, clair, closer, maadcity, everything, athletic, fan, sport, firstdate, kids, religion, serious, education, valueEd, firstsight, love. In application.py, we used “request.form.get”
to retrieve these values from the forms and used the “INSERT” SQL command to input these values into their respective tables. All of the tables are cohesive and connected by the user_id that
corresponds to each row, which makes it easier to select for a certain user’s information in any given table. Using these SQL tables, we then designed the aforementioned matching algorithm using
Python. We wrote a variety of functions that could be called to perform specific SQL queries and return lists of integers of user_ids based on specific criteria. We decided that the best way to
match people would be to first filter the people by their gender/sexual orientation and dealbreaker preferences. To accomplish this, we first searched through the SQL tables for people of the
right gender and people who had the appropriate sexual orientation. We used the SQL query command “SELECT” to find these matches and stored the user_id’s of the matches in a list of integers
called prefsexMatch. This was implemented as the function prefsexMatches(). We then repeated this for the dealbreakers and queried for people who had matching dealbreaker preferences. These
people were stored in a separate list of integers called dealbreakerMatch. The was implemented as dealbreakerMatches().
    Next, the user would be able to choose their preferred matching method: (1) find people with similar personality types, (2) fill out their ideal personality type and find people who satisfy
this, or (3) use our proprietary SoulMatch algorithm to find a match. For the similar personality matching algorithm, the user_id was passed in as an input and used to query for the user’s
personality trait scores. Then the personality table was queried again and all of the data stored in the table was stored into a list of dictionaries called people. Each person’s personality
trait scores were compared to that of the user’s and the people who had trait scores within +/-2 for each trait were added to the list of integers of user_ids returned by the function. This was
all implemented as the similarMatch() function. For the ideal personality type matching algorithm, the user filled out a form on the front-end that gave the desired trait labels (“I” or “E”, “N”
or “S”, etc.) of their ideal type. Based on the user’s input, the ranges for the trait scores were determined using if statements (i.e. if “E” was input for the first trait, the trait score range
for the first trait would be from 4 to 11). These range values were then used to query for people in the database who had personality trait scores within these ranges. These people were returned
in a list of integers of user_ids. This was all implemented as idealMatch(). For the SoulMatch algorithm, we selected for people who were 6 to 8 trait score points away from the user’s trait scores.
These ranges were calculated and then used to query for people in the database who matched these criteria in a similar manner to the idealMatch function. This was all implemented as the soulmatch()
function. Thus, from these functions, we have found a way to generate three separate lists of user_ids of people who satisfy either the right sexual orientation/gender, dealbreakers, or personality
type, respectively. However, to find matches we need to find the people who satisfy ALL three of these criteria. To find the overlap between these lists, we wrote a function called findMatches()
that accepts the three lists as input and converts them into sets. Then we used the property of sets and used the “&” operator to find the overlap of the sets. These were returned as a new list of
integers of user_ids of all the matches who fulfill the criteria. Then out of the people who satisfy all three of these criteria (the right gender/sexual orientation, dealbreaker preferences, and
personality type), we decided that these matches would be ranked by whoever has the most similar interests/beliefs to the user. We wrote a function called rank() that gives points to each match
for each interest/belief that is the same as the user’s. The match with the greatest number of points is ranked first, and the matches are ranked in descending order of points. The rank() function
returns a new list of ranked user_ids. To accomplish this, we queried into the interests table for the user’s answers to the interest form and stored these in a dictionary called user. Then for
each number in the list of user_ids passed into the rank() function, we queried into the interests table to find the match’s answers to the interest form and stored these in a dictionary called
match. Then using if statements, the user’s answers were compared to each match’s and points were added if they had the same values. To rank the user_ids by their point values, we created a list
of dictionaries called sums that maps the user_ids to their corresponding point values. Then we wrote a loop to find the max points value in sums and add the corresponding user_id to the final
list of ranked user_ids. Once a user_id was added to the final list of ranked user_ids, the user was removed from the list of dictionaries and the maximum loop was called again. In this way, the
loop repeats until all of the user_ids are stored in the ranked list and sum is empty.  To render the results html files with the correct information for the top three matches, we created a global
variable called final that stores the user_ids of the ranked list returned by the rank() function. The values in final were then used to query into the database and get the relevant information for
the matches to be displayed on the results page. The length of final was checked to make sure that the user had at least three matches to be displayed on the results page. If the user only had one
match, then a separate results page html file was rendered to only display the one match. If the user only had two matches, similarly, the different results html file pages were rendered accordingly.
If the user had no matches, then a separate results html file page was rendered with an apology.
	To display the personality names and descriptions for the personality test results page, we created a global variable called personalitytypes that is a list of dictionaries that stores the
personality type names and descriptions in an easily accessible format. For example, in the testresults.html page, the user’s personality type name and type description were easily accessed by using
the “type” and “description” key values to extract values from the dictionary and pass them into the html file as arguments. We also decided to add personalization on the match results page by
displaying the user’s name on the screen. This was done by querying into the database and finding the user’s name using their user_id. This name was then passed into the html file as an argument.
Other features were also implemented similarly by passing in arguments into the html files. For most of the pages, we used a simple “post” method to move from page to page. However, for the html
templates with multiple choice “radio” buttons, we instead used onclick functions as it was required to go through each multiple choice option to verify which value is checked. When we ran the
function from the button, we were able to submit the form with hidden inputs by selecting the correct id and running the program. In addition, for the final results page we had to have multiple
html templates so that we could account for when a user had less than three matches. For example, when there are only two matches we had to get rid of the right arrow through rendering a new html page.
For the front-end, we mainly referenced online sources to modify html and css code for things such as the typewriter effect, the form buttons, etc. We utilized javascript to compute the personality
types in the front-end and we used forms to pass input values from html into the Python script via “request.form.get”. Through our usage of html, css, bootstrap, Python and SQL we were able to create
an aesthetic front-end and robust back-end that accomplished our goals for our dating/personality test website. We hope you enjoy SoulMatch!