from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["api_key"])

def generate_blog_post(couple_name, wedding_outline, photographer_name, writing_sample, seo_keywords, model, client_testimonial, contact_page, cta_header_keywords, relationship_with_couple):
    # Generate SEO keywords if not provided
    if not seo_keywords:
        ceremony_location = next((line.split(':', 1)[1].strip() for line in wedding_outline.split('\n') if line.startswith('Ceremony Location:')), '')
        seo_keywords_prompt = f"Generate 5-7 relevant SEO keywords for a wedding blog post about a wedding in {ceremony_location}."
        seo_keywords_completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": seo_keywords_prompt}],
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        seo_keywords = seo_keywords_completion.choices[0].message.content.strip()

    # Analyze writing sample if provided
    style_instruction = ""
    if writing_sample:
        style_analysis_prompt = f"Analyze the following writing sample and describe its style characteristics:\n\n{writing_sample}"
        style_analysis_completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": style_analysis_prompt}],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        style_characteristics = style_analysis_completion.choices[0].message.content.strip()
        style_instruction = f"Mimic the following style characteristics in your writing: {style_characteristics}"
    else:
        style_instruction = "Write in a modern, realistic, and conversational style."

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
       - Structure the content with clear sections: introduction, ceremony details, reception highlights, couple's story, and conclusion.
       - Use appropriate HTML tags for headings (H1, H2, H3) and paragraphs.

    2. Specific Details:
       - Include precise details from the following wedding outline:
         {wedding_outline}
       - Describe the setting vividly, mentioning weather, decorations, and atmosphere.

    3. Personal Connection:
       - Incorporate personal details about your relationship with the couple: {relationship_with_couple}
       - Use this information to add a personal touch to the blog post.

    4. Emotional Connection:
       - Use emotive language to convey the romance and excitement of the day.
       - Include sensory details to help readers visualize the scene.

    5. SEO Optimization:
       - Naturally incorporate these SEO keywords throughout the post: {seo_keywords}
       - Use headers (H2, H3) to structure content and include keywords.
       - Create practical, search-friendly subheadings that reflect common search terms.

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
       - Only use hyperlinks that have been explicitly provided in the input.
       - When a URL is provided for a venue or business, create an HTML hyperlink like this:
         <a href="[provided_url]">[venue or business name]</a>
       - Do not create, assume, or make up any URLs that were not explicitly provided.
       - If no URL is provided for a mentioned venue or business, simply use the name without a hyperlink.
       - The only guaranteed link you should use is the contact page link in the call-to-action.

    Additional Guidelines:
    - Write from the consistent perspective of the photographer ({photographer_name}), maintaining a first-person point of view throughout the post.
    - {style_instruction}
    - Make sure the content is unique and reflects ONLY the specific details provided in the outline.
    - DO NOT mention or allude to any details that are not explicitly provided in the outline.
    - If a piece of information is not available, simply omit it from the blog post without drawing attention to its absence.
    - Do not include any section about photography insights or discuss the photography process.
    - End with a call-to-action inviting readers to contact you for their own wedding photography needs, using the provided contact page link: {contact_page}

    Follow this structure for the blog post:

    <h1>[Create a search-friendly title incorporating one or two SEO keywords]</h1>

    <p>[Introductory Paragraph: Set the scene, introduce the couple, and naturally include SEO keywords.]</p>

    <h2>[Ceremony Details: Use a practical, search-friendly subheading]</h2>

    <p>[Describe the ceremony, including time, venue details, and emotional highlights.]</p>

    <h2>[Reception Details: Use a practical, search-friendly subheading]</h2>

    <p>[Detail the reception, including venue, decor, special moments, and atmosphere.]</p>

    <h2>[Couple's Story: Use a practical, search-friendly subheading]</h2>

    <p>[Share personal details about the couple and your relationship with them.]</p>

    <h2>[Conclusion: Use a practical, search-friendly subheading]</h2>

    <p>[Summarize the wedding's unique aspects and end with a call-to-action.]</p>

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