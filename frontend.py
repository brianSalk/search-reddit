import streamlit as st
import praw_stuff

if __name__ == '__main__':
    st.title('Search Reddit')
    subreddits = subreddits = st.text_input('subreddits').split()
    search_string = st.text_input('word or phrase to search')
    is_case_sensitive = st.checkbox('case sensitive search')
    is_whole_word = st.checkbox('search as whole word')
    is_regex = st.checkbox('use extended regex')
    include_comments = st.checkbox('include comments', value=True)


    if st.button('search subreddit'):
        praw_stuff.search_in_subreddits(search_string, subreddits, not is_case_sensitive, is_whole_word, is_regex, include_comments )
    # st.button('search subreddits', on_click=praw_stuff.search_in_subreddits, args=(search_string, subreddits, not is_case_sensitive, is_whole_word, is_regex, include_comments ))
