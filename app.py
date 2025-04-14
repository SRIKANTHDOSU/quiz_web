from flask import Flask, render_template, request, redirect, url_for,json
import sqlite3
from questions import generate_questions
app = Flask(__name__)
# Route to display all programming languages
@app.route("/")
def home():
    conn = sqlite3.connect("language.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT language FROM programming_concepts")
    rows = cur.fetchall()
    conn.close()
    languages = [row[0] for row in rows]
    return render_template("names.html", languages=languages)

# Route to display all concepts for a selected language
@app.route("/concepts")
def show_concepts():
    language = request.args.get("language")
    conn = sqlite3.connect("language.db")
    cur = conn.cursor()
    cur.execute("SELECT concepts FROM programming_concepts WHERE language=?", (language,))
    rows = cur.fetchall()
    conn.close()
    concepts = [row[0] for row in rows]
    return render_template("concepts.html", language=language, concepts=concepts)

# Route to display quiz questions for a selected concept
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    language = request.args.get("language")
    concept = request.args.get("concept")
    questions = generate_questions(language, concept, difficulty="beginner", num_questions=10)
    
    
    return render_template("quiz.html", topic=language, concept=concept, questions=questions)

@app.route('/explanation')
def explanation():
    score = request.args.get('score')
    total = request.args.get('total')
    data = json.loads(request.args.get('data'))
    return render_template('explanation.html', score=score, total=total, data=data)

if __name__ == "__main__":
    app.run(debug=True)




   

