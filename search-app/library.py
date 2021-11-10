# library.py
from flask import Flask, render_template, request, redirect

from search_rank import process_query

app = Flask(__name__)

#endpoint for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.form['search_bar']
        data = process_query(query)
        #data = [("Nomadland", "https://www.rottentomatoes.com/m/nomadland"), ("Judas and the Black Messiah", "https://www.rottentomatoes.com/m/judas_and_the_black_messiah")]
        return render_template('search.html', data=data)
    return render_template('search.html')

if __name__ == '__main__':
    # app.debug = True
    app.run()