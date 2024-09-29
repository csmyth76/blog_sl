import streamlit as st

from wedding_blog_generator.input_handling import get_user_inputs
from wedding_blog_generator.data_processing import process_inputs
from wedding_blog_generator.blog_generation import generate_blog_post
from wedding_blog_generator.permalink_generation import generate_permalink
from wedding_blog_generator.output_display import display_output
from wedding_blog_generator.config import MODELS

def main():
    st.title("💍 Wedding Blog Post Generator")
    st.write(
        "Create SEO-ready blog posts on behalf of your business. Complete as many fields as possible or applicable to better ensure a strengthened blog post."
    )
    st.write("Fields marked with an asterisk (*) are required.")

    # Test Mode Toggle
    test_mode = st.sidebar.checkbox("Enable Test Mode")

    # Get User Inputs
    inputs = get_user_inputs(test_mode)

    # Process Inputs
    processed_data = process_inputs(inputs)

    if st.button("Generate Blog Post"):
        if not inputs['partner1_name'] or not inputs['partner2_name']:
            st.error("Please enter both partners' names before generating the blog post.")
        elif not inputs['photographer_name'] or not inputs['photography_business']:
            st.error("Please enter the photographer's name and business name before generating the blog post.")
        elif not inputs['ceremony_venue'] or not inputs['ceremony_location'] or not inputs['reception_venue'] or not inputs['reception_location'] or not inputs['decor_theme']:
            st.error("Please fill in all required wedding information fields (marked with *) before generating the blog post.")
        elif not test_mode and not inputs['contact_page']:
            st.error("Please provide a contact page URL for the call-to-action.")
        else:
            with st.spinner(f"Generating blog post using {MODELS[inputs['model']]}..."):
                blog_post_html = generate_blog_post(
                    processed_data['couple_name'], 
                    processed_data['wedding_outline'], 
                    inputs['photographer_name'], 
                    inputs['writing_sample'],
                    inputs['seo_keywords'], 
                    inputs['model'], 
                    inputs['client_testimonial'], 
                    inputs['contact_page'], 
                    inputs['cta_header_keywords'],
                    inputs['relationship_with_couple']
                )
            
            # Generate and display permalink suggestion with error handling
            permalink_result = generate_permalink(processed_data['couple_name'], inputs['ceremony_location'], inputs['wedding_date'].strftime("%Y-%m-%d"))

            if isinstance(permalink_result, tuple):  # Error occurred
                st.error("Permalink could not be created. Here's the error information:")
                st.text(permalink_result[1])
            else:
                display_output(blog_post_html, permalink_result)

    st.write("---")
    st.write("For help and inspiration on customizing this app, check out [docs.streamlit.io](https://docs.streamlit.io/).")

if __name__ == "__main__":
    main()