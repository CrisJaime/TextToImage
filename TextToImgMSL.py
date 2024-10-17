from PIL import Image, ImageDraw, ImageFont
import os
from unidecode import unidecode
import spacy
from spacy.matcher import Matcher


# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")
# Crear un matcher para identificar las palabras específicas
matcher = Matcher(nlp.vocab)
patterns = [
    [{"LOWER": "asno"}],
    [{"LOWER": "calamar"}],
    [{"LOWER": "canguro"}],
    [{"LOWER": "pavo"}],
    [{"LOWER": "azul"}],
    [{"LOWER": "morado"}],
    [{"LOWER": "asomar"}],
    [{"LOWER": "bailar"}],
    [{"LOWER": "estar"}]
]
matcher.add("NOUNS_CORRECTION", patterns)

# Texto de entrada
text = "Tengo 27 años, mi hermana tiene 25 y mi padre tiene 55 años."

numImagen=9
# Directorio donde se encuentran las imágenes de las palabras
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
special_symbols_urls = {
    ".": "Palabras\CategoriaGramatical(POS)\Puntuacion\Punto.JPG",
    ",": "Palabras\CategoriaGramatical(POS)\Puntuacion\Coma.JPG",
}

# URL específica para la palabra "con"
special_word_urls = {
    "con": "Palabras/CategoriaGramatical(POS)/Preposicion/Con_.JPG"
}
# Lista de números preexistentes con imágenes disponibles
available_numbers = {
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
    10000, 100000, 1000000, 10000000, 100000000, 1000000000  # Agregando valores más grandes
}


# Tamaño deseado para las imágenes de las palabras
desired_size = (100, 100)

# Número máximo de imágenes por fila
max_images_per_row = 15

# Fuente para el texto
font_size = 18
font = ImageFont.truetype("arial.ttf", font_size)

# Archivo de registro para las impresiones
log_file_path = "log.txt"

# Abrir el archivo de registro
with open(log_file_path, 'w',encoding="utf-8") as log_file:
    # Redefinir la función de impresión para escribir en el archivo de registro
    def print_to_log(*args, **kwargs):
        print(*args, **kwargs)
        print(*args, **kwargs, file=log_file)

    # Procesar el texto con spaCy
    doc = nlp(text)
    # Aplicar el matcher para corregir etiquetas
    matches = matcher(doc)
    for match_id, start, end in matches:
            span = doc[start:end]
            if span.text.lower() in ["azul", "morado"]:
                span[0].pos_ = "ADJ"  # Corregir la etiqueta a ADJ para "azul"
            elif span.text.lower() in ["asomar","bailar","estar"]:
                span[0].pos_="VERB"
            else:
                span[0].pos_ = "NOUN"  # Corregir la etiqueta a NOUN para otros
        
    categorias = ["NOUN", "ADJ", "VERB", "ADP", "ADV", "AUX", "CCONJ",
                  "DET", "INTJ", "NUM", "PART", "PRON", "PROPN", "SCONJ", "X"]
    
    fraseCategoria = []
    for token in doc:
        if token.pos_ == "NOUN" and token.text.isdigit():
            token.pos_ = "NUM"  # Forzar que los números siempre sean etiquetados como NUM
        if token.pos_ in categorias  or token.pos_ == "PUNCT":
            fraseCategoria.append([token, token.pos_])
   
    
    def get_word_image(word, pos_tag):
        if isinstance(word, spacy.tokens.token.Token):
            word_text = word.text.lower()
        else:
            word_text = word.lower()  # Si ya es una cadena
            
        if word_text in special_word_urls:
            return special_word_urls[word_text]
        
        if word_text in special_symbols_urls:
            return special_symbols_urls[word_text]
        
        if pos_tag in words_dir:
            word_image_path = os.path.join(words_dir[pos_tag], f"{word}.jpg")
            if os.path.exists(word_image_path):
                return word_image_path
        return None
    
    def get_number_image(num):
        components=[]
        if num in available_numbers:
            return [num]
        
        # Descomposición especial para números grandes (millones)
        if num >= 1000000:
            millions = num // 1000000
            remainder = num % 1000000
            if millions > 1:
                components.extend(get_number_image(millions))  # Descomponer millones si es mayor a 1
            components.append(1000000)
            if remainder > 0:
                components.extend(get_number_image(remainder))
            return components
    
        # Descomposición especial para miles
        if num >= 1000:
            thousands = num // 1000
            remainder = num % 1000
            if thousands > 1:
                components.extend(get_number_image(thousands))  # Aquí se descompone el número de miles (por ejemplo, 102 en 100 + 2)
            components.append(1000)
            if remainder > 0:
                components.extend(get_number_image(remainder))
            return components
        
        # Manejo de centenas (100 a 999)
        if num >= 100:
            hundreds = num // 100 * 100
            remainder = num % 100
            components.append(hundreds)
            if remainder > 0:
                components.extend(get_number_image(remainder))
            return components
    
        for n in sorted(available_numbers, reverse=True):
            while num >= n:
                components.append(n)
                num -= n
        return components

    # Crear un diccionario para asignar letras a imágenes
    letters_dir = "Letters"
    letter_to_image = {letter: os.path.join(
        letters_dir, f"{letter}.jpg") for letter in set(unidecode(text))}

    # Lista para almacenar las imágenes y las letras deletreadas
    images_and_letters = []

    for frase in fraseCategoria:
        text = frase[0]
        token_tag = frase[1]
        
        if token_tag == "NUM":
            num_value = int(text.text)
            components = get_number_image(num_value)
            for component in components:
                component_image_path = get_word_image(str(component), "NUM")
                if component_image_path:
                    component_image = Image.open(component_image_path)
                    component_image = component_image.resize(desired_size)
                    
                    # Dibujar el número en la imagen
                    draw = ImageDraw.Draw(component_image)
                    textbbox = draw.textbbox((0, 0), str(component), font=font)
                    text_width = textbbox[2] - textbbox[0]
                    text_height = textbbox[3] - textbbox[1]
                    text_x = (component_image.width - text_width) / 2
                    text_y = component_image.height - text_height - 10
                    draw.text((text_x, text_y), str(component), font=font, fill="black")
                    
                    images_and_letters.append(component_image)
                    print_to_log(f"[INFO] Generando imagen para el componente: {component}")
                else:
                    print_to_log(f"[INFO] No se genero imagen para el componente: {component}")
            continue
        
        
        word_image_path = get_word_image(text, token_tag)
        print_to_log("==="*10)
        print_to_log(frase, word_image_path)
        
        if word_image_path:
            # Si hay imagen disponible, cargarla y ajustarla
            word_image = Image.open(word_image_path)
            word_image = word_image.resize(desired_size)

            draw = ImageDraw.Draw(word_image)
            textbbox = draw.textbbox((0, 0), text.text, font=font)
            text_width = textbbox[2] - textbbox[0]
            text_height = textbbox[3] - textbbox[1]
            text_x = (word_image.width - text_width) / 2
            text_y = word_image.height - text_height - 10
            draw.text((text_x, text_y), text.text, font=font, fill="black")

            images_and_letters.append(word_image)
            
            print_to_log(
                f"[INFO] Se encontró imagen para la palabra: {text} con etiqueta: {token_tag}")
            print_to_log("==="*10)
            
        else:
            print_to_log(
                f"[INFO] No se encontró imagen para la palabra: {text} con etiqueta: {token_tag}")
            convertText = text.text
            for letra in convertText:
                plain_letter = unidecode(letra)
                if plain_letter in letter_to_image and os.path.exists(letter_to_image[plain_letter]):
                    letter_image = Image.open(letter_to_image[plain_letter])
                    # Redimensionar la imagen de la letra
                    letter_image = letter_image.resize(desired_size)

                    draw = ImageDraw.Draw(letter_image)
                    textbbox = draw.textbbox((0, 0), letra, font=font)
                    text_width = textbbox[2] - textbbox[0]
                    text_height = textbbox[3] - textbbox[1]
                    text_x = (letter_image.width - text_width) / 2
                    # Ajustar la posición vertical según sea necesario
                    text_y = letter_image.height - text_height - 10
                    draw.text((text_x, text_y), letra, font=font, fill="black")

                    images_and_letters.append(letter_image)
                    print_to_log(f"[INFO] Se encontró imagen para la letra: {letra}")
                else:
                    letter_image = Image.new('RGB', desired_size, (255, 255, 255))

                    draw = ImageDraw.Draw(letter_image)
                    textbbox = draw.textbbox((0, 0), letra, font=font)
                    text_width = textbbox[2] - textbbox[0]
                    text_height = textbbox[3] - textbbox[1]
                    text_x = (letter_image.width - text_width) / 2
                    text_y = (letter_image.height - text_height) / 2
                    draw.text((text_x, text_y), letra, font=font, fill="black")

                    images_and_letters.append(letter_image)

                    print_to_log(f"[INFO] No se encontró imagen para : {letra}")
            print_to_log("==="*10)

    # Calcular el número de filas necesarias para las imágenes y las letras deletreadas
    num_rows_images = (len(images_and_letters) +
                       max_images_per_row - 1) // max_images_per_row

    # Dimensiones de la imagen final para las imágenes y las letras deletreadas
    image_width_images = desired_size[0] * max_images_per_row
    image_height_images = desired_size[1] * num_rows_images

    # Crear una imagen en blanco para la imagen final
    final_image = Image.new(
        'RGB', (image_width_images, image_height_images), (255, 255, 255))

    # Variables para mantener el desplazamiento horizontal y vertical para las imágenes y las letras deletreadas
    x_offset_images = 0
    y_offset_images = 0

    # Pegar las imágenes y las letras deletreadas en la imagen final
    for img in images_and_letters:
        final_image.paste(img, (x_offset_images, y_offset_images))

        x_offset_images += desired_size[0]
        if x_offset_images >= image_width_images:
            x_offset_images = 0
            y_offset_images += desired_size[1]

    # Guardar la imagen final combinada
    # final_image.save("Pruebas\output_TextToIMG_500cha_{}.jpg".format(numImagen))
    final_image.save("Pruebas\classification.jpg")
    final_image.show()
