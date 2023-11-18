import pandas as pd
from faker import Faker
import random

# Assuming you have a real dataset named real_tweets_df
# You can replace this with your actual dataset
# real_tweets_df = pd.read_csv("your_real_dataset.csv")

# Set up Faker to generate fake data
fake = Faker()

# Function to generate a fake user
def generate_user(user_id):
    return {
        'user_id': user_id,
    }

# Function to generate fake interactions (likes)
def generate_interactions(users, tweets, num_interactions):
    interactions = []

    for _ in range(num_interactions):
        user_id = random.choice(users['user_id'])
        tweet_id = random.choice(tweets['number'])
        interactions.append({'user_id': user_id, 'tweet_id': tweet_id})

    return pd.DataFrame(interactions)

# Function to generate a fake dataset with fake users and real tweets
def generate_fake_data(users, real_tweets_df, num_interactions):
    tweets = real_tweets_df.copy()
    users_df = pd.DataFrame([generate_user(user_id) for user_id in range(1, users + 1)])
    interactions_df = generate_interactions(users_df, tweets, num_interactions)

    return users_df, tweets, interactions_df

# Replace this with your actual real dataset
real_tweets_df = pd.read_csv("data/monkeypox.csv")

# Generate a fake dataset with 100 fake users and 25000 interactions
num_fake_users = 100
num_interactions = 25000

fake_users_df, real_tweets_df, fake_interactions_df = generate_fake_data(num_fake_users, real_tweets_df, num_interactions)

# Display the generated dataframes
print("Fake Users DataFrame:")
print(fake_users_df.head())

print("\nReal Tweets DataFrame:")
print(real_tweets_df.head())

print("\nFake Interactions DataFrame:")
print(fake_interactions_df.head())

fake_interactions_df.to_csv("data/fake_interactions.csv", index=False)