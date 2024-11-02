from PIL import Image, ImageDraw, ImageFont
import os
from unidecode import unidecode
import spacy
from spacy.matcher import Matcher

# Load the spaCy model for Spanish
nlp = spacy.load("es_core_news_sm")

# Create a matcher to identify specific words
matcher = Matcher(nlp.vocab)
patterns = [
    [{"LOWER": "asno"}], [{"LOWER": "calamar"}], [{"LOWER": "canguro"}],
    [{"LOWER": "pavo"}], [{"LOWER": "azul"}], [{"LOWER": "morado"}],
    [{"LOWER": "asomar"}], [{"LOWER": "bailar"}], [{"LOWER": "estar"}]
]

matcher.add("NOUNS_CORRECTION", patterns)

# Input text
text = "Tengo 27 años, mi hermana tiene 25 y mi padre tiene 55 años."
final_phrase=text
numImagen = 9

# Directories for word images based on POS tag
words_dir = {
    "ADJ": "Palabras/CategoriaGramatical(POS)/Adjetivos",
    "ADP": "Palabras/CategoriaGramatical(POS)/Preposicion",
    "ADV": "Palabras/CategoriaGramatical(POS)/Adverbio",
    "AUX": "Palabras/CategoriaGramatical(POS)/Auxiliar",
    "CCONJ": "Palabras/CategoriaGramatical(POS)/Conjuncion",
    "DET": "Palabras/CategoriaGramatical(POS)/Articulos",
    "INTJ": "Palabras/CategoriaGramatical(POS)/Interjeccion",
    "NOUN": "Palabras/CategoriaGramatical(POS)/Sustantivo",
    "NUM": "Palabras/CategoriaGramatical(POS)/Numero",
    "PART": "Palabras/CategoriaGramatical(POS)/Particula",
    "PRON": "Palabras/CategoriaGramatical(POS)/Pronombre",
    "PROPN": "Palabras/CategoriaGramatical(POS)/NombrePropio",
    "SCONJ": "Palabras/CategoriaGramatical(POS)/Conjuncion_subordinante",
    "VERB": "Palabras/CategoriaGramatical(POS)/Verbo",
    "PUNCT": "Palabras/CategoriaGramatical(POS)/Puntuacion"
}

# Special URLs for specific symbols and words
special_symbols_urls = {
    ".": "Palabras\CategoriaGramatical(POS)/Puntuacion/Punto.JPG", ",": "Palabras/CategoriaGramatical(POS)/Puntuacion/Coma.JPG"}
special_word_urls = {
    "con": "Palabras/CategoriaGramatical(POS)/Preposicion/Con_.JPG"}

# Pre-existing numbers with available images
available_numbers = {
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
    10000, 100000, 1000000, 10000000, 100000000, 1000000000
}

# Desired image size
desired_size = (100, 100)

# Max images per row
max_images_per_row = 15

# Font settings
font = ImageFont.truetype("arial.ttf", 20)

# Log file for output
log_file_path = "log.txt"

# Open log file and redefine print function to log data
with open(log_file_path, 'w', encoding="utf-8") as log_file:
    # Redefinir la función de impresión para escribir en el archivo de registro
    def print_to_log(*args, **kwargs):
        print(*args, **kwargs)
        print(*args, **kwargs, file=log_file)

    # Process text with spaCy and apply matcher
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        # Correct POS tags for specific words
        if span.text.lower() in ["azul", "morado"]:
            span[0].pos_ = "ADJ"
        elif span.text.lower() in ["asomar", "bailar", "estar"]:
            span[0].pos_ = "VERB"
        else:
            span[0].pos_ = "NOUN"

    # Filter out tokens based on POS tags
    categorias = ["NOUN", "ADJ", "VERB", "ADP", "ADV", "AUX", "CCONJ",
                  "DET", "INTJ", "NUM", "PART", "PRON", "PROPN", "SCONJ", "X"]

    fraseCategoria = [[token, "NUM" if token.text.isdigit() else token.pos_]
                      for token in doc
                      if token.pos_ in categorias or token.pos_ == "PUNCT"]

    def get_correct_letter(letter):
        corrections = {
            'ñ': 'ñ',  # Include other characters if needed
            # Add more corrections if necessary
        }
        return corrections.get(letter, letter)  # Default to the letter itself if not found

    
    def get_word_image(word, pos_tag):
        # Convert word to lowercase depending on its type (Token or string)
        word_text = word.text.lower() if isinstance(
            word, spacy.tokens.token.Token) else word.lower()

        # Handle special characters and symbols
        word_text = get_correct_letter(word_text)

        # Return URL if word is in special_word_urls or special_symbols_urls
        if word_text in special_word_urls:
            return special_word_urls[word_text]
        elif word_text in special_symbols_urls:
            return special_symbols_urls[word_text]

        # Check if the POS tag is in words_dir and if the image exists
        word_image_path = os.path.join(
            words_dir.get(pos_tag, ""), f"{word}.jpg")
        if os.path.exists(word_image_path):
            return word_image_path

        # Return None if no match found
        return None

    def get_number_image(num):
        # Return the number if it's in available_numbers
        if num in available_numbers:
            return [num]

        components = []

        # Handle numbers >= 1,000,000
        if num >= 1000000:
            millions, remainder = divmod(num, 1000000)
            if millions > 1:
                # Decompose millions if greater than 1
                components.extend(get_number_image(millions))
            components.append(1000000)
            if remainder > 0:
                components.extend(get_number_image(remainder))
            return components

        # Handle numbers >= 1,000
        if num >= 1000:
            thousands, remainder = divmod(num, 1000)
            if thousands > 1:
                # Decompose thousands if greater than 1
                components.extend(get_number_image(thousands))
            components.append(1000)
            if remainder > 0:
                components.extend(get_number_image(remainder))
            return components

        # Handle numbers >= 100
        if num >= 100:
            hundreds, remainder = divmod(num, 100)
            components.append(hundreds * 100)
            if remainder > 0:
                components.extend(get_number_image(remainder))
            return components

        # Decompose numbers using available_numbers
        for n in sorted(available_numbers, reverse=True):
            while num >= n:
                components.append(n)
                num -= n

        return components

    # Create a dictionary to map letters to images
    letters_dir = "Letters"
    letter_to_image = {letter: os.path.join(
        letters_dir, f"{letter}.jpg") for letter in set(text)}
    
    # List to store images and spelled letters
    images_and_letters = []

    for frase in fraseCategoria:
        text, token_tag = frase  # Unpack the tuple for clarity
        
        # Handle NUM token
        if token_tag == "NUM":
            num_value = int(text.text)
            components = get_number_image(num_value)

            for component in components:
                component_image_path = get_word_image(str(component), "NUM")
                
                if component_image_path:
                    component_image = Image.open(component_image_path).resize(desired_size)

                    # Draw number on the image
                    draw = ImageDraw.Draw(component_image)
                    textbbox = draw.textbbox((0, 0), str(component), font=font)
                    text_x = (component_image.width - (textbbox[2] - textbbox[0])) / 2
                    text_y = component_image.height - (textbbox[3] - textbbox[1]) - 10
                    draw.text((text_x, text_y), str(component), font=font, fill="black")

                    images_and_letters.append(component_image)
                    print_to_log(f"[INFO] Generating image for component: {component}")
                else:
                    print_to_log(f"[INFO] No image generated for component: {component}")
            continue


        if token_tag == "PUNCT":
            punct_image_path = special_symbols_urls.get(text.text)
            
            if punct_image_path:
                
                if os.path.exists(punct_image_path):
                    punct_image = Image.open(punct_image_path).resize(desired_size)
                    
                    # Dibujar el signo de puntuación en la imagen
                    draw = ImageDraw.Draw(punct_image)
                    textbbox = draw.textbbox((0, 0), text.text, font=font)
                    text_x = (punct_image.width - (textbbox[2] - textbbox[0])) / 2
                    text_y = (punct_image.height - (textbbox[3] - textbbox[1]))/2
                    draw.text((text_x, text_y), text.text, font=font, fill="black")
                    print(text_x,text_y)
                    
                    images_and_letters.append(punct_image)
                    print_to_log(f"[INFO] Generating image for component: {text.text}")
                else:
                    print_to_log(f"[INFO] No image generated for component: {text.text}")
            else:
                print_to_log(f"[INFO] No image generated for component: {text.text}")
            continue  # Saltar al siguiente token si ya manejamos el signo de puntuación
    
        # Handle non-NUM tokens
        word_image_path = get_word_image(text, token_tag)
        print_to_log("=" * 10)
        print_to_log(frase, word_image_path)

        if word_image_path:
            # Load and resize word image if available
            word_image = Image.open(word_image_path).resize(desired_size)

            # Draw text on the image
            draw = ImageDraw.Draw(word_image)
            textbbox = draw.textbbox((0, 0), text.text, font=font)
            text_x = (word_image.width - (textbbox[2] - textbbox[0])) / 2
            text_y = word_image.height - (textbbox[3] - textbbox[1]) - 10
            draw.text((text_x, text_y), text.text, font=font, fill="black")

            images_and_letters.append(word_image)
            print_to_log(f"[INFO] Found image for word: {text} with tag: {token_tag}")
            print_to_log("=" * 10)
        else:
            # If no word image, process individual letters
            for letra in text.text:
                # Correct letter if necessary
                corrected_letra = get_correct_letter(letra)
                
                letter_image_path = letter_to_image.get(letra)

                if letter_image_path and os.path.exists(letter_image_path):
                    letter_image = Image.open(letter_image_path).resize(desired_size)
                    print_to_log(f"[INFO] Found image for letter: {letra}")
                else:
                    # Create a blank image if letter image not found
                    letter_image = Image.new('RGB', desired_size, (255, 255, 255))
                    print_to_log(f"[INFO] No image found for letter: {letra}")

                # Draw text on the letter image
                draw = ImageDraw.Draw(letter_image)
                textbbox = draw.textbbox((0, 0), letra, font=font)
                text_x = (letter_image.width - (textbbox[2] - textbbox[0])) / 2
                text_y = (letter_image.height - (textbbox[3] - textbbox[1])) -10
                draw.text((text_x, text_y), letra, font=font, fill="black")
                
                images_and_letters.append(letter_image)
                
            print_to_log("=" * 10)
            
    # Calculate the number of rows needed for the images and spelled letters
    num_rows_images = (len(images_and_letters) + max_images_per_row - 1) // max_images_per_row

    # Dimensions of the final image for the images and spelled letters
    image_width_images = desired_size[0] * max_images_per_row
    image_height_images = desired_size[1] * num_rows_images
    
    # Create a blank image for the final output
    final_image = Image.new('RGB', (image_width_images, image_height_images), (255, 255, 255))

    # Offsets to track horizontal and vertical positioning for the images and spelled letters
    x_offset_images, y_offset_images = 0, 0  # Start pasting images below the text

    # Paste the images and spelled letters into the final image
    for img in images_and_letters:
        final_image.paste(img, (x_offset_images, y_offset_images))

        # Update horizontal and vertical offsets
        x_offset_images += desired_size[0]
        if x_offset_images >= image_width_images:
            x_offset_images = 0
            y_offset_images += desired_size[1]

      # Size of the blank text box at the end (e.g., 100 px height)
    blank_text_box_height = 100

    # Adjust total height to include the blank text box at the end
    total_height_with_blank_box = image_height_images + blank_text_box_height

    # Create a new image for the final output with extra space for the blank box
    final_image_with_blank_box = Image.new(
        'RGB', (image_width_images, total_height_with_blank_box), (255, 255, 255))

    # Paste the final image containing the words and images onto the new image
    final_image_with_blank_box.paste(final_image, (0, 0))

    # Draw the blank text box (in this case, it's already blank, but you can add text if needed)
    draw = ImageDraw.Draw(final_image_with_blank_box)

    draw.text((10, image_height_images + 10), "Final phrase: " + final_phrase, font=font, fill="black")
    
    # Save and show the final combined image
    final_image_with_blank_box.save("Pruebas/classification.jpg")
    final_image_with_blank_box.show()
