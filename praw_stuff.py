import praw
import os

print(os.getenv('CID'))
reddit = praw.Reddit(
        client_id = os.getenv('CID'),
        client_secret = os.getenv('SECRET'),
        user_agent = 'brianplusplus reddit scraper for a string of text',
        username = os.getenv('REDDIT_USER_NAME'),
        password = os.getenv('REDDIT_PASSWORD')
        )
def find_string_in_subreddit(string, subreddit_name, ignore_case=True, squeeze_spaces=True):
    
    # get each submission within the subreddit
    for submission in reddit.subreddit(subreddit_name).new(limit=None):
        comment_forest = submission.comments.replace_more(limit=100)
        print('s')

        title = submission.title
        selftext = submission.selftext
        if squeeze_spaces:
            title = title.replace('\n', ' ')
            title = ' '.join(title.split())
            selftext = selftext.replace('\n', ' ')
            selftext = ' '.join(selftext.split())
        if ignore_case:
            title = title.lower()
            selftext = selftext.lower()
            string = string.lower()
        if string in title:
            print('found string in title', submission.url)
        if string in submission.selftext:
            print('found string in self-text', submission.url)
        for comment in comment_forest:
            comment_body = comment.body
            if squeeze_spaces:
                comment_body = text.replace('\n', ' ')
                comment_body = ' '.join(text.split())
            if ignore_case:
                comment_body = comment_body.lower()
            if string in comment.body:
                print('found string in comment: ', comment.submission.url)

if __name__ == "__main__":
    subreddit = input('enter subreddit name:')
    string = input('enter search string:')
    find_string_in_subreddit(string, subreddit)
