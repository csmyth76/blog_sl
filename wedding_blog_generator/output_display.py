import streamlit as st

def display_output(blog_post_html, permalink):
    st.subheader("Generated Blog Post:")
    st.components.v1.html(blog_post_html, height=600, scrolling=True)
    
    st.subheader("Suggested Permalink:")
    st.text(f"/{permalink}/")
    
    st.download_button(
        label="Download Blog Post as HTML",
        data=blog_post_html,
        file_name="wedding_blog_post.html",
        mime="text/html"
    )