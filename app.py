from flask import Flask, render_template, redirect, url_for, request
from sklearn import datasets
from KnnBasic import KnnBasic 
import os

# refrence to this file
app = Flask(__name__)

# @app.route('/<db>,<name>')
# def knn(db, name):
#    datasets=db.split('-')
#    names=name.split('-')
#    # Knn=KnnBasic(datasets[0], datasets[1], names[0],names[1],names[2],names[3],names[4])
#    Knn=KnnBasic("ratings1.csv", "movies1.csv", 'userId', 'rating', 'movieId', 'movieId', 'title')
#    return Knn.FindObjects()
  
@app.route('/',methods = ['POST', 'GET'])
def Train():
   favoriteMovies=[]
   if request.method=='POST':
      datasetAdresses=request.form['datasets']
      rowNames=request.form['rowNames']
      favoriteObject=request.form['favoriteObject']

      try:
         datasets=datasetAdresses.split('-')
         names=rowNames.split('-')
         Knn=KnnBasic(datasets[0], datasets[1], names[0],names[1],names[2],names[3],names[4])
         favoriteMovies=Knn.FindObjects(favoriteObject)
         movies="other things you may like: "
         for movie in favoriteMovies:
            movies+=movie+" / "
         return movies
      except:
         return 'there was an issue finding reccomended movies'

   else:
      return render_template('./main.html', favoriteMovies=favoriteMovies)


   # if request.method == 'POST':
   #    database = request.form['nm']
   #    names= request.form['rn']
   #    return redirect(url_for('knn',db = database,name=names))
   # else:
   #    database = request.form['nm']
   #    names= request.form['rn']
   #    return redirect(url_for('knn',db = database,name=names))