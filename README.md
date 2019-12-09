    Welcome to SoulMatcher! Get ready to find that special someone! All that must be done to run our website is to download
all the files from our Github link. Then cd into the appropriate directory (most likely our soulmatcher folder), enter flask
run in the terminal, and click the https:// link that shows up. When you enter, you will be mesmerized by the spellbinding home
page, and you will proceed to click the "register" button if you are new to the website. If you already have an account, you can
click the "login" button. In the register page, you will be prompted to enter a username, password, and password confirmation,
which must be unique to the usernames and passwords already in our database. If you do not provide a username or password, an
error message will appear. If your password and password confirmation do not match, an error message will appear. If you
successfully enter a username, password, and password confirmation, you will be directed to enter necessary biographical
information such as name, email, phone number, height, age, gender, sexual orientation, location (state). Each of these are
important either for the pairing process (gender, sexual orientation, and location are necessary to know who is initially
available to be paired with another. Our dealbreakers section include preferred height and age) or for the choosing process
(after our algorithm gives you a list of 3 potential partners, you get to select the person you want to contact to go on a
date!! Name, email, and phone number are essential for this to occur). Our registration page is full of requirements. For
example, your email must be a full email address (@ sign is required), your height must be a positive integer, your phone number
must be written in the XXX-XXX-XXXX format, etc. Once you complete registration, you are directed to the login page of our site.
Again, if you fail to successfully enter your username and password, or if you do not enter a username or password at all, an
error message will appear. However, if you successfully log in, you will enter into SoulMatcher!
    The first part of your pathway to true love is our start page, where you will be prompted to begin your quest.
Next, you will enter into our hand-crafted Personality Test! The Personality Test contains 5 sections, and you are required to
answer each question in a section before you can click next to enter the next section. Further explanation of the Personality
Test and its role in the matching process can be found in DESIGN.md. After you take the Personality Test, you will receive your
personality type with a brief description of what people of your type are generally like. Next, after clicking the “Find your
perfect match” button, you will enter "Dealbreakers" section where you enter some information about your ideal partner that
MUST be true in order for your picture perfect life with them to become a reality. For example, some people care very much that
their partner is younger/older than them, taller/shorter than them, or CLEAN. After the Dealbreakers section, you will be
directed to the Interests/Beliefs section. In this section, you are asked various questions about your personal interests and
beliefs in order to help us narrow down your potential match options (more description in DESIGN.md) Finally, after you
complete the Interests/Beliefs section, you will be given three options. The first option is to be paired with people of your
same personality type. This option is for the narcissists of the world who think "oh all I need in my partner is someone who
is just like me." The second option is to fill out another test for what you BELIEVE to be the ideal personality type of your
future partner. This option puts more control in the hands of the user, and was primarily created for the people of the world
who think "I know exactly what I want. And I'm always right." The third and final option is to be "Soulmatched" which is
recommended as it places the control into the hands of the experts.
    If you select the first option, the algorithm will find people who fit your Dealbreaker requirements, have the same
personality type as you, and have some shared interests/beliefs. Your top 3 matches will be shown to you on our Matches
page. If you select the second option, you will be directed to another test for your ideal partner. Upon completion of that
test, you will be directed to our Matches page where the algorithm will have found the top 3 people who fit your Dealbreaker
requirements, have the personality type that you desire based on the results of your test, and have some shared
interests/beliefs. If you select the third option, we will use our homemade algorithm to match you with the top 3 people who
fit your Dealbreaker requirements, are compatible to your personality type, and who have some shared interests/beliefs. On
the Matches page, you will also be given the option to reshuffle your matches using the options you did not try just to see
what you get. Also, if you have already taken the personality test, you will be redirected to the 3 options page (similar
type, ideal type, soulmatch) if you ever logout and log back in.

The list of files is as follows:
        /static/
            clairdelune.mp3  <!--these are the mp3 files for the audio clips to be played during the interests form-->
            closer.mp3
            everything.mp3
            maadcity.mp3
            icon.ico        <!--the heart emoji icon for our website-->
            styles.css      <!--file containing the css necessary for certain html pages-->
        /templates/
            apology.html    <!--apology template we used from finance that shows server error messages-->
            bio.html        <!--part of the registration form where the user inputs their information-->
            changepassword.html <!--where the user can change their password-->
            dealbreaker.html    <!--part of the matching process where the user inputs their dealbreakers-->
            givematches.html    <!--personalized page right before the match results are shown; the user presses a button to reveal their results!-->
            ideal.html      <!--form for if the user chooses to fill out their ideal personality type of their match-->
            index.html      <!--home page with fancy GIF that welcomes users to our website-->
            interests.html  <!--part of the matching process where the user inputs their interests-->
            layout.html     <!--general html for headers, nav bar, etc. most pages extend this-->
            login.html      <!--login page for users-->
            matchchoice.html    <!--page where the user can select how they want to be matched: either with someone similar, someone of their ideal personality type, or SoulMatched-->
            nomatches.html <!--final results page if the algorithm finds no matches for the user (default number of matches is 3)-->
            onematch.html <!--final results page if the algorithm only finds one match for the user (default number of matches is 3)-->
            personality.html <!--personality test form-->
            register.html <!--user registration form-->
            results1match.html <!--final results page that shows the top match out of the 3 matches found-->
            results2match.html <!--final results page that shows the second match out of the 3 matches found-->
            results3match.html <!--final results page that shows the third match out of the 3 matches found-->
    start.html <!--page with a button to start the personality test and your quest for a lover-->
            testresults.html <!--page that shows the user's results for the personality test-->
            twomatches1.html <!--final results page if the algorithm only finds two matches for the user (default number of matches is 3)-->
        application.py <!--main python script that has the algorithm's functions as well as functions to render the html pages-->
        helpers.py <!--contains some helper functions that are necessary for running the website (we used this file from finance)-->
        soulmatcher.db <!--the SQL database that stores all the information needed for the website-->