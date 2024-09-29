def process_inputs(inputs):
    processed_data = inputs.copy()
    
    # Combine partner names
    processed_data['couple_name'] = f"{inputs['partner1_name']} and {inputs['partner2_name']}" if inputs['partner1_name'] and inputs['partner2_name'] else ""
    
    # Prepare the wedding outline
    wedding_outline = "\n".join([
        f"- Couple: {processed_data['couple_name']}",
        f"- Ceremony Venue: {inputs['ceremony_venue']}",
        f"- Ceremony Location: {inputs['ceremony_location']}",
        f"- Ceremony Time: {inputs['ceremony_time']}",
        f"- Ceremony Venue URL: {inputs['ceremony_venue_url']}",
        f"- Reception Venue: {inputs['reception_venue']}",
        f"- Reception Location: {inputs['reception_location']}",
        f"- Reception Time: {inputs['reception_time']}",
        f"- Reception Venue URL: {inputs['reception_venue_url']}",
        f"- Wedding Theme/Décor: {inputs['decor_theme']}",
        f"- Weather: {inputs['weather']}",
        f"- First Look: {inputs['first_look']}",
        f"- First Dance: {inputs['first_dance_song']}",
        f"- Emotional Moment: {inputs['emotional_moment']}",
        f"- Special Moments: {inputs['special_moments']}"
    ])
    
    # Remove any lines where the value after the colon is empty
    processed_data['wedding_outline'] = "\n".join(line for line in wedding_outline.split("\n") if line.split(": ", 1)[1].strip())
    
    return processed_data