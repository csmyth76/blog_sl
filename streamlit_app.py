import streamlit as st
from openai import OpenAI
import html

# Access your API key securely
api_key = st.secrets["api_key"]

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=api_key)

# Define available models
models = {
    "gpt-4": "GPT-4 (Default, more capable but slower)",
    "gpt-3.5-turbo": "GPT-3.5 (Faster, less capable)"
}

def generate_blog_post(couple_name, wedding_outline, photographer_name, tones, seo_keywords, model, client_testimonial, contact_page):
    testimonial_instruction = f'Include this client testimonial in a blockquote: "<blockquote>{html.escape(client_testimonial)}</blockquote>"' if client_testimonial.strip() else "Do not include a client testimonial."
    
    prompt = f"""
    Create a wedding blog post for a couple named {couple_name}, following this exact structure and using HTML tags:

    <h1>[Create a catchy title for the blog post, incorporating one or two SEO keywords if possible]</h1>

    <p>[Introductory Paragraph: Write a brief overview of the wedding day, setting the scene and introducing the couple. Try to naturally include one or two SEO keywords.]</p>

    <h2>A Day to Remember: {couple_name}'s [Location] Wedding</h2>

    <p>[In this section, summarize the key details of the wedding day. Include information about the ceremony and reception venues, any unique aspects of the wedding, and highlight some emotional moments. Use the following wedding outline, but ONLY include details that are provided (non-empty):
    {wedding_outline}
    Incorporate SEO keywords naturally throughout this section.]</p>

    <h2>Capturing Love and [Include one or two relevant SEO keywords]</h2>

    <p>[In this final section, focus on the SEO keywords the photographer wants to rank for. Describe how you, as the photographer, captured the essence of the day. Especially focus on these SEO keywords: {seo_keywords}. End with a call-to-action inviting readers to contact you for their own wedding photography needs, using the provided contact page link: {contact_page}]</p>

    {testimonial_instruction}

    Write from the consistent perspective of the photographer ({photographer_name}), maintaining a first-person point of view throughout the post.
    The overall tone should be a combination of the following: {', '.join(tones)}.
    Make sure the content is unique and reflects ONLY the specific details provided in the outline.
    DO NOT mention or allude to any details that are not explicitly provided in the outline.
    If a piece of information is not available (i.e., if the corresponding field in the outline is empty), 
    simply omit it from the blog post without drawing attention to its absence.
    The blog post should be around 400-500 words long.
    Remember to maintain a consistent first-person perspective as the photographer throughout the entire post.
    Naturally incorporate the SEO keywords throughout the post, ensuring they fit seamlessly into the content.
    Use appropriate HTML tags for paragraphs, emphasis, and links where necessary.
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a skilled wedding photographer writing a structured, SEO-optimized blog post in HTML format. Maintain a consistent first-person perspective throughout the post and follow the given structure exactly."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return completion.choices[0].message.content.strip()



def generate_blog_post(couple_name, wedding_outline, photographer_name, tones, seo_keywords, model, client_testimonial, contact_page):
    testimonial_instruction = f'Include this client testimonial in a blockquote: "<blockquote>{html.escape(client_testimonial)}</blockquote>"' if client_testimonial.strip() else "Generate a realistic testimonial quote from the couple."
    
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

    {testimonial_instruction}
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



st.title("💍 Wedding Blog Post Generator")
st.write(
    "Create SEO-ready blog posts on behalf of your business. Complete as many fields as possible or applicable to better ensure a strengthened blog post."
)

st.write("Fields marked with an asterisk (*) are required.")

# a. Wedding Information
st.header("Wedding Information")

st.subheader("Couple's Names*")
col1, col2 = st.columns(2)
with col1:
    partner1_name = st.text_input("Name of Partner 1*", "")
    partner1_gender = st.selectbox("Gender of Partner 1", ["", "Male", "Female", "Non-binary", "Prefer not to say"])
with col2:
    partner2_name = st.text_input("Name of Partner 2*", "")
    partner2_gender = st.selectbox("Gender of Partner 2", ["", "Male", "Female", "Non-binary", "Prefer not to say"])

# Combine partner names for use in the rest of the application
couple_name = f"{partner1_name} and {partner2_name}" if partner1_name and partner2_name else ""

st.subheader("Ceremony Details")
col1, col2 = st.columns(2)
with col1:
    ceremony_venue = st.text_input("Ceremony Venue Name*", "e.g., St. Mary's Church")
    ceremony_time = st.text_input("Ceremony Time", "5:00 PM")
with col2:
    ceremony_location = st.text_input("Ceremony City & State*", "e.g., Malibu, California")

st.subheader("Reception Details")
col1, col2 = st.columns(2)
with col1:
    reception_venue = st.text_input("Reception Venue Name*", "e.g., Oceanfront Resort Ballroom")
    reception_time = st.text_input("Reception Time", "7:00 PM")
with col2:
    reception_location = st.text_input("Reception City & State*", "e.g., Malibu, California")

decor_theme = st.text_input("Wedding Theme / Décor / Color Palette*", "e.g., Beach theme with shades of blue and coral")
weather = st.text_input("Weather Conditions", "e.g., Clear sky with a beautiful sunset")

# b. Special Moments
st.header("Special Moments")
first_look = st.text_input("First Look Location (if applicable)", "e.g., Beach Gazebo")
first_dance_song = st.text_input("First Dance Song", "'At Last' by Etta James")
emotional_moment = st.text_area("An Emotional Moment or Memory from the Day", "e.g., Bride's father's touching speech")
special_moments = st.text_area("Additional Special Moments or Unique Details", "e.g., Surprise fireworks display, Sand ceremony")

# c. Photographer Information
st.header("Photographer Information")
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
        tone_checkboxes[tone] = st.checkbox(tone.capitalize())

# Get the selected tones
selected_tones = [tone for tone, checked in tone_checkboxes.items() if checked]

seo_keywords = st.text_input("SEO Keywords to Rank For (comma-separated)*", "Malibu wedding photographer, beach wedding photography")

# Model selection
model = st.selectbox("Choose GPT Model", list(models.keys()), format_func=lambda x: models[x], index=0)

wedding_outline = "\n".join([
    f"- Couple: {couple_name}",
    f"- Ceremony Venue: {ceremony_venue}",
    f"- Ceremony Location: {ceremony_location}",
    f"- Ceremony Time: {ceremony_time}",
    f"- Reception Venue: {reception_venue}",
    f"- Reception Location: {reception_location}",
    f"- Reception Time: {reception_time}",
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
            blog_post_html = generate_blog_post(couple_name, wedding_outline, photographer_name, selected_tones, seo_keywords, model, client_testimonial, contact_page)
        
        st.subheader("Generated Blog Post:")
        st.components.v1.html(blog_post_html, height=600, scrolling=True)

        st.download_button(
            label="Download Blog Post as HTML",
            data=blog_post_html,
            file_name="wedding_blog_post.html",
            mime="text/html"
        )

st.write("---")
st.write("For help and inspiration on customizing this app, check out [docs.streamlit.io](https://docs.streamlit.io/).")