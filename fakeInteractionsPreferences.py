import pandas as pd
from faker import Faker
import random

# Assuming you have a real dataset named real_tweets_df
# You can replace this with your actual dataset
# real_tweets_df = pd.read_csv("your_real_dataset.csv")

# Set up Faker to generate fake data
fake = Faker()

# Function to generate a fake user with a specified misinformation preference
def generate_user(user_id, misinformation_preference):
    return {
        'user_id': user_id,
        'misinformation_preference': misinformation_preference,
    }

def generate_interactions(users, tweets, num_interactions, misinformation_preference):
    interactions = []

    # Cast the 'binary_class' column to int
    tweets['binary_class'] = tweets['binary_class'].astype(int)

    # Filter tweets based on misinformation_preference
    if misinformation_preference == 'misinformation':
        filtered_tweets = tweets[tweets['binary_class'] == 1]
    elif misinformation_preference == 'non-misinformation':
        filtered_tweets = tweets[tweets['binary_class'] == 0]
    else:
        filtered_tweets = tweets  # No specific preference, use all tweets

    # Print the first few rows of the DataFrame to check its structure
    print("Filtered Tweets DataFrame:")
    print(filtered_tweets.head())

    for _ in range(num_interactions):
        user_id = random.choice(users)['user_id']
        
        # Check if there are tweets with the specified condition
        if not filtered_tweets.empty:
            # Convert the 'number' column to a list for random.choice
            tweet_ids = filtered_tweets['number'].tolist()

            # Use random.choice on the list of tweet_ids
            tweet_id = random.choice(tweet_ids)

            interaction_type = random.choice(['like', 'retweet', 'comment'])
            interactions.append({'user_id': user_id, 'tweet_id': tweet_id, 'interaction_type': interaction_type})

    return pd.DataFrame(interactions)

def generate_fake_data(num_users, real_tweets_df, num_interactions_per_user):
    users = []
    interactions = []

    for user_id in range(1, num_users + 1):
        if user_id <= 25:
            misinformation_preference = 'misinformation'
        elif user_id <= 75:
            misinformation_preference = 'non-misinformation'
        else:
            misinformation_preference = random.choice(['misinformation', 'non-misinformation'])

        users.append(generate_user(user_id, misinformation_preference))
        
        user_interactions = generate_interactions(users[-1:], real_tweets_df, num_interactions_per_user, misinformation_preference)
        interactions.append(user_interactions)

    users_df = pd.DataFrame(users)
    interactions_df = pd.concat(interactions, ignore_index=True)

    return users_df, interactions_df

# Replace this with your actual real dataset
real_tweets_df = pd.read_csv("data/monkeypox-followup.csv")

# Generate a fake dataset with 100 users and 5 interactions per user
num_users = 100
num_interactions_per_user = 10

fake_users_df, fake_interactions_df = generate_fake_data(num_users, real_tweets_df, num_interactions_per_user)

# Display the generated dataframes
print("Fake Users DataFrame:")
print(fake_users_df.head())

print("\nFake Interactions DataFrame:")
print(fake_interactions_df.head())

fake_users_df.to_csv("data/preference_fake_users.csv", index=False)
fake_interactions_df.to_csv("data/preference_fake_interactions.csv", index=False)