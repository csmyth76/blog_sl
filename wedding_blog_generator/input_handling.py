import streamlit as st
from .config import MODELS, SAMPLE_DATA

def get_user_inputs(test_mode):
    inputs = {}
    
    # Wedding Information
    inputs['wedding_date'] = st.date_input("Wedding Date", SAMPLE_DATA['wedding_date'] if test_mode else None)
    
    # Couple's Names
    st.subheader("Couple's Names*")
    col1, col2 = st.columns(2)
    with col1:
        inputs['partner1_name'] = st.text_input("Name of Partner 1*", SAMPLE_DATA['partner1_name'] if test_mode else "")
        inputs['partner1_gender'] = st.selectbox(
            "Gender of Partner 1", 
            ["", "Male", "Female", "Non-binary", "Prefer not to say"],
            index=["", "Male", "Female", "Non-binary", "Prefer not to say"].index(SAMPLE_DATA['partner1_gender']) if test_mode else 0
        )
    with col2:
        inputs['partner2_name'] = st.text_input("Name of Partner 2*", SAMPLE_DATA['partner2_name'] if test_mode else "")
        inputs['partner2_gender'] = st.selectbox(
            "Gender of Partner 2", 
            ["", "Male", "Female", "Non-binary", "Prefer not to say"],
            index=["", "Male", "Female", "Non-binary", "Prefer not to say"].index(SAMPLE_DATA['partner2_gender']) if test_mode else 0
        )
    
    # Ceremony Details
    st.subheader("Ceremony Details")
    col1, col2 = st.columns(2)
    with col1:
        inputs['ceremony_venue'] = st.text_input("Ceremony Venue Name*", SAMPLE_DATA['ceremony_venue'] if test_mode else "e.g., St. Mary's Church")
        inputs['ceremony_time'] = st.text_input("Ceremony Time", SAMPLE_DATA['ceremony_time'] if test_mode else "5:00 PM")
    with col2:
        inputs['ceremony_location'] = st.text_input("Ceremony City & State*", SAMPLE_DATA['ceremony_location'] if test_mode else "e.g., Malibu, California")
        inputs['ceremony_venue_url'] = st.text_input("Ceremony Venue Website (optional)", SAMPLE_DATA['ceremony_venue_url'] if test_mode else "")

    # Reception Details
    st.subheader("Reception Details")
    col1, col2 = st.columns(2)
    with col1:
        inputs['reception_venue'] = st.text_input("Reception Venue Name*", SAMPLE_DATA['reception_venue'] if test_mode else "e.g., Oceanfront Resort Ballroom")
        inputs['reception_time'] = st.text_input("Reception Time", SAMPLE_DATA['reception_time'] if test_mode else "7:00 PM")
    with col2:
        inputs['reception_location'] = st.text_input("Reception City & State*", SAMPLE_DATA['reception_location'] if test_mode else "e.g., Malibu, California")
        inputs['reception_venue_url'] = st.text_input("Reception Venue Website (optional)", SAMPLE_DATA['reception_venue_url'] if test_mode else "")

    inputs['decor_theme'] = st.text_input("Wedding Theme / Décor / Color Palette*", SAMPLE_DATA['decor_theme'] if test_mode else "e.g., Beach theme with shades of blue and coral")
    inputs['weather'] = st.text_input("Weather Conditions", SAMPLE_DATA['weather'] if test_mode else "e.g., Clear sky with a beautiful sunset")

    # Special Moments
    st.header("Special Moments")
    inputs['first_look'] = st.text_input("First Look Location (if applicable)", SAMPLE_DATA['first_look'] if test_mode else "e.g., Beach Gazebo")
    inputs['first_dance_song'] = st.text_input("First Dance Song", SAMPLE_DATA['first_dance_song'] if test_mode else "'At Last' by Etta James")
    inputs['emotional_moment'] = st.text_area("An Emotional Moment or Memory from the Day", SAMPLE_DATA['emotional_moment'] if test_mode else "e.g., Bride's father's touching speech")
    inputs['special_moments'] = st.text_area("Additional Special Moments or Unique Details", SAMPLE_DATA['special_moments'] if test_mode else "e.g., Surprise fireworks display, Sand ceremony")

    # Photographer Information
    st.header("Photographer Information")
    inputs['photographer_name'] = st.text_input("Photographer's Name*", SAMPLE_DATA['photographer_name'] if test_mode else "John Doe")
    inputs['photography_business'] = st.text_input("Photography Business Name*", SAMPLE_DATA['photography_business'] if test_mode else "John Doe Photography")
    inputs['client_testimonial'] = st.text_area("Client Testimonial", SAMPLE_DATA['client_testimonial'] if test_mode else "John captured our wedding day beautifully. The photos are stunning and truly reflect the joy and love we felt. We couldn't be happier!")
    
    if test_mode:
        inputs['contact_page'] = "https://www.example.com/contact"
        st.info(f"Test Mode: Using example contact page - {inputs['contact_page']}")
    else:
        inputs['contact_page'] = st.text_input("Contact Page Hyperlink*", "")

    # New field for photographer's relationship with the couple
    inputs['relationship_with_couple'] = st.text_area("Describe your relationship with the couple (e.g., fond memories of working together, inside jokes, anything you had in common, their dynamics as a couple, etc.)", 
                                                      SAMPLE_DATA.get('relationship_with_couple', '') if test_mode else "")

    # Blog Post Goals
    st.header("Blog Post Goals")
    
    # Writing sample input
    inputs['writing_sample'] = st.text_area("Provide a sample of your writing style (optional)", 
                                            SAMPLE_DATA.get('writing_sample', '') if test_mode else "")

    inputs['seo_keywords'] = st.text_input("SEO Keywords to Rank For (comma-separated, optional)", SAMPLE_DATA['seo_keywords'] if test_mode else "")
    inputs['cta_header_keywords'] = st.text_input("SEO Keywords for Call-to-Action Header", SAMPLE_DATA['cta_header_keywords'] if test_mode else "e.g., book wedding photographer, Malibu wedding photography")

    # Model selection
    model_index = list(MODELS.keys()).index(SAMPLE_DATA['model']) if test_mode else 0
    inputs['model'] = st.selectbox("Choose GPT Model", list(MODELS.keys()), index=model_index, format_func=lambda x: MODELS[x])

    return inputs