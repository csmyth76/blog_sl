from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["api_key"])

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