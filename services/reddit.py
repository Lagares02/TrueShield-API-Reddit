import praw
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de PRAW
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('UG')
)

def search_reddit_posts(keywords):
    
    keywords = [keyword.lower() for keyword in keywords]

    results = []
    
    for submission in reddit.subreddit('all').search(" OR ".join(keywords), limit=100):
        title_text = (submission.title + " " + submission.selftext).lower()
        matches = sum(1 for keyword in keywords if keyword in title_text)
        
        if matches >= 1:
            ContextLevel = round(float(matches / len(keywords)), 2)
        else:
            ContextLevel = 0.0

        if matches >= 2:
            results.append({
                "Id": submission.id,
                "DatePub": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d'),
                "NameProfile": str(submission.author) if submission.author else "Unknown",
                "TitlePub": submission.title,
                "TextPub": submission.selftext,
                "CantUpVotes": submission.ups,
                "CantDownVotes": submission.downs,
                "CantComents": submission.num_comments,
                "CantShares": submission.num_crossposts,
                "TrueLevel": 0.60,
                "ContextLevel": ContextLevel,
                "Type_item": "reddit",
                "matches": matches
            })

    results = sorted(results, key=lambda x: x["matches"], reverse=True)
    
    return results