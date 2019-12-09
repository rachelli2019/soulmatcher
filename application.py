import os

# Hi please enjoy viewing our application.py file. we hope you enjoyed using Soulmatch!
# From Rachel, Eton and Isaiah

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

"""
additional sources referenced and used during our project:
https://www.w3schools.com/html/html_form_input_types.asp
https://www.w3schools.com/jsref/prop_html_innerhtml.asp
https://teamtreehouse.com/library/http-basics/get-and-post-requests-in-a-browser/using-forms-for-get-requests
https://www.w3schools.com/html/html_form_input_types.asp
https://www.w3schools.com/tags/att_input_type_hidden.asp
https://www.w3schools.com/jsref/prop_text_value.asp
https://www.w3schools.com/html/html_forms.asp
https://www.w3schools.com/js/js_validation.asp
https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementsByTagName
https://stackoverflow.com/questions/1423777/how-can-i-check-whether-a-radio-button-is-selected-with-javascript
http://javascript-coder.com/javascript-form/javascript-get-check.phtml
https://www.w3schools.com/howto/howto_js_form_steps.asp
"""
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQLite database
db = SQL("sqlite:///soulmatcher.db")

# list of user_ids of the matches!
final = []
prefsexMatch = []
dealbreakerMatch = []

# set up the array of dictionaries of personality types
personalitytypes = [ {"type": "ENFPC", "name": "SOCIAL BUTTERFLY", \
    "description": "You are a social butterfly. You can be the life of the party when you want to and you really enjoy being with people. \
    You are friendly, curious, observant, and popular. However, you’re a bit impractical and you get stressed easily. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Social butterflies can be the life of the party when they want to and they really enjoy being with people. They are friendly, curious, observant, and popular."},\
    {"type": "ENFPU", "name": "NICE POPULAR BOI", \
    "description": "You are cool! Friendly, curious, observant, and even popular! You need to be more confident! But it’s ok we’ll find the perfect person for you!", \
    "description2": "Nice popular bois are friendly, curious, observant, and popular."},\
    {"type": "ENFJC", "name": "HERCULES", \
    "description": "In the grand story of life, you are the protagonist. You have strong character, are confident, charismatic, and a natural leader. \
    However, you can be a little bit too idealistic and sensitive. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Hercules have strong character, are confident, charismatic, and natural leaders."},\
    {"type": "ENFJU", "name": "FRODO BAGGINS", \
    "description": "You are born to be a protagonist. You are reliable, altruistic, and a natural leader. You may not believe in yourself just yet, but it’s ok we’ll find \
    the perfect person for you!", \
    "description2": "Frodo Baggins are born to be protagonists. They are reliable, altruistic, and natural leaders."},\
    {"type": "ENTPC", "name": "LAWYER", \
    "description": "You are a great debater. You are an analyst, you’re charismatic, and you’re a good devil’s advocate. However, especially in terms of finding a partner, \
    you can be a bit too argumentative. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Lawyers are great debater. They are analysts, charismatic, good devil’s advocates."},\
    {"type": "ENTPU", "name": "DEBATE TEAM BOI", \
    "description": "You are a natural debater. You are able to analyze and play the devil’s advocate. However, you need more confidence! But it’s ok we’ll find the perfect person for you!", \
    "description2": "Debate team bois are natural debaters. They are able to analyze and play the devil’s advocate."},\
    {"type": "ENTJC", "name": "LEADER", \
    "description": "You’re a natural leader. You are confident in yourself and you can lead a group efficiently. Be careful… you can be a little too stubborn and dominant at times. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Leaders are confident in themselves and they can lead a group efficiently."},\
    {"type": "ENTJU", "name": "BLOSSOMING FLOWER", \
    "description": "Believe in yourself! You were born to be a leader. You just need a little boost of confidence. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Believe in yourself! You were born to be a leader. You just need a little boost of confidence. But it’s ok we’ll find the perfect person for you!"},\
    {"type": "ESFPC", "name": "PARTY LIFE", \
    "description": "You are the life of the party. You're energetic, confident, attractive, and live in the moment. You’re also… slightly… too much sometimes. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "The life of the party. Party lifers are energetic, confident, attractive, and live in the moment."},\
    {"type": "ESFPU", "name": "WOOHOO", \
    "description": "You are an entertainer. You are a partier. You are energetic and live in the moment. You also need a confidence boost… but it’s ok we’ll find the perfect person for you!",\
    "description2": "Woohoos are entertainers. They are energetic and live in the moment."},\
    {"type": "ESFJC", "name": "THE MAN", \
    "description": "You are the quarterback of the high school football team, the head cheerleader, the popular person. People want to be you! You are loyal, warm,\
    and good at connecting with others. \
    However, you can be a bit inflexible and reluctant to improvise. But it’s ok we’ll find the perfect person for you!", \
    "description2": "The mans are the quarterback of the high school football team, the head cheerleader, the popular person. They are loyal, warm, and good at connecting with others."},\
    {"type": "ESFJU", "name": "ALMOST THE MAN", \
    "description": "You are cool, popular, and people want to be you! You are loyal, warm, and good at connecting with others. However, you’re too worried about your social \
    status and you need to be more confident! \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Almost the mans are cool and popular. They are loyal, warm, and good at connecting with others."},\
    {"type": "ESTPC", "name": "BALLER", \
    "description": "You’re a baller. You are risk taking, bold, and sociable. However, you can be a bit impatient and unstructured. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Ballers are ballers. They are risk taking, bold, and sociable."},\
    {"type": "ESTPU", "name": "MINI BALLER", \
    "description": "You’re a baller… you just need to believe it! You are risk taking, bold, and sociable. You need to be more confident! But it’s ok we’ll find the perfect person for you!", \
    "description2": "You’re a baller… you just need to believe it! You are risk taking, bold, and sociable. You need to be more confident! But it’s ok we’ll find the perfect person for you!"},\
    {"type": "ESTJC", "name": "CEO", \
    "description": "You are extremely practical and strong-willed. You have good administration skills and you enforce order. However, you can be a bit too inflexible and stubborn. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "CEOs are extremely practical and strong-willed. They have good administration skills and they enforce order."},\
    {"type": "ESTJU", "name": "BOSS", \
    "description": "You are very practical and strong-willed. You have good administration skills and you are very reliable. You need to be more confident! But it’s ok we’ll \
    find the perfect person for you!", \
    "description2": "Bosses are very practical and strong-willed. They have good administration skills and are very reliable."},\
    {"type": "INFPC", "name": "IDEALIST", \
    "description": "You’re always looking to make things better. You are creative, open-minded, passionate, and hard-working. However, you can be a little too idealistic and impractical. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Idealists are always looking to make things better. They are creative, open-minded, passionate, and hard-working."},\
    {"type": "INFPU", "name": "PERFECTIONIST", \
    "description": "You’re always looking to make things better. You are creative, open-minded, passionate, and hard-working. However, you apply your perfectionism to yourself a bit too much. \
    You need to be more confident! \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Perfectionists are always looking to make things better. They are creative, open-minded, passionate, and hard-working."},\
    {"type": "INFJC", "name": "INSPIRATION", \
    "description": "You are inspirational. You are a rare type of person… and the world needs more people like you. You fight for what you believe in and you really care about people. \
    However, you can be a sensitive at time. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Inspirations are inspirational. They are a rare type of person… and the world needs more people like them. They fight for what they believe in and they really \
    care about people."},\
    {"type": "INFJU", "name": "WISE BOI", \
    "description": "You were born to be special. You are rare, and you can do so much to help the world. You care about people and really have a good heart. You need more confidence!! \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Wise bois were born to be special. They are rare, and they can do so much to help the world. They care about people and really have a good heart."},\
    {"type": "INTPC", "name": "NERD", \
    "description": "You’re a nerd. Hey, you are a rare type. You are creative, intellectual, and confident. You’re also a little insensitive and private… but it’s ok we’ll find the \
    perfect person for you!", \
    "description2": "Nerds are a rare type. They are creative, intellectual, and confident."},\
    {"type": "INTPU", "name": "PHILOSOPHER", \
    "description": "You’re smart. You’re creative. But you need to be more confident!! it’s ok though, we’ll find the perfect person for you!",
    "description2": "Philsophers are smart. They’re creative."},\
    {"type": "INTJC", "name": "A SHINY POKEMON", \
    "description": "You are a very very rare type of person. You are quick, imaginative, independent, and decisive. You are hard-working, yet open-minded. \
    And you’re good at a lot of things. However, you can be a bit arrogant and judgemental. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Shiny pokemon are very very rare. They are quick, imaginative, independent, and decisive. They are hard-working, yet open-minded. And they’re good at a lot of things."},\
    {"type": "INTJU", "name": "BOOKWORM", \
    "description": "You are filled with knowledge. You are quick, imaginative, independent, and decisive. You are a super duper rare type of person. Be proud of who you are! \
    You need to be more confident. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Bookworms are filled with knowledge. They are quick, imaginative, independent, and decisive. They are a super duper rare type of person."},\
    {"type": "ISFPC", "name": "DORA THE EXPLORER", \
    "description": "You cannot be put in a box. You live in a different world than everyone else. It’s a world full of wonder and color, and there is no end to your imagination. \
    You are passionate, curious, and artistic. \
    However, you can be a bit too independent and unpredictable. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Dora the Explorers cannot be put in a box. They live in a different world than everyone else. It’s a world full of wonder and color, and there is no end to their imagination.  \
    They are passionate, curious, and artistic."},\
    {"type": "ISFPU", "name": "BLUE FROM BLUE’S CLUES", \
    "description": "You live to explore! Your world is full of wonder and color, and there is no end to your imagination. You are passionate, curious, and artistic. However, \
    you need to be more confident. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Blues live to explore! They’re world is full of wonder and color, and there is no end to their imagination. You are passionate, curious, and artistic."},\
    {"type": "ISFJC", "name": "DOCTOR", \
    "description": "You are a universal helper. You are kind, altruistic, reliable, patient, and practical. However, you can take things a bit too personally and repress your feelings. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Doctors are universal helpers. They are kind, altruistic, reliable, patient, and practical."},\
    {"type": "ISFJU", "name": "NURSE", \
    "description": "You are a universal helper. You are kind, altruistic, reliable, patient, and practical. However, you are shy and you need to be more confident! \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Nurses are universal helpers. They are kind, altruistic, reliable, patient, and practical."},\
    {"type": "ISTPC", "name": "INNOVATOR", \
    "description": "You love the challenge, and you believe you have the tools to overcome it. You are optimistic, energetic, and great in crisis situations. \
    However, you can be a bit stubborn and insensitive. But it’s ok we’ll find the perfect person for you!", \
    "description2": "Innovators love the challenge, and they believe they have the tools to overcome it. They are optimistic, energetic, and great in crisis situations."},\
    {"type": "ISTPU", "name": "CREATIVE", \
    "description": "You are so creative. You are innovative, optimistic, energetic, and great in crisis situations. You need to believe in yourself more!! \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Creatives are so creative. They are innovative, optimistic, energetic, and great in crisis situations."},\
    {"type": "ISTJC", "name": "NORMAL", \
    "description": "There are a lot of people like you. You are honest, dutiful, responsible, and practical. However, you live life a little too close to the books. \
    But it’s ok we’ll find the perfect person for you!", \
    "description2": "Normals are honest, dutiful, responsible, and practical."},\
    {"type": "ISTJU", "name": "BASIC",
    "description": "You may be in the most populated personality type, but that doesn’t mean you aren’t great! You are honest, dutiful, responsible, and practical. \
    And you need to be more confident! But it’s ok we’ll find the perfect person for you!", \
    "description2": "Basics are great! They are honest, dutiful, responsible, and practical."} ]

# MATCHING ALGORITHM FUNCTIONS

def prefsexMatches(user_id):
    # return an array of user_ids that have the right preferred sexual orientation
    matches = []
    # M, F, O; M, F, B, O
    # obtain the gender and sexual orientation of the user
    user = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user_id)
    gender = user[0]["gender"] # M, F, O
    prefsex = user[0]["prefsex"] # M, F, B, O
    # if the user is bisexual, select male and female users who have a prefsex = user's gender
    if prefsex == "B":
        people = db.execute("SELECT * FROM bio WHERE (gender = 'M' OR gender = 'F') AND prefsex = :sex", sex=gender)
        for person in people:
            if person["user_id"] != user_id:
                matches.append(person["user_id"])
        return matches
    # if the user prefers other genders or is of the other gender and prefers either males or females; select for ppl with the opposite prefsex and gender
    elif prefsex == "O" or gender == "O":
        people = db.execute("SELECT * FROM bio WHERE gender=:gender AND prefsex = :sex", gender=prefsex, sex=gender)
        for person in people:
            if person["user_id"] != user_id:
                matches.append(person["user_id"])
        return matches
    # if the user is heterosexual, select for ppl of the opposite gender who have the opposite prefsex or are bisexual
    else:
        people = db.execute("SELECT * FROM bio WHERE gender = :gender AND (prefsex = :sex OR prefsex = 'B')", gender=prefsex, sex=gender)
        for person in people:
            if person["user_id"] != user_id:
                matches.append(person["user_id"])
        return matches

def dealbreakerMatches(user_id):
    # return an array of user_ids that are dealbreaker matches
    matches = []
    # store the dealbreakers of the user
    pref = db.execute("SELECT * FROM dealbreakers WHERE user_id = :user", user=user_id)
    print(pref)
    heightmin = pref[0]["heightmin"]
    heightmax = pref[0]["heightmax"]
    agemin = pref[0]["agemin"]
    agemax = pref[0]["agemax"]
    clean = pref[0]["clean"]
    userLocation = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user_id)
    loc = userLocation[0]["location"]
    # store dictionary of all people and their bios
    people = db.execute("SELECT * FROM bio")
    # select for people with the preferred traits (height, age, cleanliness, location) using nested if statements
    for person in people:
        if heightmin <= person["height"] <= heightmax:
            if agemin <= person["age"] <= agemax:
                if loc == person["location"]:
                    personDealbreakers = db.execute("SELECT  * FROM dealbreakers WHERE user_id = :user", user=user_id)
                    if clean == personDealbreakers[0]["clean"]:
                        if user_id != person["user_id"]:
                            matches.append(person["user_id"])
    return matches

def idealMatch(user_id, t1, t2, t3, t4, t5):
    # 5 traits of significant other's desired personality type determined by what the user inputs into the form
    # return an array of user_ids of users with the right personality match
    matches = []
    # find the desired ranges of the traits
    if t1 == "H":
        min1 = 4
        max1 = 11
    elif t1 == "L":
        min1 = -11
        max1 = -4
    else:
        min1 = -3
        max1 = 3

    if t2 == "H":
        min2 = 4
        max2 = 11
    elif t2 == "L":
        min2 = -10
        max2 = -4
    else:
        min2 = -3
        max2 = 3

    if t3 == "H":
        min3 = 3
        max3 = 7
    elif t3 == "L":
        min3 = -7
        max3 = -3
    else:
        min3 = -2
        max3 = 2

    if t4 == "H":
        min4 = 4
        max4 = 9
    elif t4 == "L":
        min4 = -10
        max4 = -4
    else:
        min4 = -3
        max4 = 3

    if t5 == "H":
        min5 = 4
        max5 = 10
    elif t5 == "L":
        min5 = -10
        max5 = -4
    else:
        min5 = -3
        max5 = 3
    # select the people who have the personality values within the range of the preferred traits
    people = db.execute("SELECT * FROM personality WHERE (IE BETWEEN :min1 AND :max1) \
    AND (NS BETWEEN :min2 AND :max2) \
    AND (FT BETWEEN :min3 AND :max3) \
    AND (PJ BETWEEN :min4 AND :max4) \
    AND (UC BETWEEN :min5 AND :max5)", \
    min1 = min1, max1 = max1, \
    min2 = min2, max2 = max2, \
    min3 = min3, max3 = max3, \
    min4 = min4, max4 = max4, \
    min5 = min5, max5 = max5 )
    # store the user_ids of the matches in an array
    for person in people:
        if person["user_id"] != user_id:
                matches.append(person["user_id"])
    return matches

def soulmatch(user_id):
    # return an array of user_ids that are matches according to the soulmatch algorithm
    matches = []
    # query for the user's personality trait scores
    user = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user_id)
    # store the desired scores for the matches based on the user's score for each trait
    t1 = user[0]["IE"]
    if t1 >= 0:
        m1 = t1 - 8
    else:
        m1 = t1 + 6

    t2 = user[0]["NS"]
    if t2 >= 0:
        m2 = t2 - 8
    else:
        m2 = t2 + 6

    t3 = user[0]["FT"]
    if t3 >= 0:
        m3 = t3 - 6
    else:
        m3 = t3 + 4

    t4 = user[0]["PJ"]
    if t4 >= 0:
        m4 = t4 - 7
    else:
        m4 = t4 + 5

    t5 = user[0]["UC"]
    if t5 >= 0:
        m5 = t5 - 7
    else:
        m5 = t5 + 5
    # query into the database and select for people with traits in the specified ranges (ex. for trait 1, m1 +/- 2)
    people = db.execute("SELECT * FROM personality WHERE (IE BETWEEN :min1 AND :max1) \
    AND (NS BETWEEN :min2 AND :max2) \
    AND (FT BETWEEN :min3 AND :max3) \
    AND (PJ BETWEEN :min4 AND :max4) \
    AND (UC BETWEEN :min5 AND :max5)", \
    min1 = m1, max1 = m1+2, \
    min2 = m2, max2 = m2+2, \
    min3 = m3, max3 = m3+2, \
    min4 = m4, max4 = m4+2, \
    min5 = m5, max5 = m5+2 )
    # store the user_ids of the matches in an array
    for person in people:
        if person["user_id"] != user_id:
            matches.append(person["user_id"])
    return matches

def similarMatch(user_id):
    # return an array of user_ids of people with similar trait values
    matches = []
    # get user personality info
    user = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user_id)
    IE = user[0]["IE"]
    NS = user[0]["NS"]
    FT = user[0]["FT"]
    PJ = user[0]["PJ"]
    UC = user[0]["UC"]
    # query for the rest of the people's personality traits in the database
    people = db.execute("SELECT * FROM personality")
    # find people with similar scores for each personality trait
    for person in people:
        print(IE)
        print("-")
        print(person["IE"])
        if abs(IE - person["IE"]) <= 2 and abs(NS-person["NS"]) <= 2 and abs(FT-person["FT"]) <= 2 and abs(PJ-person["PJ"]) <= 2 and abs(UC-person["UC"]) <= 2 and person["user_id"] != user_id:
            matches.append(person["user_id"])
    return matches


def findMatches(prefsex, dealbreaker, personalityMatches):
    # parse through the lists of user_ids and find people that satisfy all three criteria: sexual orientation, dealbreakers, personality type
    prefsexSet = set(prefsex)
    dealbreakerSet = set(dealbreaker)
    personalitySet = set(personalityMatches)
    return prefsexSet & dealbreakerSet & personalitySet

def rank(user_id, matches):
    # matches is the list of people who satisfy the three criteria: sexual orientation, dealbreakers, personality type
    # ranks the matches based on interests and beliefs
    # each potential match is given points for each matching interest or belief, resulting in a weighted sum
    # return a ranked list of user_ids
    ranks = []
    # create an array of dictionaries that match the user_ids to their respective sums
    sums = []
    # query for the user's interests and beliefs
    user = db.execute("SELECT * FROM interests WHERE user_id = :user", user=user_id)
    print(user)
    for num in matches:
        # point tally to keep track of total sums for each potential match
        points = 0
        # query for the match's interests and beliefs
        match = db.execute("SELECT * FROM interests WHERE user_id = :user", user=num)
        print(match)
        # compare the user's interests/beliefs to the match
        #  user_id, humor, outdoors, live, music, clair, closer, maadcity, everything, athletic, fan, sport, food, firstdate, kids, religion, serious, education, valueEd, firstsight, love

        if user[0]["humor"] == match[0]["humor"]:
            points += 1
        if user[0]["outdoors"] == match[0]["outdoors"]:
            points += 1
        if user[0]["live"] == match[0]["live"]:
            points += 1
        if user[0]["music"] == match[0]["music"]:
            points += 1
        if user[0]["clair"] == match[0]["clair"]:
            points += 1
        if user[0]["closer"] == match[0]["closer"]:
            points += 1
        if user[0]["maadcity"] == match[0]["maadcity"]:
            points += 1
        if user[0]["everything"] == match[0]["everything"]:
            points += 1
        if user[0]["athletic"] == match[0]["athletic"]:
            points += 1
        if user[0]["fan"] == match[0]["fan"]:
            points += 1
        if user[0]["sport"] == match[0]["sport"]:
            points += 1
        if user[0]["firstdate"] == match[0]["firstdate"]:
            points += 1
        if user[0]["kids"] == match[0]["kids"]:
            points += 1
        if user[0]["serious"] == "veryserious":
            if user[0]["religion"] == match[0]["religion"]:
                points += 2 # religion points are weighted more if both parties are serious about religion
            if user[0]["serious"] == match[0]["serious"]:
                points += 2
        else:
            if user[0]["religion"] == match[0]["religion"]:
                points += 1
            if user[0]["serious"] == match[0]["serious"]:
                points += 1
        if user[0]["education"] == match[0]["education"]:
            points += 1
        if user[0]["valueEd"] == match[0]["valueEd"]:
            points += 1
        if user[0]["firstsight"] == match[0]["firstsight"]:
            points += 1
        if user[0]["love"] == match[0]["love"]:
            points += 1

        # add the points total to the dictionary of sums
        userPoints = {"user_id": num, "points": points}
        sums.append(userPoints)
    # sort the match dictionaries by greatest to least points
    # find the max points in the list and add the corresponding user_id to the ranks list
    while len(sums) > 0:
        maxpoints = 0
        for i in range(len(sums)):
            if sums[i]["points"] >= maxpoints:
                maxpoints = sums[i]["points"]
                saveid = sums[i]["user_id"]
                toDelete = i
        ranks.append(saveid)
        sums.remove(sums[toDelete])
    return ranks

# END OF MATCHING ALGORITHM FUNCTIONS

@app.route("/")
def index():
    # home page for soulmatcher animation
    return render_template("index.html")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE id = :user", user=session["user_id"])
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("current password incorrect")
            return render_template("changepassword.html")
        elif request.form.get("confirm") != request.form.get("newpassword"):
            flash("passwords do not match")
            return render_template("changepassword.html")
        password = request.form.get("newpassword")
        hash1 = generate_password_hash(password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", (hash1, session["user_id"]))
        return redirect("/login")
    else:
        return render_template("changepassword.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username/password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # if the user has already taken the personality test, redirect them to their results
        taken = db.execute("SELECT test FROM users WHERE username = :username", username=request.form.get("username"))
        if taken[0]["test"] == "Y":
            return redirect("/matchchoice")

        # if the user is a new user, redirect user to start page for the personality test
        return render_template("start.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/start", methods=["GET", "POST"])
def start():
    # start button for the personality test
    if request.method == "POST":
        return render_template("personality.html")
    # start the personality test with the bio form
    return render_template("start.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # error message if password does not match confirmation
    if request.method == "POST":
        if not request.form.get("confirmation") or request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords do not match")
            return render_template("register.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # if username already exists give error message
        if len(rows) > 0:
            flash("Username already exists")
            return render_template("register.html")

        # insert the user information to the database
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = :username",
                           username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # render the bio
        return render_template("bio.html")
    else:
        return render_template("register.html")

@app.route("/bio", methods=["GET", "POST"])
def bio():
    if request.method == "POST":
        # store the form answers
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("pnumber")
        height = request.form.get("height")
        age = request.form.get("age")
        gender = request.form.get("gender")
        prefsex = request.form.get("prefsex")
        location = request.form.get("state")

        # insert the user information to the database
        rows = db.execute("INSERT INTO bio (user_id, name, email, phone, height, age, gender, prefsex, location) \
        VALUES (:user, :name, :email, :phone, :height, :age, :gender, :prefsex, :location)", \
        user=session["user_id"], name=name, email=email, phone=phone, height=height, age=age, gender=gender, prefsex=prefsex, location=location)

        # notify user of successful registration
        flash("Successfully registered!")

        # return to the login page
        return render_template("login.html")
    else:
        return render_template("bio.html")

@app.route("/dealbreaker", methods=["GET", "POST"])
def dealbreaker():
    if request.method == "POST":
        # show error messages if user input doesn't make sense
        if request.form.get("agemax") < request.form.get("agemin"):
            flash("Maximum age must be larger than minimum age")
            return render_template("dealbreaker.html")
        elif request.form.get("heightmax") < request.form.get("heightmin"):
            flash("Maximum height must be larger than minimum height")
            return render_template("dealbreaker.html")

        # store user info
        agemin = int(request.form.get("agemin"))
        agemax = int(request.form.get("agemax"))
        heightmin = int(request.form.get("heightmin"))
        heightmax = int(request.form.get("heightmax"))
        clean = request.form.get("clean")

        # insert user info into the database
        rows = db.execute("INSERT INTO dealbreakers (user_id, agemin, agemax, heightmin, heightmax, clean) \
        VALUES (:user, :agemin, :agemax, :heightmin, :heightmax, :clean)", \
        user=session["user_id"], agemin=agemin, agemax=agemax, heightmin=heightmin, heightmax=heightmax, clean=clean)

        # move on to the interests page test
        return render_template("interests.html")
    else:
        return render_template("dealbreaker.html")

@app.route("/personality", methods=["GET", "POST"])
def personality():
    if request.method == "POST":
        x = request.form.get("result")
         # 'x' REPRESENTS THE PERSONALITY code OF THE PERSON
         # match the personality code to the name and the description
        for ptype in personalitytypes:
            if ptype["type"] == x:
                # store the name and description of the personality type
                description = ptype["description"]
                name = ptype["name"]
        IE = request.form.get("IE") # VALUE FOR IE
        NS = request.form.get("NS") # VALUE for NS
        FT = request.form.get("FT") # VALUE for FT
        PJ = request.form.get("PJ") # VALUE for PJ
        UC = request.form.get("UC") # VALUE for UC

        # insert user personality trait values into the database
        rows = db.execute("INSERT INTO personality (user_id, type, IE, NS, FT, PJ, UC) \
        VALUES (:user, :ptype, :IE, :NS, :FT, :PJ, :UC)", \
        user=session["user_id"], ptype=x, IE=IE, NS=NS, FT=FT, PJ=PJ, UC=UC)

        # record down that the user has already taken the test for future login reference
        taken = db.execute("UPDATE users SET test=:taken WHERE id = :user", taken = "Y", user=session["user_id"])
        print(IE + NS + FT + PJ + UC)
        # tell the user their personality type
        return render_template("testresults.html", personalitytype=name, description=description)
    else:
        return render_template("personality.html")

@app.route("/interests", methods=["GET", "POST"])
def interests():
    if request.method == "POST":
        # store the user's input
        q1 = request.form.get("q1") # VALUE FOR q1
        q2 = request.form.get("q2") # VALUE for q2
        q3 = request.form.get("q3") # VALUE for q3
        q4 = request.form.get("q4") # VALUE for q4
        q5 = request.form.get("q5") # VALUE for q5
        q6 = request.form.get("q6") # VALUE for q6
        q7 = request.form.get("q7") # VALUE for q7
        q8 = request.form.get("q8") # VALUE for q8
        q9 = request.form.get("q9") # VALUE for q9
        q10 = request.form.get("q10") # VALUE for q10
        q11 = request.form.get("q11") # VALUE for q11
        q12 = request.form.get("q12") # VALUE for q12
        q13 = request.form.get("q13") # VALUE for q13
        q14 = request.form.get("q14") # VALUE for q14
        q15 = request.form.get("q15") # VALUE for q15
        q16 = request.form.get("q16") # VALUE for q16
        q17 = request.form.get("q17") # VALUE for q17
        q18 = request.form.get("q18") # VALUE for q18
        q19 = request.form.get("q19") # VALUE for q19

        # store these answers into the database
        rows = db.execute("INSERT INTO interests (user_id, humor, outdoors, live, music, clair, closer, maadcity, everything, athletic, fan, sport, firstdate, kids,\
        religion, serious, education, valueEd, firstsight, love) \
        VALUES (:user, :q1, :q2, :q3, :q4, :q5, :q6, :q7, :q8, :q9, :q10, :q11, :q12, :q13,\
        :q14, :q15, :q16, :q17, :q18, :q19)", \
        user=session["user_id"], q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10, q11=q11, q12=q12, q13=q13,\
        q14=q14, q15=q15, q16=q16, q17=q17, q18=q18, q19=q19)

        # move onto asking the user for their preferred matching algorithm
        return render_template("matchchoice.html")
    else:
        return render_template("interests.html")

@app.route("/matchchoice", methods=["GET", "POST"])
def matchchoice():
    global final
    # ask the user how they would like to be matched: with a similar personality type, an ideal type they fill out, or soulmatched
    if request.method == "POST":
        user = session["user_id"]
        # query the database for the user's name for a personalized message
        username = db.execute("SELECT name FROM bio WHERE user_id = :user_id", user_id = user)
        name = username[0]["name"]
        choice = request.form.get("choice")
        # if they would like to fill out their ideal type, redirect to the form
        if choice == "ideal":
            return render_template("ideal.html")
            # otherwise, call the functions in algorithm.py to find the matches
            # first, call the appropriate function to find the preferred matches,
            # call the prefsex function to find people of the same sexual orientation,
            # call the dealbreakers function to find people who satisfy the dealbreakers conditions
            # then find the overlap of the people who fit all these criteria
            # then call rank to find the top 5 matches
        elif choice == "similar":
            # if they would like to find similar people, call the similarMatch() function
            similarMatches = similarMatch(user)
            prefsexMatch = prefsexMatches(user)
            dealbreakerMatch = dealbreakerMatches(user)
            overlap = findMatches(prefsexMatch, dealbreakerMatch, similarMatches)
            final = rank(user, overlap)
            return render_template("givematches.html", name=name)

        elif choice == "soulmatch":
            # if they would like to be soulmatched, call the soulmatch() function
            similarMatches = soulmatch(user)
            prefsexMatch = prefsexMatches(user)
            dealbreakerMatch = dealbreakerMatches(user)
            overlap = findMatches(prefsexMatch, dealbreakerMatch, similarMatches)
            final = rank(user, overlap)
            print(final)
            return render_template("givematches.html", name=name)
    else:
        return render_template("matchchoice.html")

@app.route("/ideal", methods=["GET", "POST"])
def ideal():
    user = session["user_id"]
    # query the database for the user's name for a personalized message
    username = db.execute("SELECT name FROM bio WHERE user_id = :user_id", user_id = user)
    name = username[0]["name"]
    choice = request.form.get("choice")
    # store the personality trait values of the user's ideal type
    t1 = request.form.get("q1")
    t2 = request.form.get("q2")
    t3 = request.form.get("q3")
    t4 = request.form.get("q4")
    t5 = request.form.get("q5")
    # call the idealMatch() function from algorithm.py to find possible matches
    # call the prefsex function to find people of the same sexual orientation,
    # call the dealbreakers function to find people who satisfy the dealbreakers conditions
    # then find the overlap of the people who fit all these criteria
    # then call rank to find the top 5 matches
    idealmatches = idealMatch(user, t1, t2, t3, t4, t5)
    prefsexMatch = prefsexMatches(user)
    dealbreakerMatch = dealbreakerMatches(user)
    overlap = findMatches(prefsexMatch, dealbreakerMatch, idealmatches)
    final = rank(user, overlap)
    return render_template("givematches.html", name=name)

@app.route("/results1match", methods=["GET", "POST"])
def results1match():
    global final
    if request.method == "POST":
        # user_id of the top match
        user = final[1]
        # query into the database for the user's bio information
        match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
        # store the match's information
        name = match[0]["name"]
        phone = match[0]["phone"]
        email = match[0]["email"]
        height = match[0]["height"]
        age = match[0]["age"]
        # query for the match's type
        matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
        x = matchtype[0]["type"]
        # store the match's personality type and description
        for ptype in personalitytypes:
                if ptype["type"] == x:
                    # store the name and description of the personality type
                    description = ptype["description2"]
        if len(final) == 2:
            return render_template("twomatches1.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
        return render_template("results2match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
    else:
        # if there are no matches, render apology message to the user
        if not final:
            return render_template("nomatches.html")
        else:
            # user_id of the top match
            user = final[0]
            # query into the database for the user's bio information
            match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
            # store the match's information
            name = match[0]["name"]
            phone = match[0]["phone"]
            email = match[0]["email"]
            height = match[0]["height"]
            age = match[0]["age"]
            # query for the match's type
            matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
            x = matchtype[0]["type"]
            # store the match's personality type and description
            for ptype in personalitytypes:
                    if ptype["type"] == x:
                        # store the name and description of the personality type
                        description = ptype["description2"]
                        ptype = ptype["name"]
            # if there is only one match, render a special template that only displays one match
            if len(final) == 1:
                return render_template("onematch.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
            else:
                return render_template("results1match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)

@app.route("/results2match", methods=["GET", "POST"])
def results2match():
    if request.method == "POST":
        if request.form.get("direct") == "right":
            # user_id of the top match
            user = final[2]
            # query into the database for the user's bio information
            match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
            # store the match's information
            name = match[0]["name"]
            phone = match[0]["phone"]
            email = match[0]["email"]
            height = match[0]["height"]
            age = match[0]["age"]
            # query for the match's type
            matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
            x = matchtype[0]["type"]
            # store the match's personality type and description
            for ptype in personalitytypes:
                    if ptype["type"] == x:
                        # store the name and description of the personality type
                        description = ptype["description2"]
                        ptype = ptype["name"]
            return render_template("results3match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
        elif request.form.get("direct") == "left":
            # user_id of the top match
            user = final[0]
            # query into the database for the user's bio information
            match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
            # store the match's information
            name = match[0]["name"]
            phone = match[0]["phone"]
            email = match[0]["email"]
            height = match[0]["height"]
            age = match[0]["age"]
            # query for the match's type
            matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
            x = matchtype[0]["type"]
            # store the match's personality type and description
            for ptype in personalitytypes:
                    if ptype["type"] == x:
                        # store the name and description of the personality type
                        description = ptype["description2"]
                        ptype = ptype["name"]
            return render_template("results1match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
    else:
        # user_id of the top match
        user = final[1]
        # query into the database for the user's bio information
        match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
        # store the match's information
        name = match[0]["name"]
        phone = match[0]["phone"]
        email = match[0]["email"]
        height = match[0]["height"]
        age = match[0]["age"]
        # query for the match's type
        matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
        x = matchtype[0]["type"]
        # store the match's personality type and description
        for ptype in personalitytypes:
                if ptype["type"] == x:
                    # store the name and description of the personality type
                    description = ptype["description2"]
                    ptype = ptype["name"]
        if len(final) == 2:
            return render_template("twomatches1.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
        return render_template("results2match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)

@app.route("/results3match", methods=["GET", "POST"])
def results3match():
    if request.method == "POST":
        # user_id of the top match
        user = final[1]
        # query into the database for the user's bio information
        match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
        # store the match's information
        name = match[0]["name"]
        phone = match[0]["phone"]
        email = match[0]["email"]
        height = match[0]["height"]
        age = match[0]["age"]
        # query for the match's type
        matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
        x = matchtype[0]["type"]
        # store the match's personality type and description
        for ptype in personalitytypes:
                if ptype["type"] == x:
                    # store the name and description of the personality type
                    description = ptype["description2"]
                    ptype = ptype["name"]
        return render_template("results2match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)
    else:
        # user_id of the top match
        user = final[2]
        # query into the database for the user's bio information
        match = db.execute("SELECT * FROM bio WHERE user_id = :user", user=user)
        # store the match's information
        name = match[0]["name"]
        phone = match[0]["phone"]
        email = match[0]["email"]
        height = match[0]["height"]
        age = match[0]["age"]
        # query for the match's type
        matchtype = db.execute("SELECT * FROM personality WHERE user_id = :user", user=user)
        x = matchtype[0]["type"]
        # store the match's personality type and description
        for ptype in personalitytypes:
                if ptype["type"] == x:
                    # store the name and description of the personality type
                    description = ptype["description2"]
                    ptype = ptype["name"]
        return render_template("results3match.html", name=name, phone=phone, email=email, height=height, age=age, description=description)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    flash(e.name)
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)