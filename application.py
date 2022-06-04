#Package import
from flask import Flask, render_template, make_response, url_for, Response, redirect, request
import pandas as pd
from tabulate import tabulate
from googlesearch import search
import newspaper
from newspaper import Article
import nltk

#initialise app
application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html',PageTitle = "Landing page")
#These functions will run when POST method is used.
@application.route('/', methods = ["POST"] )
def checkit():
    #gathering file from form
    uploaded_file = request.form['txt_file']
    #making sure its not empty
    if uploaded_file != '':
        text = str(uploaded_file)
        #You can then run any scripts you want on our file.
        #Here we used a text file so any sort of text analysis could be undertaken
        #You could even run machine learning on a csv dataset.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'left')
        Food = text
        df = pd.read_csv("Oxalate_list.csv")
        df = df[df['Food Item'].str.contains(Food)]
        if df.empty:
            return (Food+' not found in Oxalate list')
        else:
            purine_result =str('Purines in '+Food)
            for result in search(purine_result):
                first_article = Article(url=result)
                first_article.download()
                first_article.parse()
                first_article.nlp()
                a = str('<br/>'+df.to_html(header="true",table_id="table",index=False))
                b = str(('<br/>Description taken from '+result+'<br/>'))
                c = str((first_article.title+'<br/>'))
                d = str((first_article.summary))
                return (a+'<br/>'+b+'<br/>'+c+'<br/>'+d)
    else:
        return render_template('index.html',PageTitle = "Landing page")
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(response)))])
          #This just reloads the page if no file is selected and the user tries to POST.

if __name__ == '__main__':
    application.debug = True
    application.run()
