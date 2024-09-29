import re
from unidecode import unidecode
import traceback

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