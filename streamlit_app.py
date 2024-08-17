import streamlit as st
from openai import OpenAI
import html

# Access your API key securely
api_key = st.secrets["api_key"]

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=api_key)

# Define specific writer tones
writer_tones = {
    "None": "No specific writer tone",
    "Joanna Gaines": "Warm, personable, and slightly nostalgic",
    "Emily Henderson": "Friendly, accessible, and visually descriptive",
    "Martha Stewart": "Polished, informative, and inspirational",
    "Anne Lamott": "Honest, heartfelt, and introspective",
    "Nora Ephron": "Witty, insightful, with a touch of romantic comedy"
}

# Define available models
models = {
    "gpt-4": "GPT-4 (Default, more capable but slower)",
    "gpt-3.5-turbo": "GPT-3.5 (Faster, less capable)"
}

def generate_blog_post(couple_name, wedding_outline, photographer_name, tones, keywords, seo_keywords, writer_tone, model, client_testimonial, contact_page):
    writer_instruction = f"Write in the style of {writer_tone}: {writer_tones[writer_tone]}. " if writer_tone != "None" else ""
    
    testimonial_instruction = f'Include this client testimonial in a blockquote: "<blockquote>{html.escape(client_testimonial)}</blockquote>"' if client_testimonial.strip() else "Do not include a client testimonial."
    
    prompt = f"""
    {writer_instruction}Create a wedding blog post for a couple named {couple_name}, following this exact structure and using HTML tags:

    <h1>[Create a catchy title for the blog post, incorporating one or two SEO keywords if possible]</h1>

    <p>[Introductory Paragraph: Write a brief overview of the wedding day, setting the scene and introducing the couple. Try to naturally include one or two SEO keywords.]</p>

    <h2>A Day to Remember: {couple_name}'s [Location] Wedding</h2>

    <p>[In this section, summarize the key details of the wedding day. Include information about the ceremony and reception venues, any unique aspects of the wedding, and highlight some emotional moments. Use the following wedding outline, but ONLY include details that are provided (non-empty):
    {wedding_outline}
    Incorporate SEO keywords naturally throughout this section.]</p>

    <h2>Capturing Love and [Include one or two relevant SEO keywords]</h2>

    <p>[In this final section, focus on the SEO keywords the photographer wants to rank for. Describe how you, as the photographer, captured the essence of the day. Include the following keywords: {keywords}. Especially focus on these SEO keywords: {seo_keywords}. End with a call-to-action inviting readers to contact you for their own wedding photography needs, using the provided contact page link: {contact_page}]</p>

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

st.title("💍 Wedding Blog Post Generator")
st.write(
    "Welcome to the Wedding Blog Post Generator! This app helps wedding photographers create unique, SEO-optimized blog posts for their clients. You can leave any field blank if the information is not available or you don't want it included in the post."
)

st.subheader("Enter Wedding Details")

couple_name = st.text_input("Couple's Names", "Alice and Bob")

st.write("Wedding Outline (leave blank if you don't want this information in the post):")
ceremony_location = st.text_input("Ceremony Location", "Sunset Beach")
ceremony_city_state = st.text_input("Ceremony Venue City & State", "Malibu, California")
ceremony_time = st.text_input("Ceremony Time", "5:00 PM")
reception_venue = st.text_input("Reception Venue", "Oceanfront Resort Ballroom")
reception_city_state = st.text_input("Reception Venue City & State", "Malibu, California")
first_look = st.text_input("First Look Location (if applicable)", "Beach Gazebo")
first_dance_song = st.text_input("First Dance Song", "'At Last' by Etta James")
special_moments = st.text_area("Special Moments or Unique Aspects", "Surprise fireworks display, Sand ceremony")
decor_theme = st.text_input("Decor Theme/Colors", "Beach theme with shades of blue and coral")
weather = st.text_input("Weather Conditions", "Clear sky with a beautiful sunset")
emotional_highlight = st.text_area("Emotional Highlights", "Bride's father's touching speech, Groom's surprise serenade")

wedding_outline = "\n".join([
    f"- Ceremony: {ceremony_location + ' in ' + ceremony_city_state if ceremony_location and ceremony_city_state else ceremony_location or ceremony_city_state}",
    f"- Ceremony Time: {ceremony_time}",
    f"- Reception: {reception_venue + ' in ' + reception_city_state if reception_venue and reception_city_state else reception_venue or reception_city_state}",
    f"- First Look: {first_look}",
    f"- First Dance: {first_dance_song}",
    f"- Special Moments: {special_moments}",
    f"- Decor/Theme: {decor_theme}",
    f"- Weather: {weather}",
    f"- Emotional Highlights: {emotional_highlight}"
])

# Remove any lines where the value after the colon is empty
wedding_outline = "\n".join(line for line in wedding_outline.split("\n") if line.split(": ", 1)[1].strip())

photographer_name = st.text_input("Photographer's Name", "John Doe")

# Client's Testimonial with a default value
default_testimonial = "John captured our wedding day beautifully. The photos are stunning and truly reflect the joy and love we felt. We couldn't be happier!"
client_testimonial = st.text_area("Client's Testimonial (Optional)", default_testimonial)

# Hyperlink to Wedding Photographer's Contact Page
contact_page = st.text_input("Contact Page Hyperlink", "https://www.example.com/contact")

# Updated tone selection
tone_options = [
    "romantic", "fun", "elegant", "professional", "formal", "cheerful", "casual",
    "enthusiastic", "conversational", "informative", "quirky", "snarky",
    "trustworthy", "upbeat", "witty"
]
tones = st.multiselect("Overall Tone of the Blog Post (Select multiple)", tone_options, default=["romantic", "elegant"])

writer_tone = st.selectbox("Writing Style", list(writer_tones.keys()), format_func=lambda x: f"{x}: {writer_tones[x]}")
keywords = st.text_input("General Keywords (comma-separated)", "beach wedding, sunset, love, oceanfront")
seo_keywords = st.text_input("SEO Keywords to Feature (comma-separated)", "Malibu wedding photographer, beach wedding photography")

# Model selection
model = st.selectbox("Choose GPT Model", list(models.keys()), format_func=lambda x: models[x], index=0)

if st.button("Generate Blog Post"):
    if not couple_name:
        st.error("Please enter the couple's names before generating the blog post.")
    elif not photographer_name:
        st.error("Please enter the photographer's name before generating the blog post.")
    elif not tones:
        st.error("Please select at least one tone for the blog post.")
    else:
        with st.spinner(f"Generating blog post using {models[model]}..."):
            blog_post_html = generate_blog_post(couple_name, wedding_outline, photographer_name, tones, keywords, seo_keywords, writer_tone, model, client_testimonial, contact_page)
        
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