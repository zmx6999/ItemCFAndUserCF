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
    n = {}
    w = {}
    for user,movies in train.items():
        for x in movies:
            n[x] = n.get(x,0)+1
            for y in movies:
                if x != y:
                    if x not in w: w[x] = {}
                    w[x][y] = w[x].get(y,0)+1
    total = len(n)

    for x,related_movies in w.items():
        for y,wxy in related_movies.items():
            w[x][y] = float(wxy)/math.sqrt(n[x]*n[y])
    return w,total


def recommend(user,train,w,k=20,j=10):
    recommend_movies = {}
    watched_movies = train[user]
    for x,star in watched_movies.items():
        for y,wxy in sorted(w[x].items(),key=operator.itemgetter(1),reverse=True)[:k]:
            if y not in watched_movies: recommend_movies[y] = recommend_movies.get(y,0)+wxy*float(star)
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
    print(evaluate(train,test,w,total)) #0.33775185577942735, 0.12710004389640447, 0.12021857923497267