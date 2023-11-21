import math
from collections import defaultdict
from SVM import combo_df
import csv

interactions = []

tweet_text = {}

# Read ratings.csv. For each item in ratings, ratings have form: userid, movieid, rating, timestamp.

with open("data/fake_interactions.csv", "r") as file:
    k = 0
    for line in file:
        if (k == 0):
            pass
        else:
            li = line.strip().split(",")
            interactions.append(li)
        k = k + 1

with open("data/monkeypox.csv", "r") as file:
    k = 0
    for line in file:
        if (k == 0):
            pass
        else:
            li = line.strip().split(",")
            tweet_text[int(li[0])] = li[2]
        k = k + 1

def get_credibility_scores():
    credibility_dict = {}

    with open("data/credibility_scores.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Assuming the CSV has headers, skip the first row
        next(reader, None)

        for row in reader:
            user_id, credibility_score = row
            credibility_dict[int(user_id)] = float(credibility_score)

    return credibility_dict

#Create dictionary of users and the tweets they have interacted with.
#Users 

# interactions_dict = {}
# for interaction in interactions:
#     user = interaction[0]
#     tweet = interaction[1]
#     interaction_type = interaction[2]
#     if (user not in interactions_dict.keys()):
#         interactions_dict[user] = {}
#     else:
#         if (tweet not in in interactions_dict[user].keys()):
#             interactions_dict[user][tweet] = [0] * 3           
#     if (interaction_type == "like"):
#         interactions_dict[user][tweet][0] = 1
#     if (interaction_type == "comment"):
#         interactions_dict[user][tweet][1] = 1
#     if (interaction_type == "retweet"):
#         interactions_dict[user][tweet][2] = 1
interactions_dict = {}
userset = set()
for interaction in interactions:
    user = int(interaction[0])
    tweet = int(interaction[1])
    interaction_type = interaction[2]
    userset.add(user)
    if (user not in interactions_dict.keys()):
        interactions_dict[user] = {}
    if (tweet not in interactions_dict[user].keys()):
        interactions_dict[user][tweet] = 0           
    if (interaction_type == "like"):
        interactions_dict[user][tweet] = interactions_dict[user][tweet] + 10
    if (interaction_type == "comment"):
        interactions_dict[user][tweet] = interactions_dict[user][tweet] + 15
    if (interaction_type == "retweet"):
        interactions_dict[user][tweet] = interactions_dict[user][tweet] + 10


# userset = set()
# for rating in ratings:
#     if (int(rating[0]) in users):
#         users[int(rating[0])].append([int(rating[1]), int(rating[2])])
#     else:
#         users[int(rating[0])] = [[int(rating[1]), int(rating[2])]]
#     userset.add(int(rating[0]))


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
    for tweet in interactions_dict[user1].keys():
        combined[tweet].append(interactions_dict[user1][tweet])
    for tweet in interactions_dict[user2].keys():
        combined[tweet].append(interactions_dict[user2][tweet])
        if (len(combined[tweet]) > 1):
            combinedlist.append(combined[tweet])
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

def recommender(u, nrecs, k, misinfo_filter):
    interactions_copy = interactions_dict.copy()
    neighbors = knearestneighbor(u, userset, 3, k)
    movies = defaultdict(list)
    credibility_scores = get_credibility_scores()
    for tweet in interactions_copy[u].keys():
        movies[tweet] = ["PASS"]
    for neighbor in neighbors:
        credibility_score = credibility_scores.get(neighbor, 1.0)  # Default to 1.0 if credibility score is not available
        for tweet in interactions_copy[neighbor].keys():
            if tweet in movies.keys():
                if movies[tweet] != ["PASS"]:
                    movies[tweet][0] += credibility_score  # Adjust the interaction count
                    movies[tweet][1] += credibility_score * interactions_copy[neighbor][tweet]  # Adjust the interaction score
            else:
                movies[tweet] = [credibility_score, credibility_score * interactions_copy[neighbor][tweet]]
    smoothedprediction = []
    for tweet, data in movies.items():
        if data != ["PASS"]:
            credibility_adjusted_count = data[0]
            credibility_adjusted_score = data[1] / data[0]  # Adjusted average based on credibility
            prediction = (1 + (credibility_adjusted_count * credibility_adjusted_score)) / (1 + credibility_adjusted_count)
#         if (data != ["PASS"]):
#             average = data[1]/data[0]
#             prediction = (10 + (data[0]*average))/(1 + data[0])
            smoothedprediction.append([tweet_text[tweet], prediction])
    smoothedprediction.sort(key=lambda x: x[1], reverse=True)
    return smoothedprediction[0:nrecs]

def main():
    # print(ratingdistance(1, 100, 3))
    # print(ratingdistance(200, 300, 3))
    # print(ratingdistance(200, 500, 3))
    # print(knearestneighbor(2, (100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110), 3, 5))
    # print(recommender(1, 5, 30))
    recommendations = recommender(1, 10, 30, "yes")
    for line in recommendations:
        print(line)

if __name__ == "__main__":
    main()
