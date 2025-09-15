from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import joblib

# --------------------
# Initialize Flask app
# --------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --------------------
# Database Tables
# --------------------
class SpamKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)

class EmailRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_text = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.String(20), nullable=True)

# --------------------
# Load ML models
# --------------------
model_data = joblib.load("sentence_bert_spam_model.joblib")
clf = model_data["clf"]
scaler = model_data["scaler"]
embedding_model = model_data["embedding_model"]

nb_model_data = joblib.load("tfidf_nb_spam_model.joblib")
tfidf_vectorizer = nb_model_data["vectorizer"]
nb_clf = nb_model_data["nb_clf"]

# --------------------
# Ensure DB exists
# --------------------
with app.app_context():
    db.create_all()

# --------------------
# Home page - GET & POST
# --------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    conf_pct = None
    email_text = ""
    if request.method == "POST":
        email_text = request.form.get("email_text", "")

        # Sentence Transformer + Logistic Regression prediction
        try:
            emb = embedding_model.encode([email_text])
            emb_scaled = scaler.transform(emb)
            pred_label = int(clf.predict(emb_scaled)[0])
            prob = clf.predict_proba(emb_scaled)[0][1]
            result = "🚨 Spam detected! (BERT LR)" if pred_label == 1 else "✅ Not Spam (BERT LR)"
            conf_pct = f"{prob*100:.1f}%"
        except Exception as e:
            result = f"⚠️ ML Error: {str(e)}"

        # TF-IDF + Naive Bayes prediction (fallback/alternative)
        try:
            email_tfidf = tfidf_vectorizer.transform([email_text])
            nb_pred_label = nb_clf.predict(email_tfidf)[0]
            nb_prob = nb_clf.predict_proba(email_tfidf)[0][1]
            if nb_pred_label == 1:
                result = "🚨 Spam detected! (Naive Bayes)"
                conf_pct = f"{nb_prob*100:.1f}%"
        except Exception as e:
            print("Naive Bayes prediction error:", e)

        # Keyword-based check (fallback)
        try:
            keywords = SpamKeyword.query.all()
            keyword_list = [k.word.lower() for k in keywords]
            if any(word in email_text.lower() for word in keyword_list):
                result = "🚨 Spam detected! (Keyword match)"
        except Exception:
            pass

        # Save to DB
        try:
            record = EmailRecord(email_text=email_text, result=result, confidence=conf_pct)
            db.session.add(record)
            db.session.commit()
        except Exception as e:
            print("DB save error:", e)

    return render_template("index.html", result=result, confidence=conf_pct, email_text=email_text)

# --------------------
# View history
# --------------------
@app.route("/history")
def history():
    records = EmailRecord.query.all()
    return render_template("history.html", records=records)

# --------------------
# Run app
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
