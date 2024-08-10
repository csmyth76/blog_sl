import streamlit as st
from openai import OpenAI

# Access your API key securely
api_key = st.secrets["api_key"]

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=api_key)

# Define specific writer tones
writer_tones = {
    "None": "No specific writer tone",
    "Joanna Gaines": "Warm, personable, and slightly nostalgic",
    "Emily Henderson": "Friendly, accessible, and visually descriptive",
    "Jane Austen (modern)": "Romantic, subtle, with a timeless and whimsical touch",
    "Martha Stewart": "Polished, informative, and inspirational",
    "Anne Lamott": "Honest, heartfelt, and introspective",
    "Nora Ephron": "Witty, insightful, with a touch of romantic comedy"
}

# Define available models
models = {
    "gpt-4": "GPT-4 (Default, more capable but slower)",
    "gpt-3.5-turbo": "GPT-3.5 (Faster, less capable)"
}

def generate_blog_post(couple_name, wedding_outline, photographer_name, tone, keywords, writer_tone, model):
    writer_instruction = f"Write in the style of {writer_tone}: {writer_tones[writer_tone]}. " if writer_tone != "None" else ""
    
    prompt = f"""
    {writer_instruction}Create a wedding blog post for a couple named {couple_name}.
    Use the following wedding outline to structure the post, but ONLY include details that are provided (non-empty):
    {wedding_outline}
    The photographer is {photographer_name}.
    The overall tone should be {tone}.
    Include the following keywords: {keywords}.
    Make sure the content is unique and reflects ONLY the specific details provided in the outline.
    DO NOT mention or allude to any details that are not explicitly provided in the outline.
    If a piece of information is not available (i.e., if the corresponding field in the outline is empty), 
    simply omit it from the blog post without drawing attention to its absence.
    The blog post should be around 400 words long, but may be shorter if less information is provided.
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a skilled wedding blogger and photographer. Only use the information provided and do not invent or mention missing details."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=650,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return completion.choices[0].message.content.strip()

st.title("💍 Wedding Blog Post Generator")
st.write(
    "Welcome to the Wedding Blog Post Generator! This app helps wedding photographers create unique blog posts for their clients. You can leave any field blank if the information is not available or you don't want it included in the post."
)

st.subheader("Enter Wedding Details")

couple_name = st.text_input("Couple's Names", "Alice and Bob")

st.write("Wedding Outline (leave blank if you don't want this information in the post):")
ceremony_location = st.text_input("Ceremony Location", "Sunset Beach")
ceremony_time = st.text_input("Ceremony Time", "5:00 PM")
reception_venue = st.text_input("Reception Venue", "Oceanfront Resort Ballroom")
first_look = st.text_input("First Look Location (if applicable)", "Beach Gazebo")
first_dance_song = st.text_input("First Dance Song", "'At Last' by Etta James")
special_moments = st.text_area("Special Moments or Unique Aspects", "Surprise fireworks display, Sand ceremony")
decor_theme = st.text_input("Decor Theme/Colors", "Beach theme with shades of blue and coral")
weather = st.text_input("Weather Conditions", "Clear sky with a beautiful sunset")
emotional_highlight = st.text_area("Emotional Highlights", "Bride's father's touching speech, Groom's surprise serenade")

wedding_outline = "\n".join([
    f"- Ceremony: {ceremony_location + ' at ' + ceremony_time if ceremony_location and ceremony_time else ceremony_location or ceremony_time}",
    f"- Reception: {reception_venue}",
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
tone = st.selectbox("Overall Tone of the Blog Post", ["romantic", "fun", "elegant", "rustic", "modern"])
writer_tone = st.selectbox("Writing Style", list(writer_tones.keys()), format_func=lambda x: f"{x}: {writer_tones[x]}")
keywords = st.text_input("Keywords (comma-separated)", "beach wedding, sunset, love, oceanfront")

# Model selection
model = st.selectbox("Choose GPT Model", list(models.keys()), format_func=lambda x: models[x], index=0)

if st.button("Generate Blog Post"):
    if not couple_name:
        st.error("Please enter the couple's names before generating the blog post.")
    elif not photographer_name:
        st.error("Please enter the photographer's name before generating the blog post.")
    else:
        with st.spinner(f"Generating blog post using {models[model]}..."):
            blog_post = generate_blog_post(couple_name, wedding_outline, photographer_name, tone, keywords, writer_tone, model)
        
        st.subheader("Generated Blog Post:")
        st.write(blog_post)

        st.download_button(
            label="Download Blog Post",
            data=blog_post,
            file_name="wedding_blog_post.txt",
            mime="text/plain"
        )

st.write("---")
st.write("For help and inspiration on customizing this app, check out [docs.streamlit.io](https://docs.streamlit.io/).")