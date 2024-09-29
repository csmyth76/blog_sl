import datetime

# Define available models
MODELS = {
    "gpt-4": "GPT-4 (Default, more capable but slower)",
    "gpt-3.5-turbo": "GPT-3.5 (Faster, less capable)"
}

# Define sample data
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