from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    text_area_content = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        current_text = request.form.get('text_area')
        text_area_content = current_text + "\n" + user_input if current_text else user_input

    return render_template_string('''
    <html>
    <body>
        <form method="post">
            User Input: <input type="text" name="user_input"><br>
            <textarea name="text_area" rows="10" cols="50">{{ text_area_content }}</textarea><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    ''', text_area_content=text_area_content)

if __name__ == '__main__':
    app.run(debug=True)
