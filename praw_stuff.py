import re
import praw
import os
import streamlit as st

reddit = praw.Reddit(
        client_id = st.secrets['CID'],
        client_secret = st.secrets['SECRET'],
        user_agent = 'Myyyy reddit scraper for a string of text',
        username = st.secrets['REDDIT_USER_NAME'],
        password = st.secrets['REDDIT_PASSWORD']
        )

def get_bad_subreddits(subreddits):
    nonexistant = []
    for subreddit in subreddits:
        try:
            reddit.subreddit(subreddit).new(limit=None)
        except Exception as e:
            nonexistant.append(subreddit)
    return nonexistant


def squeeze_spaces(s):
    s = s.replace('\n', ' ')
    s = ' '.join(s.split())
    return s

def compile_word_re(s, ):
    return re.compile(fr'\b{s}\b')


def find_string_in_subreddit(string, subreddit_name, ignore_case=True, whole_word=False, use_regex=False, include_comments=True, limit=None, sort_by='new'):
    # get each submission within the subreddit
    try:
        if sort_by == 'new':
            submissions = reddit.subreddit(subreddit_name).new(limit=limit)
        elif sort_by == 'hot':
            submissions = reddit.subreddit(subreddit_name).hot(limit=limit)
        elif sort_by == 'controversial':
            submissions = reddit.subreddit(subreddit_name).controversial(limit=limit)
        for submission in submissions:
            found_in_post = False
            found_in_comments_count = 0
            url = submission.url 
            title = submission.title
            selftext = submission.selftext
            regex = ''
            if whole_word:
                regex = compile_word_re(string)
            elif use_regex:
                regex = re.compile(string)
            title = squeeze_spaces(title)
            selftext = squeeze_spaces(selftext)
            if ignore_case:
                title = title.lower()
                selftext = selftext.lower()
                string = string.lower()
            print('submission: ', title)
            # check if string is in title or submission selftext
            if whole_word:
                if regex.search(title) or regex.search(selftext):
                    found_in_post = True
            elif use_regex:
                if regex.search(title) or regex.search(selftext):
                    found_in_post = True
            else:
                if string in title or string in selftext:
                    found_in_post = True

            comment_forest = None
            # SEARCH COMMENTS
            if include_comments:
                submission.comments.replace_more(limit=None)
                print('comment searched')
                for comment in submission.comments.list():
                    print('comment')
                    comment_body = comment.body
                    comment_body = squeeze_spaces(comment_body)
                    if ignore_case:
                        comment_body = comment_body.lower()
                    if use_regex or whole_word:
                        if regex.search(comment_body):
                            found_in_comments_count += 1
                    else:
                        if string in comment_body:
                            found_in_comments_count += 1
            comment = ''
            if found_in_comments_count == 1:
                comment = f'found in {found_in_comments_count} comment'
            if found_in_comments_count > 1:
                comment = f'found in {found_in_comments_count} comments'

            if found_in_post or found_in_comments_count > 1:
                st.markdown(f'[{title}](%s) {comment}' % url)
    except Exception as e:
        st.write(':red[{subreddit_name} not found, check your spelling]')


def search_in_subreddits(string, subreddit_names, ignore_case=True, whole_word=False, use_regex=False, include_comments=True, limit=None, sort_by='new'):
    if not string or not subreddit_names:
        st.write(':red[search string and subreddits cannot be blank]')
        return
    st.spinner('scraping reddit')
    for subreddit_name in subreddit_names:
        st.markdown("<h2 style='color: blue;'>" + f"Searching for '{string}' in:" + "</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: blue;'>" + "r/" + subreddit_name + "</h3>", unsafe_allow_html=True)
        subreddit_name = subreddit_name.lower()
        try:
            find_string_in_subreddit(
                    string, 
                    subreddit_name, 
                    ignore_case=ignore_case, 
                    whole_word=whole_word, 
                    use_regex=use_regex, 
                    include_comments=include_comments,
                    limit=limit,
                    sort_by=sort_by
                    )    
        except Exception as e:
            st.write('red:[One or more subreddits not found]')




if __name__ == "__main__":
    subreddit = input('enter subreddit name:')
    string = input('enter search string:')
    find_string_in_subreddit(string, subreddit)
