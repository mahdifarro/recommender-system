# code
from ctypes.wintypes import PINT
import numpy as np
import pandas as pd
# Now, we create user-item matrix using scipy csr matrix
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

class KnnBasic:
    ratings, objects=pd.DataFrame(list()), pd.DataFrame(list())

    userIdColName_ratings, ratingsColName_ratings, objectsIdColName_ratings = '', '', ''
    objectIdColName, objectTitleColName = '', ''
    def __init__(self, ratingDB, firstDB,
        userIdColName_ratings, ratingsColName_ratings, objectsIdColName_ratings,
        objectIdColName, objectTitleColName):
        self.objects = pd.read_csv(firstDB)  
        self.ratings = pd.read_csv(ratingDB)
        self.userIdColName_ratings,  self.ratingsColName_ratings, self.objectsIdColName_ratings = userIdColName_ratings, ratingsColName_ratings, objectsIdColName_ratings
        self.objectIdColName,  self.objectTitleColName = objectIdColName, objectTitleColName

        self.InitFunctions()
    
    def InitFunctions(self):
        
        ## the above objects has very low dataset. We will use bayesian average
        self.movie_stats = self.ratings.groupby(self.objectsIdColName_ratings)[[self.ratingsColName_ratings]].agg(['count', 'mean'])
        self.movie_stats.columns = self.movie_stats.columns.droplevel()

    def Create_matrix(self, ratings):
        N = len(ratings[self.userIdColName_ratings].unique())
        M = len(ratings[self.objectsIdColName_ratings].unique())
        
        # Map Ids to indices
        user_mapper = dict(zip(np.unique(ratings[self.userIdColName_ratings]), list(range(N))))
        movie_mapper = dict(zip(np.unique(ratings[self.objectsIdColName_ratings]), list(range(M))))
        
        # Map indices to IDs
        user_inv_mapper = dict(zip(list(range(N)), np.unique(ratings[self.userIdColName_ratings])))
        movie_inv_mapper = dict(zip(list(range(M)), np.unique(ratings[self.objectsIdColName_ratings])))
        
        user_index = [user_mapper[i] for i in ratings[self.userIdColName_ratings]]
        movie_index = [movie_mapper[i] for i in ratings[self.objectsIdColName_ratings]]
    
        X = csr_matrix((ratings[self.ratingsColName_ratings], (movie_index, user_index)), shape=(M, N))
        
        return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

    """
    Find similar objects using KNN
    """
    def Find_similar_Objects(self, movie_id, X, k, movie_mapper, movie_inv_mapper, metric='cosine', show_distance=False):
        

        neighbour_ids = []
        
        movie_ind = movie_mapper[movie_id]
        movie_vec = X[movie_ind]
        k+=1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        movie_vec = movie_vec.reshape(1,-1)
        neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
        for i in range(0,k):
            n = neighbour.item(i)
            neighbour_ids.append(movie_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

    def FindObjects(self, movie_title, k=10):
        movie_titles = dict(zip(self.objects[self.objectIdColName], self.objects[self.objectTitleColName]))
        movie_ids=dict(zip(self.objects[self.objectTitleColName], self.objects[self.objectIdColName]))

        movie_id=movie_ids[movie_title]

        X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = self.Create_matrix(self.ratings)
        similar_ids = self.Find_similar_Objects(movie_id, X, k, movie_mapper, movie_inv_mapper)

        favoriteMoviesList=[]

        # print(f"Since you watched {movie_title}")
        for i in similar_ids:
            favoriteMoviesList.append(movie_titles[i])
            # print(movie_titles[i])
        return favoriteMoviesList