from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("MCQ_CLEANED.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    grades = sorted(df['Grade'].dropna().unique())
    subjects = sorted(df['Subject'].dropna().unique())
    return render_template("index.html", grades=grades, subjects=subjects)

@app.route("/quiz", methods=["POST"])
def quiz():
    grade = int(request.form["grade"])
    subject = request.form["subject"]
    num_questions = int(request.form["num_questions"])
    filtered = df[(df['Grade'] == grade) & (df['Subject'] == subject)]
    selected = filtered.sample(n=min(num_questions, len(filtered))).to_dict(orient="records")
    return render_template("quiz.html", questions=selected)

@app.route("/result", methods=["POST"])
def result():
    total = int(request.form["total"])
    correct = 0
    for i in range(total):
        user_ans = request.form.get(f"user_ans_{i}")
        correct_ans = request.form.get(f"correct_ans_{i}")
        print(f"user_ans_{i}: {user_ans}")
        print(f"correct_ans_{i}: {correct_ans}")
        if user_ans and correct_ans:
            if user_ans.strip().lower() == correct_ans.strip().lower():
                correct += 1
        print(user_ans)
        print(correct_ans)
    percentage = round((correct / total) * 100, 2)
    return render_template("result.html", total=total, correct=correct, percentage=percentage)

if __name__ == "__main__":
    print("App running on http://127.0.0.1:5000/")
    app.run(debug=True)
