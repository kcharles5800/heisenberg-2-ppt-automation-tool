import urllib.parse
import requests
from bs4 import BeautifulSoup


def find_song_url_by_name(song_name):
    # 1. Format the typed query safely for the URL search parameter
    encoded_name = urllib.parse.quote_plus(song_name)
    search_url = f"https://tamilchristiansongs.in/?s={encoded_name}"
    
    # 2. Download the search results page
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 3. Targeted Strike: Look for the class container seen in the inspector
    title_container = soup.find(class_="entry-title")
    
    if title_container:
        # Find the anchor link nested directly inside this container
        link_tag = title_container.find("a")
        if link_tag and link_tag.has_attr("href"):
            return link_tag["href"]
            
    # 3. Bulletproof Fallback: Scan all links if the specific class is missing
    for anchor in soup.find_all("a", href=True):
        if "/lyrics/" in anchor["href"] and "?s=" not in anchor["href"]:
            return anchor["href"]

    return None

# Target URL to scrape data from
#target_URL = "https://tamilchristiansongs.in/lyrics/deiveega-koodarame-en-devanin/"

def sanitize_english_line(text_line):
    """
    Removes non-ASCII scripts, isolated Tamil marks, and broken placeholder 
    dotted circle glyphs from Romanized lines before rendering.
    """
    if not text_line:
        return ""
    
    # Remove the unicode dotted circle glyph explicit artifact
    clean_line = text_line.replace("\u25cc", "").replace("◌", "")
    
    # Keep only standard alphanumerics, spaces, and basic lyrics punctuation
    import re
    clean_line = re.sub(r'[^a-zA-Z0-9\s.,\/#!$%\^&\*;:{}=\-_`~()?"\'’\[\]+–—]', "", clean_line)
    
    # Collapse any accidental double spaces down
    return re.sub(r' +', ' ', clean_line).strip()

# function to scrap data
# function to scrap data
def get_scraped_lyrics(target_URL):
    # To Avoid bot checks
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    # Download website content
    response = requests.get(target_URL, headers=headers)

    # Turn the collected data into searchable beautifulsoup object
    soup = BeautifulSoup(response.text, "html.parser")

    # Response code 200 = Success
    print(f"Website Response Code: {response.status_code}")

    # search for the title of the song
    title_tag = soup.find("h1") or soup.find(class_="entry-title")
    song_title = "New_song" # Default backup name

    if title_tag:
        raw_title = title_tag.get_text().strip()
        # hyphen separates the English & Tamil text, split and take only English text
        if "-" in raw_title:
            song_title = raw_title.split("-")[0].strip()
        else:
            song_title = raw_title

    # finding the english lyrics & tamil lyrics
    english_div = soup.find("div", id = "roman_tamiltext")
    tamil_div = soup.find("div", id = "tamiltext")

    # safety check for typos
    if not english_div or not tamil_div:
        raise Exception("Lyrics found. Please check your spelling and try again!")

    # getting all the paragraphs and skipping the title
    eng_paragraphs = english_div.find_all("p")[0:]
    tam_paragraphs = tamil_div.find_all("p")[0:]

    # Making a list (of stanzas) of lists (of lines)
    eng_slides = []
    tamil_slides = []

    # Loop through both language stanzas simultaneously to ensure perfect synchronization
    for eng_stanza, tam_stanza in zip(eng_paragraphs, tam_paragraphs):
        
        # 1. Extract, sanitize, and clean English lines
        raw_eng_lines = eng_stanza.get_text(separator="\n").strip().split("\n")
        clean_eng = []
        for line in raw_eng_lines:
            if line.strip():
                sanitized = sanitize_english_line(line)
                if sanitized:  # Only add if there's text left after stripping glitches
                    clean_eng.append(sanitized)

        # 2. Extract and clean Tamil lines
        raw_tam_lines = tam_stanza.get_text(separator="\n").strip().split("\n")
        clean_tam = [line.strip() for line in raw_tam_lines if line.strip()]

        # Ensure both stanzas actually have lines to process
        total_lines = max(len(clean_eng), len(clean_tam))
        if total_lines == 0:
            continue

        # 3. Check if ANY line in this stanza exceeds our safe character limit
        CHARACTER_LIMIT = 45
        has_long_lines = any(len(l) > CHARACTER_LIMIT for l in clean_eng) or any(len(l) > CHARACTER_LIMIT for l in clean_tam)

        # 4. Apply Dynamic Split Rules based on line counts and line lengths
        if has_long_lines:
            # ADAPTIVE HEAVY SPLIT: Chop into strict 2-line slides if text strings wrap dangerously
            for i in range(0, total_lines, 2):
                eng_chunk = clean_eng[i:i+2]
                tam_chunk = clean_tam[i:i+2]
                if eng_chunk or tam_chunk:
                    eng_slides.append(eng_chunk)
                    tamil_slides.append(tam_chunk)

        elif total_lines > 4:
            # --- FIXED FOR THE EDGE CASE: DYNAMIC MAXIMUM 4 LINES PER SLIDE ---
            # Handles 5, 6, 7, 8+ lines gracefully by looping in chunks of 4
            for i in range(0, total_lines, 4):
                eng_chunk = clean_eng[i:i+4]
                tam_chunk = clean_tam[i:i+4]
                if eng_chunk or tam_chunk:
                    eng_slides.append(eng_chunk)
                    tamil_slides.append(tam_chunk)
                    
        else:
            # 4 lines or fewer stay completely together on a single slide frame
            eng_slides.append(clean_eng)
            tamil_slides.append(clean_tam)

    return song_title, eng_slides, tamil_slides