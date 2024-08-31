import streamlit as st
import praw_stuff

if __name__ == '__main__':
    st.title('Search Reddit')
    subreddits = st.text_input('subreddits').split()
    st.text_input('word or phrase to search')
    is_case_sensitive = st.checkbox('case sensitive search')
    is_whole_word = st.checkbox('search as whole word')
    is_regex = st.checkbox('use extended regex')
    st.button('search subreddits', on_click=praw_stuff.find_string_in_subreddit, args=(search_string, subreddits[0], not is_case_sensitive, is_ ))
