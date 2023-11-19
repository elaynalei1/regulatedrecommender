import math

interactions = []

# Read ratings.csv. For each item in ratings, ratings have form: userid, movieid, rating, timestamp.

with open("data/fake_interactions.csv", "r") as file:
    for line in file:
        li = line.strip().split(",")
        interactions.append(li)

#Create dictionary of users and the tweets they have interacted with.
#Users 

interactions_dict = {}
for interaction in interactions:
    user = interaction[0]
    tweet = interaction[1]
    interaction_type = interaction[2]
    if (user not in interactions_dict.keys()):
        interactions_dict[user] = {}
    else:
        if (tweet not in in interactions_dict[user].keys()):
            interactions_dict[user][tweet] = [0] * 3           
    if (interaction_type == "like"):
        interactions_dict[user][tweet][0] = 1
    if (interaction_type == "comment"):
        interactions_dict[user][tweet][1] = 1
    if (interaction_type == "retweet"):
        interactions_dict[user][tweet][2] = 1


userset = set()
for rating in ratings:
    if (int(rating[0]) in users):
        users[int(rating[0])].append([int(rating[1]), int(rating[2])])
    else:
        users[int(rating[0])] = [[int(rating[1]), int(rating[2])]]
    userset.add(int(rating[0]))


def angulardistance(combinedlist):
    a = 0
    b = 0
    c = 0
    for i in combinedlist:
        x = i[0]
        y = i[1]
        a += x * y
        b += x * x
        c += y * y
    return 1 - a/((math.sqrt(b)*math.sqrt(c)))

def ratingdistance(user1, user2, threshold):
    combined = defaultdict(list)
    combinedlist = []

    for movie1 in users[user1]:
        combined[movie1[0]].append(movie1[1])

    for movie2 in users[user2]:
        combined[movie2[0]].append(movie2[1])
        if (len(combined[movie2[0]]) > 1):
            combinedlist.append(combined[movie2[0]])

    if (len(combinedlist) > threshold - 1):
        return angulardistance(combinedlist)
    else:
        return 1.0

def knearestneighbor(u, S, threshold, k):
    if (k > len(S)):
        return S
    neighbors = []
    for user in S:
        if (user != u):
            distance = ratingdistance(u, user, threshold)
            neighbors.append((user, distance))
    neighbors.sort(key=lambda x: x[1])
    ret = []
    for i in range(k):
        ret.append(neighbors[i][0])
    return(ret)

def recommender(u, nrecs, k):
    users2 = users.copy()
    neighbors = knearestneighbor(u, userset, 3, k)
    movies = defaultdict(list)
    for movierating in users2[u]:
        movies[movierating[0]] = ["PASS"]
    for neighbor in neighbors:
        for movierating in users2[neighbor]:
            if (movierating[0] in movies):
                if (movies[movierating[0]] != ["PASS"]):
                    movies[movierating[0]][0] += 1
                    movies[movierating[0]][1] = (movies[movierating[0]][1] + movierating[1])
            else:
                movies[movierating[0]] = [1, movierating[1]]
    smoothedprediction = []
    for movie, data in movies.items():
        if (data != ["PASS"]):
            average = data[1]/data[0]
            prediction = (3.5 + (data[0]*average))/(1 + data[0])
            smoothedprediction.append([movie, prediction])
    smoothedprediction.sort(key=lambda x: x[1], reverse=True)
    return smoothedprediction[0:nrecs]

def main():
    # print(ratingdistance(1, 100, 3))
    # print(ratingdistance(200, 300, 3))
    # print(ratingdistance(200, 500, 3))
    # print(knearestneighbor(2, (100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110), 3, 5))
    # print(recommender(1, 5, 30))
    print(recommender(0, 5, 30))

if __name__ == "__main__":
    main()
