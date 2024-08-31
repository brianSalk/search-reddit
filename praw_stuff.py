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
        found_in_post = False
        found_in_comments_count = 0
        url = submission.url 
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
        print('submission: ', title)
        if string in title or string in selftext:
            found_in_post = True
        comment_forest = None
        # SEARCH COMMENTS
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print('comment')
            comment_body = comment.body
            if squeeze_spaces:
                comment_body = comment_body.replace('\n', ' ')
                comment_body = ' '.join(comment_body.split())
            if ignore_case:
                comment_body = comment_body.lower()
            if string in comment_body:
                found_in_comments_count += 1
        if found_in_post:
            print(f' -------------------- Found {string} in {title}', url)
        if found_in_comments_count:
            print(f' -------------------- Found in {found_in_comments_count} comments', url)

if __name__ == "__main__":
    subreddit = input('enter subreddit name:')
    string = input('enter search string:')
    find_string_in_subreddit(string, subreddit)
