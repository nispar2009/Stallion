import pyodbc

conn = pyodbc.connect("Driver={SQL Server}; Server=NISANTH_PC\\SQLEXPRESS; Database=stallion; Trusted_Connection=yes;")
cursor = conn.cursor()

quotes = [
    "\"I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'\" - Muhammad Ali",
    "\"The real workout starts when you want to stop.\" - Ronnie Coleman",
    "\"Take care of your body. It's the only place you have to live.\" - Jim Rohn",
    "\"You must expect things of yourself before you can do them.\" - Michael Jordan",
    "\"If something stands between you and your success, move it. Never be denied.\" - Dwayne \"The Rock\" Johnson",
    "\"Great things come from hard work and perseverance. No excuses.\" - Kobe Bryant",
    "\"Time, Effort, Sacrifice, and Sweat. How will you pay for your goals?\" - Usain Bolt",
    "\"Don't stop chasing your dreams, because dreams do come true.\" - Sachin Tendulkar",
    "\"Just believe in yourself. Even if you don't, just pretend that you do and at some point, you will.\" - Venus Williams",
    "\"Face the failure, until the failure fails to face you.\" - MS Dhoni",
    "\"The last three or four reps is what makes the muscle grow. This area of pain divides a champion from someone who is not a champion.\" - Arnold Schwarzenegger"
]

class Post:
    def __init__(self, _id, author, title, content, topic, likes):
        self.id = _id
        self.author = author
        self.title = title
        self.content = content
        self.topic = topic
        self.likes = likes

class Food:
    def __init__(self, item, cal, protein, carbs, fats, na):
        self.item = item
        self.cal = cal
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.na = na

class Rating:
    def __init__(self, author, comment, stars):
        self.author = author
        self.comment = comment
        self.stars = stars

class Report:
    def __init__(self, _id, item, cal, protein, carbs, fats, na, email):
        self.id = _id
        self.item = item
        self.cal = cal
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.na = na
        self.email = email

def feed():
    query = "SELECT * FROM blog WHERE topic = 'Muscle building' ORDER BY likes DESC"
    db_output = cursor.execute(query)
    muscle_feed = []

    for item in list(db_output):
        muscle_feed.append(Post(item[0], item[1], item[2], item[3], item[4], item[5]))

    query = "SELECT * FROM blog WHERE topic = 'Weight loss' ORDER BY likes DESC"
    db_output = cursor.execute(query)
    weight_feed = []

    for item in list(db_output):
        weight_feed.append(Post(item[0], item[1], item[2], item[3], item[4], item[5]))

    query = "SELECT * FROM blog WHERE topic = 'Overall health' ORDER BY likes DESC"
    db_output = cursor.execute(query)
    overall_feed = []

    for item in list(db_output):
        overall_feed.append(Post(item[0], item[1], item[2], item[3], item[4], item[5]))

    query = "SELECT * FROM blog WHERE topic = 'Recipe' ORDER BY likes DESC"
    db_output = cursor.execute(query)
    recipe_feed = []

    for item in list(db_output):
        recipe_feed.append(Post(item[0], item[1], item[2], item[3], item[4], item[5]))

    return [muscle_feed, weight_feed, overall_feed, recipe_feed]

def fetch(_id):
    query = "SELECT * FROM blog WHERE id=?"
    post = list(cursor.execute(query, (_id,)))

    if len(post) == 0:
        return 404

    post = post[0]
    content = post[3]
    content = content.replace("\n", "<br>")
    content = content.replace("\"", "&quot;")
    content = content.replace("[[", "<em>")
    content = content.replace("]]", "</em>")

    post_class = Post(post[0], post[1], post[2], content, post[4], post[5])
    return post_class

def add_post(author, title, content, topic):
    query = "INSERT INTO blog (author, title, content, topic, likes) VALUES (?, ?, ?, ?, 0)"
    cursor.execute(query, (author, title, content, topic))
    conn.commit()

def add_food(item, energy, protein, carbs, fats, na):
    query = "INSERT INTO food (item, cal, protein, carbs, fats, na) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (item, energy, protein, carbs, fats, na))
    conn.commit()

def add_like(_id):
    query = "UPDATE blog SET likes=likes+1 WHERE id=?"
    cursor.execute(query, (_id,))
    conn.commit()

def food():
    query = "SELECT * FROM food ORDER BY protein/cal DESC"
    db_food = list(cursor.execute(query))
    overall_food = []
    for item in db_food:
        overall_food.append(Food(item[0], item[1], item[2], item[3], item[4], item[5]))

    query = "SELECT * FROM food ORDER BY protein DESC"
    db_food = list(cursor.execute(query))
    muscle_food = []
    for item in db_food:
        muscle_food.append(Food(item[0], item[1], item[2], item[3], item[4], item[5]))

    query = "SELECT * FROM food ORDER BY fats ASC"
    db_food = list(cursor.execute(query))
    weight_food = []
    for item in db_food:
        weight_food.append(Food(item[0], item[1], item[2], item[3], item[4], item[5]))

    return [overall_food, weight_food, muscle_food]

def show_ratings():
    query = "SELECT * FROM ratings ORDER BY stars DESC"
    ratings = list(cursor.execute(query))
    good_ratings = []
    for item in ratings:
        good_ratings.append(Rating(item[0], item[1], item[2]))

    return good_ratings

def add_rating(author, comment, stars):
    query = "INSERT INTO ratings (author, comment, stars) VALUES (?, ?, ?)"
    cursor.execute(query, (author, comment, stars))
    conn.commit()

def add_report(item, email):
    query = "INSERT INTO reported (item, email) VALUES (?, ?)"
    cursor.execute(query, (item, email))
    conn.commit()

def show_reports():
    query = "SELECT * FROM reported"
    db_reports = list(cursor.execute(query))
    good_reports = []

    for item in db_reports:
        food_query = "SELECT * FROM food WHERE item = ?"
        food_item = list(cursor.execute(food_query, (item[1],)))[0]

        good_reports.append(Report(item[0], item[1], food_item[1], food_item[2], food_item[3], food_item[4], food_item[5], item[2]))

    return good_reports

def delete(_id):
    query = "DELETE reported WHERE id = ?"
    cursor.execute(query, (_id,))
    conn.commit()

def act(_id):
    query = "SELECT item FROM reported WHERE id = ?"
    item = list(cursor.execute(query, (_id,)))[0][0]

    query = "DELETE food WHERE item = ?"
    cursor.execute(query, (item,))
    conn.commit()

    delete(_id)