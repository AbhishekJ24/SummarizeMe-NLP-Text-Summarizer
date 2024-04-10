from flask import Flask, request, render_template
from model import SummarizerModule

app = Flask(__name__)
summarizer_module = SummarizerModule()

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST','GET'])
def summarize():
    if request.method == 'POST':
        text = request.form['text']
        lines = int(request.form['lines'])
        summarized_text = summarizer_module.generate_summary(text, lines)
        return render_template('index.html', text=text, lines=lines, summarized_text=summarized_text)

if __name__ == '__main__':
    app.run(debug=True)