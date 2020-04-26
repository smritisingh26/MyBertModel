import praw
import pandas as pd
#Creating an instance of Reddit for authentication
reddit = praw.Reddit(client_id='kOGeR-5c1FXO5w', client_secret='q49RjW9bDPTMb5-vr8aCTDDbhxU', user_agent='RScrape')
subreddit = reddit.subreddit('india')
#Making a list of all flairs to be scraped
flairs=["Coronavirus","Politics","Non-Political","AskIndia","Business/Finance","Policy/Economy","Photography","CAA-NRC-NPR","Science/Technology","[R]eddiquette","Entertainment","Sports"]
#Making a dictionary of parameters of each post
topics={"flair":[], "title":[], "score":[], "id":[], "url":[], "comms_num": [], "created": [], "body":[], "author":[], "comments":[]}
#Scraping data in a neat format:
for flair in flairs:
  print("working on"+flair)
  try:
      get_subreddits = subreddit.search(flair, limit=200)
  except:
      print("An error occured in"+flair)
  for submission in get_subreddits:

    topics["flair"].append(flair)
    topics["title"].append(submission.title)
    topics["score"].append(submission.score)
    topics["id"].append(submission.id)
    topics["url"].append(submission.url)
    topics["comms_num"].append(submission.num_comments)
    topics["created"].append(submission.created)
    topics["body"].append(submission.selftext)
    topics["author"].append(submission.author)

    submission.comments.replace_more(limit=None)
    comment=''
    for top_level_comment in submission.comments:
      comment=comment + ' ' + top_level_comment.body
    topics["comments"].append(comment)

df=pd.DataFrame(topics)
df.to_csv('rIndia2.csv', index=False)
