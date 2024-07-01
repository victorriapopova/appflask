from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Models
class Message:
    global_count = 0

    def __init__(self, username, text):
        self.username = username
        self.text = text
        self.id = Message.global_count
        Message.global_count += 1

    def to_dict(self):
        return {
            "username": self.username,
            "text": self.text,
            "id": self.id
        }

    def __repr__(self):
        return str(self.to_dict())


# Initial message for the auto service
messages = [
    Message("Auto Service", "Welcome to our auto service! How can we assist you today?")
]


# Routes
@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        username = request.form.get("username", "Customer")
        text = request.form["text"]
        messages.append(Message(username, text))
        return "Feedback accepted!"

    return render_template("feedback.html")


@app.route("/request_messages", methods=["POST"])
def request_messages():
    last_received_message_id = request.json.get('last_received_message_id', -1)
    new_messages = [m.to_dict() for m in messages if m.id > last_received_message_id]
    return jsonify(new_messages)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
