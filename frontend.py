import streamlit as st
import praw_stuff

def clean_subreddits(subreddits):
    cleaned = []
    for sub in subreddits:
        if ',' in sub:
            sub = sub.replace(',', '')
            sub = sub.strip()
        if sub.startswith('r/') or sub.startswith('R/'):
            sub = sub[2:]
        if len(sub) > 0:
            cleaned.append(sub.lower())
    return cleaned



if __name__ == '__main__':
    with st.sidebar:
        st.subheader('App created by Brian Salkas')
        st.write('Got any ideas to improve this app?  Open an issue [here](%s)' % 'https://github.com/brianSalk/search-reddit/issues')
        st.write('If you are a programmer, send me a pull request [here](%s)' % 'https://github.com/brianSalk/search-reddit/pulls')
    st.title('Search Reddit')

    col1,col2 = st.columns(2)
    with col2:
            sort_by = st.radio(
                    'sort submissions by:',
                    ['new','hot', 'controversial'],
                    index=0,
                    horizontal=True
                    )
            limit = sub_limit = st.number_input(
                    'max number of submissions to search per sub',
                    0,
                    None,
                    value=100,
                    step=1,
                    )
    with st.form('form'):
        subreddits =    st.text_input('space-seperated list of subreddits', help='Example: programminghumor vegan jokes').split()
        search_string = st.text_input('word or phrase to search')
        
        # remove invalid characters and r/ prefix
        subreddits = clean_subreddits(subreddits)
        

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
                        include_comments=include_comments,
                        limit=limit,
                        sort_by=sort_by
                        )
