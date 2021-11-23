from flask import Flask, render_template, request, redirect

app = Flask(__name__)

import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(0, './model/')


from search_rank import process_query


# endpoint for search
@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.form['search_bar']
        data = process_query(query)
        return render_template('search.html', data=data)
    return render_template('search.html')


if __name__ == '__main__':
    #app.debug = False
    app.run(threaded=False)
