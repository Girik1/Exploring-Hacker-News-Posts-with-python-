import requests
from datetime import datetime
import matplotlib.pyplot as plt

# Base URL for Hacker News API
BASE_URL = "https://hacker-news.firebaseio.com/v0/"

# Fetch top story IDs
def get_top_story_ids():
    url = BASE_URL + "topstories.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Fetch details of a post by its ID
def get_story_details(story_id):
    url = BASE_URL + f"item/{story_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

# Convert UNIX timestamp to a readable date
def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Fetch comments for a post
def get_comments(post_id):
    post_details = get_story_details(post_id)
    comments = []

    if "kids" in post_details:  # 'kids' contains comment IDs
        for comment_id in post_details["kids"]:
            comment_details = get_story_details(comment_id)
            if comment_details:
                comments.append({
                    "author": comment_details.get("by"),
                    "text": comment_details.get("text"),
                    "time": comment_details.get("time"),
                })
    return comments

# Fetch top posts
def get_top_posts(limit=5):
    top_story_ids = get_top_story_ids()
    top_posts = []

    for story_id in top_story_ids[:limit]:
        story_details = get_story_details(story_id)
        if story_details:
            top_posts.append({
                "title": story_details.get("title"),
                "url": story_details.get("url"),
                "score": story_details.get("score"),
                "by": story_details.get("by"),
                "time": story_details.get("time"),
                "id": story_details.get("id"),
            })

    return top_posts

# Visualize the distribution of post scores
def plot_score_distribution(posts):
    scores = [post['score'] for post in posts]
    
    plt.hist(scores, bins=20, color='blue', edgecolor='black')
    plt.title('Distribution of Post Scores')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()

# Main function to explore Hacker News data
def explore_hacker_news(limit=5):
    print(f"Fetching the top {limit} stories...\n")
    top_posts = get_top_posts(limit)
    
    # Print top posts with details
    for idx, post in enumerate(top_posts, 1):
        print(f"{idx}. {post['title']}")
        print(f"   URL: {post['url']}")
        print(f"   Score: {post['score']} | Author: {post['by']}")
        print(f"   Time: {convert_timestamp(post['time'])}")
        
        # Fetch and display comments for each post
        comments = get_comments(post['id'])
        if comments:
            print("   Comments:")
            for comment in comments[:3]:  # Limit to top 3 comments
                print(f"      - Author: {comment['author']}")
                print(f"        {comment['text'][:100]}...")  # Display first 100 characters
                print(f"        Time: {convert_timestamp(comment['time'])}")
                print("-" * 60)
        else:
            print("   No comments found.")
        
        print("-" * 60)
    
    # Plot score distribution
    plot_score_distribution(top_posts)

if __name__ == "__main__":
    explore_hacker_news(limit=5)
