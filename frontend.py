import streamlit as st
import praw_stuff

if __name__ == '__main__':
    with st.sidebar:
        st.subheader('App created by Brian Salkas')
        st.write('Got any ideas to improve this app?  Open an issue [here](%s)' % 'https://github.com/brianSalk/search-reddit/issues')
        st.write('If you are a programmer, send me a pull request [here](%s)' % 'https://github.com/brianSalk/search-reddit/pulls')
    st.title('Search Reddit')
    with st.form('form'):
        subreddits =    st.text_input('subreddits').split()
        search_string = st.text_input('word or phrase to search')

        is_case_sensitive = st.checkbox('make search case sensitive search')
        is_whole_word = st.checkbox('search as whole word', help="Check this box to avoid matching for parts of words.  For example, if you are searching 'ed' but do not want to show matches for 'helped' or 'education'")
        is_regex = st.checkbox('use python regex (programmers only)')
        include_comments = st.checkbox('search for word or phrase in submission comments', value=True)
        submitted = st.form_submit_button('Search reddit')

        if submitted:
            with st.spinner(f'finding occurances of {search_string} in {" ".join(subreddits)}...'):
                praw_stuff.search_in_subreddits(
                        search_string, 
                        subreddits, 
                        ignore_case = not is_case_sensitive, 
                        whole_word=is_whole_word, 
                        use_regex=is_regex, 
                        include_comments=include_comments 
                        )
