import random
import math
import operator


def loadfile():
    data = {}
    lines = open('u.data').readlines()
    for line in lines:
        user,movie,star,addtime = line.strip().split('\t')
        if user not in data: data[user] = {}
        data[user][movie] = star
    return data


def get_data(data,m=.75):
    train = {}
    test = {}
    for user,movies in data.items():
        for movie,star in movies.items():
            if random.random() < m:
                if user not in train: train[user] = {}
                train[user][movie] = star
            else:
                if user not in test: test[user] = {}
                test[user][movie] = star
    return train,test


def get_w(train):
    movie_user = {}
    for user,movies in train.items():
        for movie in movies:
            if movie not in movie_user: movie_user[movie] = set()
            movie_user[movie].add(user)
    total = len(movie_user)

    w = {}
    for movie,users in movie_user.items():
        for x in users:
            for y in users:
                if x != y:
                    if x not in w: w[x] = {}
                    w[x][y] = w[x].get(y,0)+1

    for x,related_users in w.items():
        for y,wxy in related_users.items():
            w[x][y] = float(wxy)/math.sqrt(len(train[x])*len(train[y]))
    return w,total


def recommend(user,train,w,k=20,j=10):
    recommend_movies = {}
    watched_movies = train[user]
    for related_user,wxy in sorted(w[user].items(),key=operator.itemgetter(1),reverse=True)[:k]:
        for movie,star in train[related_user].items():
            if movie not in watched_movies: recommend_movies[movie] = recommend_movies.get(movie,0)+wxy*float(star)
    return sorted(recommend_movies.items(),key=operator.itemgetter(1),reverse=True)[:j]


def evaluate(train,test,w,total,k=20,j=10):
    hit = 0
    total_recall = 0
    total_precision = 0
    all_recommend_movies = set()
    for user in train:
        recommend_movies = recommend(user,train,w,k,j)
        test_movies = test.get(user,{})
        for movie,_ in recommend_movies:
            if movie in test_movies: hit += 1
            all_recommend_movies.add(movie)
        total_recall += len(test_movies)
        total_precision += len(recommend_movies)
    precision = float(hit)/total_precision
    recall = float(hit)/total_recall
    coverage = float(len(all_recommend_movies))/total
    return precision,recall,coverage


if __name__ == '__main__':
    data = loadfile()
    train,test = get_data(data)
    w,total = get_w(train)
    print(evaluate(train,test,w,total)) #0.35980911983032876, 0.13573628835460255, 0.2087912087912088