import streamlit as st
from openai import OpenAI
import html
import re
from unidecode import unidecode
import datetime

# Access your API key securely
api_key = st.secrets["api_key"]

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=api_key)

# Define available models
models = {
    "gpt-4": "GPT-4 (Default, more capable but slower)",
    "gpt-3.5-turbo": "GPT-3.5 (Faster, less capable)"
}

def generate_permalink(couple_name, ceremony_location, wedding_date):
    try:
        # Process couple's name: remove 'and', replace spaces with hyphens
        couple_name = couple_name.lower().replace(' and ', '-').replace(' ', '-')
        
        # Process location: replace spaces with hyphens
        location = ceremony_location.lower().replace(' ', '-')
        
        # Combine relevant information
        permalink = f"{couple_name}-{location}-{wedding_date}"
        
        # Convert to ASCII, remove non-alphanumeric characters (except hyphens)
        permalink = re.sub(r'[^a-z0-9-]+', '', unidecode(permalink))
        
        # Remove any double hyphens and trim hyphens from start/end
        permalink = re.sub(r'-+', '-', permalink).strip('-')
        
        return permalink
    except Exception as e:
        error_message = f"Error generating permalink: {str(e)}\n"
        error_message += f"Inputs: couple_name='{couple_name}', ceremony_location='{ceremony_location}', wedding_date='{wedding_date}'\n"
        error_message += f"Traceback: {traceback.format_exc()}"
        return None, error_message

def generate_blog_post(couple_name, wedding_outline, photographer_name, tones, seo_keywords, model, client_testimonial, contact_page, cta_header_keywords):
    testimonial_instruction = """
    If a client testimonial is provided, include it in the blog post as follows:
    <div class="testimonial">
        <blockquote>
            "[Insert the testimonial text here]"
        </blockquote>
        <p class="testimonial-author">- {couple_name}</p>
    </div>
    """ if client_testimonial.strip() else "Do not include a testimonial in the blog post."
    
    prompt = f"""
    Create a wedding blog post for a couple named {couple_name}, following these instructions:

    1. Word Count and Structure:
       - Write between 500-1000 words.
       - Structure the content with clear sections: introduction, ceremony details, reception highlights, photography insights, and conclusion.
       - Use appropriate HTML tags for headings (H1, H2, H3) and paragraphs.

    2. Specific Details:
       - Include precise details from the following wedding outline:
         {wedding_outline}
       - Describe the setting vividly, mentioning weather, decorations, and atmosphere.

    3. Photography Focus:
       - Incorporate information about photography techniques specific to beach weddings.
       - Describe challenges and solutions in capturing outdoor wedding moments.

    4. Emotional Connection:
       - Use emotive language to convey the romance and excitement of the day.
       - Include sensory details to help readers visualize the scene.

    5. SEO Optimization:
       - Naturally incorporate these SEO keywords throughout the post: {seo_keywords}
       - Use headers (H2, H3) to structure content and include keywords.

    6. Engagement Elements:
       - Add 1-2 questions within the post to encourage reader interaction.
       - Include a clear call-to-action, not just at the end but woven into the narrative.

    7. Credibility:
       {testimonial_instruction}
       - Mention specific vendor names or popular local wedding spots to add authenticity.

    8. Value Addition:
       - Include 2-3 tips for couples planning a similar wedding.
       - Briefly explain why the location is ideal for weddings.

    9. Hyperlinks:
       - When mentioning venues or businesses with provided URLs, create HTML hyperlinks.
       - For example, if given "Oceanfront Resort Ballroom (https://www.example.com)", 
         create a link like this: <a href="https://www.example.com">Oceanfront Resort Ballroom</a>
       - Do not use parentheses to show URLs. Always create proper HTML links.

    Additional Guidelines:
    - Write from the consistent perspective of the photographer ({photographer_name}), maintaining a first-person point of view throughout the post.
    - The overall tone should be a combination of the following: {', '.join(tones)}.
    - Make sure the content is unique and reflects ONLY the specific details provided in the outline.
    - DO NOT mention or allude to any details that are not explicitly provided in the outline.
    - If a piece of information is not available, simply omit it from the blog post without drawing attention to its absence.
    - End with a call-to-action inviting readers to contact you for their own wedding photography needs, using the provided contact page link: {contact_page}

    Follow this structure for the blog post:

    <h1>[Create a catchy title incorporating one or two SEO keywords]</h1>

    <p>[Introductory Paragraph: Set the scene, introduce the couple, and naturally include SEO keywords.]</p>

    <h2>[Ceremony Details: Include location name and incorporate relevant keywords]</h2>

    <p>[Describe the ceremony, including time, venue details, and emotional highlights.]</p>

    <h2>[Reception Highlights: Use location or theme-related keywords]</h2>

    <p>[Detail the reception, including venue, decor, special moments, and atmosphere.]</p>

    <h2>[Photography Insights: Include keywords related to wedding photography]</h2>

    <p>[Discuss photography techniques, challenges, and solutions specific to this wedding.]</p>

    <h2>[Conclusion: Wrap up with a keyword-rich title]</h2>

    <p>[Summarize the wedding's unique aspects, include tips for similar weddings, and end with a call-to-action.]</p>

    [If a testimonial was provided, insert it here using the format specified in the testimonial instruction.]

    <h2>[Create a header using the following SEO keywords: {cta_header_keywords}]</h2>

    <p>[Write a compelling call-to-action paragraph inviting readers to book your services. Include the contact page link: {contact_page}]</p>
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a skilled wedding photographer writing a structured, SEO-optimized blog post in HTML format. Maintain a consistent first-person perspective throughout the post and follow the given structure and instructions exactly."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return completion.choices[0].message.content.strip()

# Step 1: Add Test Mode Toggle
test_mode = st.sidebar.checkbox("Enable Test Mode")

# Step 2: Define Sample Data
SAMPLE_DATA = {
    'partner1_name': 'Alex',
    'partner1_gender': 'Male',
    'partner2_name': 'Jordan',
    'partner2_gender': 'Female',
    'wedding_date': datetime.date(2023, 10, 15),
    'ceremony_venue': "St. Mary's Church",
    'ceremony_time': '5:00 PM',
    'ceremony_location': 'Malibu, California',
    'ceremony_venue_url': 'https://www.stmaryschurch.com',
    'reception_venue': 'Oceanfront Resort Ballroom',
    'reception_time': '7:00 PM',
    'reception_location': 'Malibu, California',
    'reception_venue_url': 'https://www.oceanfrontresort.com',
    'decor_theme': 'Beach theme with shades of blue and coral',
    'weather': 'Clear sky with a beautiful sunset',
    'first_look': 'Beach Gazebo',
    'first_dance_song': "'At Last' by Etta James",
    'emotional_moment': "Bride's father's touching speech",
    'special_moments': 'Surprise fireworks display, Sand ceremony',
    'photographer_name': 'John Doe',
    'photography_business': 'John Doe Photography',
    'client_testimonial': "John captured our wedding day beautifully. The photos are stunning and truly reflect the joy and love we felt. We couldn't be happier!",
    'contact_page': 'https://www.example.com/contact',
    'selected_tones': ['Romantic', 'Professional'],
    'seo_keywords': 'Malibu wedding photographer, beach wedding photography',
    'cta_header_keywords': 'book wedding photographer, Malibu wedding photography',
    'model': 'gpt-4'
}

st.title("💍 Wedding Blog Post Generator")
st.write(
    "Create SEO-ready blog posts on behalf of your business. Complete as many fields as possible or applicable to better ensure a strengthened blog post."
)

st.write("Fields marked with an asterisk (*) are required.")

# a. Wedding Information
st.header("Wedding Information")

# Step 3: Modify Input Fields to Use Sample Data in Test Mode
if test_mode:
    wedding_date = st.date_input("Wedding Date", SAMPLE_DATA['wedding_date'])
else:
    wedding_date = st.date_input("Wedding Date", value=None)

st.subheader("Couple's Names*")
col1, col2 = st.columns(2)
with col1:
    if test_mode:
        partner1_name = st.text_input("Name of Partner 1*", SAMPLE_DATA['partner1_name'])
        partner1_gender = st.selectbox(
            "Gender of Partner 1", 
            ["", "Male", "Female", "Non-binary", "Prefer not to say"],
            index=["", "Male", "Female", "Non-binary", "Prefer not to say"].index(SAMPLE_DATA['partner1_gender'])
        )
    else:
        partner1_name = st.text_input("Name of Partner 1*", "")
        partner1_gender = st.selectbox("Gender of Partner 1", ["", "Male", "Female", "Non-binary", "Prefer not to say"])
with col2:
    if test_mode:
        partner2_name = st.text_input("Name of Partner 2*", SAMPLE_DATA['partner2_name'])
        partner2_gender = st.selectbox(
            "Gender of Partner 2", 
            ["", "Male", "Female", "Non-binary", "Prefer not to say"],
            index=["", "Male", "Female", "Non-binary", "Prefer not to say"].index(SAMPLE_DATA['partner2_gender'])
        )
    else:
        partner2_name = st.text_input("Name of Partner 2*", "")
        partner2_gender = st.selectbox("Gender of Partner 2", ["", "Male", "Female", "Non-binary", "Prefer not to say"])

# Combine partner names for use in the rest of the application
couple_name = f"{partner1_name} and {partner2_name}" if partner1_name and partner2_name else ""

st.subheader("Ceremony Details")
col1, col2 = st.columns(2)
with col1:
    if test_mode:
        ceremony_venue = st.text_input("Ceremony Venue Name*", SAMPLE_DATA['ceremony_venue'])
        ceremony_time = st.text_input("Ceremony Time", SAMPLE_DATA['ceremony_time'])
    else:
        ceremony_venue = st.text_input("Ceremony Venue Name*", "e.g., St. Mary's Church")
        ceremony_time = st.text_input("Ceremony Time", "5:00 PM")
with col2:
    if test_mode:
        ceremony_location = st.text_input("Ceremony City & State*", SAMPLE_DATA['ceremony_location'])
        ceremony_venue_url = st.text_input("Ceremony Venue Website (optional)", SAMPLE_DATA['ceremony_venue_url'])
    else:
        ceremony_location = st.text_input("Ceremony City & State*", "e.g., Malibu, California")
        ceremony_venue_url = st.text_input("Ceremony Venue Website (optional)", "")

st.subheader("Reception Details")
col1, col2 = st.columns(2)
with col1:
    if test_mode:
        reception_venue = st.text_input("Reception Venue Name*", SAMPLE_DATA['reception_venue'])
        reception_time = st.text_input("Reception Time", SAMPLE_DATA['reception_time'])
    else:
        reception_venue = st.text_input("Reception Venue Name*", "e.g., Oceanfront Resort Ballroom")
        reception_time = st.text_input("Reception Time", "7:00 PM")
with col2:
    if test_mode:
        reception_location = st.text_input("Reception City & State*", SAMPLE_DATA['reception_location'])
        reception_venue_url = st.text_input("Reception Venue Website (optional)", SAMPLE_DATA['reception_venue_url'])
    else:
        reception_location = st.text_input("Reception City & State*", "e.g., Malibu, California")
        reception_venue_url = st.text_input("Reception Venue Website (optional)", "")

if test_mode:
    decor_theme = st.text_input("Wedding Theme / Décor / Color Palette*", SAMPLE_DATA['decor_theme'])
    weather = st.text_input("Weather Conditions", SAMPLE_DATA['weather'])
else:
    decor_theme = st.text_input("Wedding Theme / Décor / Color Palette*", "e.g., Beach theme with shades of blue and coral")
    weather = st.text_input("Weather Conditions", "e.g., Clear sky with a beautiful sunset")

# b. Special Moments
st.header("Special Moments")
if test_mode:
    first_look = st.text_input("First Look Location (if applicable)", SAMPLE_DATA['first_look'])
    first_dance_song = st.text_input("First Dance Song", SAMPLE_DATA['first_dance_song'])
    emotional_moment = st.text_area("An Emotional Moment or Memory from the Day", SAMPLE_DATA['emotional_moment'])
    special_moments = st.text_area("Additional Special Moments or Unique Details", SAMPLE_DATA['special_moments'])
else:
    first_look = st.text_input("First Look Location (if applicable)", "e.g., Beach Gazebo")
    first_dance_song = st.text_input("First Dance Song", "'At Last' by Etta James")
    emotional_moment = st.text_area("An Emotional Moment or Memory from the Day", "e.g., Bride's father's touching speech")
    special_moments = st.text_area("Additional Special Moments or Unique Details", "e.g., Surprise fireworks display, Sand ceremony")

# c. Photographer Information
st.header("Photographer Information")
if test_mode:
    photographer_name = st.text_input("Photographer's Name*", SAMPLE_DATA['photographer_name'])
    photography_business = st.text_input("Photography Business Name*", SAMPLE_DATA['photography_business'])
    client_testimonial = st.text_area("Client Testimonial", SAMPLE_DATA['client_testimonial'])
    contact_page = st.text_input("Contact Page Hyperlink", SAMPLE_DATA['contact_page'])
else:
    photographer_name = st.text_input("Photographer's Name*", "John Doe")
    photography_business = st.text_input("Photography Business Name*", "John Doe Photography")
    client_testimonial = st.text_area("Client Testimonial", "John captured our wedding day beautifully. The photos are stunning and truly reflect the joy and love we felt. We couldn't be happier!")
    contact_page = st.text_input("Contact Page Hyperlink", "https://www.example.com/contact")

# d. Blog Post Goals
st.header("Blog Post Goals")
st.subheader("Overall tone of the blog post (check all that apply)*")

tone_options = [
    "casual", "cheerful", "conversational", "elegant", "enthusiastic", "formal",
    "fun", "informative", "professional", "quirky", "romantic", "snarky",
    "trustworthy", "upbeat", "witty"
]

# Sort the tone options alphabetically
sorted_tones = sorted(tone_options)

# Calculate the number of tones per column (5 tones per column)
tones_per_column = 5
num_columns = (len(sorted_tones) + tones_per_column - 1) // tones_per_column

# Create columns
cols = st.columns(num_columns)

# Dictionary to store the state of each checkbox
tone_checkboxes = {}

# Distribute checkboxes across columns
for i, tone in enumerate(sorted_tones):
    with cols[i // tones_per_column]:
        if test_mode:
            tone_checkboxes[tone] = st.checkbox(tone.capitalize(), value=tone.capitalize() in SAMPLE_DATA['selected_tones'])
        else:
            tone_checkboxes[tone] = st.checkbox(tone.capitalize())

# Get the selected tones
selected_tones = [tone for tone, checked in tone_checkboxes.items() if checked]

if test_mode:
    seo_keywords = st.text_input("SEO Keywords to Rank For (comma-separated)*", SAMPLE_DATA['seo_keywords'])
    cta_header_keywords = st.text_input("SEO Keywords for Call-to-Action Header", SAMPLE_DATA['cta_header_keywords'])
else:
    seo_keywords = st.text_input("SEO Keywords to Rank For (comma-separated)*", "Malibu wedding photographer, beach wedding photography")
    cta_header_keywords = st.text_input("SEO Keywords for Call-to-Action Header", "e.g., book wedding photographer, Malibu wedding photography")

# Model selection
if test_mode:
    model_index = list(models.keys()).index(SAMPLE_DATA['model'])
    model = st.selectbox("Choose GPT Model", list(models.keys()), index=model_index, format_func=lambda x: models[x])
else:
    model = st.selectbox("Choose GPT Model", list(models.keys()), format_func=lambda x: models[x], index=0)

# Step 4: Ensure Switching Between Modes is Smooth
if 'prev_test_mode' not in st.session_state:
    st.session_state['prev_test_mode'] = test_mode
elif st.session_state['prev_test_mode'] != test_mode:
    st.session_state['prev_test_mode'] = test_mode
    st.rerun()

# Prepare the wedding outline
wedding_outline = "\n".join([
    f"- Couple: {couple_name}",
    f"- Ceremony Venue: {ceremony_venue}",
    f"- Ceremony Location: {ceremony_location}",
    f"- Ceremony Time: {ceremony_time}",
    f"- Ceremony Venue URL: {ceremony_venue_url}",
    f"- Reception Venue: {reception_venue}",
    f"- Reception Location: {reception_location}",
    f"- Reception Time: {reception_time}",
    f"- Reception Venue URL: {reception_venue_url}",
    f"- Wedding Theme/Décor: {decor_theme}",
    f"- Weather: {weather}",
    f"- First Look: {first_look}",
    f"- First Dance: {first_dance_song}",
    f"- Emotional Moment: {emotional_moment}",
    f"- Special Moments: {special_moments}"
])

# Remove any lines where the value after the colon is empty
wedding_outline = "\n".join(line for line in wedding_outline.split("\n") if line.split(": ", 1)[1].strip())

if st.button("Generate Blog Post"):

    if not partner1_name or not partner2_name:
        st.error("Please enter both partners' names before generating the blog post.")
    elif not photographer_name or not photography_business:
        st.error("Please enter the photographer's name and business name before generating the blog post.")
    elif not ceremony_venue or not ceremony_location or not reception_venue or not reception_location or not decor_theme:
        st.error("Please fill in all required wedding information fields (marked with *) before generating the blog post.")
    elif not selected_tones or not seo_keywords:
        st.error("Please select at least one tone and enter SEO keywords before generating the blog post.")
    else:
        with st.spinner(f"Generating blog post using {models[model]}..."):
            blog_post_html = generate_blog_post(
                couple_name, wedding_outline, photographer_name, selected_tones, seo_keywords, model, client_testimonial, contact_page, cta_header_keywords)
        
        st.subheader("Generated Blog Post:")
        st.components.v1.html(blog_post_html, height=600, scrolling=True)

        # Generate and display permalink suggestion with error handling
        permalink_result = generate_permalink(couple_name, ceremony_location, wedding_date.strftime("%Y-%m-%d"))

        if isinstance(permalink_result, tuple):  # Error occurred
            st.error("Permalink could not be created. Here's the error information:")
            st.text(permalink_result[1])
        else:
            st.subheader("Suggested Permalink:")
            st.text(f"/{permalink_result}/")

        st.download_button(
            label="Download Blog Post as HTML",
            data=blog_post_html,
            file_name="wedding_blog_post.html",
            mime="text/html"
        )

st.write("---")
st.write("For help and inspiration on customizing this app, check out [docs.streamlit.io](https://docs.streamlit.io/).")