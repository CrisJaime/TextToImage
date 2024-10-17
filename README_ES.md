# Generación de Imágenes Basadas en Texto con spaCy y PIL

Este proyecto utiliza `spaCy` y `PIL` para procesar texto en español, identificar palabras clave y generar imágenes basadas en las palabras, números y caracteres especiales encontrados. El objetivo es permitir la visualización de texto como imágenes, lo que resulta útil en contextos educativos, sistemas de accesibilidad y otras aplicaciones que requieran la conversión de texto a gráficos.

## ¿Qué hace este proyecto?

Este script toma como entrada un texto, lo analiza utilizando procesamiento del lenguaje natural (NLP) y produce una imagen combinada que representa las palabras y números detectados. El proyecto:

- Identifica sustantivos, verbos, adjetivos y otras categorías gramaticales.
- Genera imágenes específicas para palabras y números basándose en etiquetas de categorías gramaticales (POS).
- Crea una imagen final que combina las imágenes de palabras y caracteres presentes en el texto.
- Adapta imágenes preexistentes para cada palabra o crea imágenes de letras si no se encuentra una imagen específica.

## ¿Por qué es útil este proyecto?

Este proyecto es útil para diversas aplicaciones como:

- **Educación**: Ayuda a visualizar palabras y frases en español, lo que puede mejorar la comprensión del lenguaje para estudiantes o personas con necesidades especiales.
- **Accesibilidad**: Proporciona una forma gráfica de representar texto, útil para sistemas que transforman texto en imágenes para usuarios con discapacidades visuales o de aprendizaje.
- **Análisis de texto**: Es una herramienta flexible para mostrar visualmente las palabras en un texto y su análisis gramatical, útil en proyectos de investigación o análisis de datos.

## Cómo comenzar con el proyecto

### Requisitos previos

Antes de empezar, asegúrate de tener instalado lo siguiente:

- Python 3.x
- [spaCy](https://spacy.io/) para procesamiento de lenguaje natural.
- [Pillow (PIL)](https://python-pillow.org/) para la manipulación de imágenes.
- [unidecode](https://pypi.org/project/Unidecode/) para la normalización de texto.
  
### Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/tu-repositorio.git
2. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
3. Descarga el modelo de `spaCy` en español:
    ```bash 
    python -m spacy download es_core_news_sm
4. Asegúrate de tener las imágenes de palabras y letras organizadas en las carpetas correspondientes (Palabras/ y Letters/).

## Ejecución del Proyecto
1. Modifica el texto de entrada en el archivo Python por cualquier frase que quieras utilizar:
    ```python 
    text = "Tengo 27 años, mi hermana tiene 25 y mi padre tiene 55 años"
2. Ejecuta el script para procesar el texto y generar la imagen final:
    ```bash
    python TextToImgMSL_1.0.0.py
3. La imagen generada estará disponible en la carpeta `Pruebas\` con el nombre de `classification.jpg`

## Etiquetas POS(Partes del Discurso)

El proyecto utiliza las etiquetas de categorías gramaticales (POS, por sus siglas en inglés) generadas por el modelo de `spaCy` y para identificar diferentes tipos de palabras en el texto. Aquí están las etiquetas principales utilizadas en el script y lo que representan:

- **ADJ (Adjetivo)**: Palabras que describen características o cualidades de sustantivos, como colores o tamaños (por ejemplo: *azul, grande*).
- **ADP (Preposición)**: Palabras que indican relaciones entre otras palabras, como *con, sin o en*.
- **ADV (Adverbio)**: Palabras que modifican verbos, adjetivos u otros adverbios, indicando cómo se realiza una acción (por ejemplo: *rápidamente*).
- **AUX (Verbo Auxiliar)**: Verbos que acompañan a otros verbos para formar tiempos verbales compuestos (por ejemplo: *haber, ser*).
- **CCONJ (Conjunción de Coordinación)**: Palabras que conectan frases o cláusulas de igual importancia, como *y, o*.
- **DET (Determinante)**: Palabras que introducen sustantivos y expresan cantidad o posesión, como *el, la, un, mi*.
- **INTJ (Interjección)**: Palabras o frases cortas que expresan emociones o reacciones, como *¡ay!, ¡oh!*.
- **NOUN (Sustantivo)**: Palabras que nombran personas, animales, cosas o ideas (por ejemplo: *niño, libro*).
- **NUM (Número**): Números cardinales, como *uno, dos, 27*.
- **PART (Partícula)**: Palabras funcionales que no encajan fácilmente en otras categorías gramaticales y que modifican o aclaran (por ejemplo: *no* en no hacer).
- **PRON (Pronombre)**: Palabras que sustituyen a los nombres, como *él, ella, nosotros*.
- **PROPN (Nombre Propio)**: Nombres específicos de personas, lugares o instituciones (por ejemplo: *Juan, México*).
- **SCONJ (Conjunción Subordinante)**: Palabras que introducen cláusulas subordinadas, como *porque, aunque*.
- **PUNCT (Puntuación)**: Caracteres de puntuación como *. (punto) o , (coma)*.

Estas etiquetas permiten que el script identifique las palabras en el texto y determine qué imagen o letra utilizar para visualizarlas.

### Imágenes por Categoría POS

En esta versión del proyecto, hay **893 palabras** clasificadas y asociadas con imágenes, distribuidas de la siguiente manera:

- **ADJ (Adjetivo)**: 194 imágenes
- **ADP (Preposición)**: 10 imágenes
- **ADV (Adverbio)**: 34 imágenes
- **AUX (Verbo Auxiliar)**: 3 imágenes
- **CCONJ (Conjunción de Coordinación)**: 3 imágenes
- **DET (Determinante)**: 14 imágenes
- **INTJ (Interjección)**: 4 imágenes
- **NOUN (Sustantivo)**: 358 imágenes
- **NUM (Número)**: 39 imágenes
- **PRON (Pronombre)**: 15 imágenes
- **PROPN (Nombre Propio)**: 21 imágenes
- **VERB (Verbo)**: 198 imágenes

### Palabra Especial con URL Específica
Una palabra especial en este proyecto es la palabra **"con"**. Esta palabra está asociada a una URL específica, que la ubica dentro de la categoría de preposiciones. La URL es la siguiente: 
`Palabras/CategoriaGramatical(POS)/Preposicion/Con_.JPG`

La palabra **"con"** es una palabra reservada de Windows que se refiere a la palabra `Console`.

### Categorías no Utilizadas
- **PART (Partícula)**: Esta categoría no se utiliza en el proyecto actual ya que no hay palabras que encajen en esta etiqueta. En futuras versiones, se podrían incluir partículas específicas que cumplan esta función.

### Palabras Agregadas a través de Patterns

Algunas palabras en el texto pueden haber sido clasificadas de manera incorrecta por el modelo de `spaCy`. Para corregir esto, se han agregado **palabras en los patrones** (patterns) utilizando la función `matcher`. Esta funcionalidad permite redefinir la clasificación de palabras que no encajan perfectamente en una categoría gramatical estándar o que requieren un tratamiento personalizado dentro del flujo del programa.

Por ejemplo, si una palabra es etiquetada erróneamente como un sustantivo cuando debería ser un verbo, la función `matcher` puede corregir este error para garantizar que el procesamiento del texto sea lo más preciso posible.

## Fuente de las Imágenes

Las imágenes utilizadas en esta versión del proyecto fueron obtenidas del documento titulado:

- **Manos con Voz: Diccionario de Lengua de Señas Mexicana**  
    - Autor: **Consejo Nacional para Prevenir la Discriminación (CONAPRED)**  
    - URL: [https://www.conapred.org.mx/wp-content/uploads/2022/07/ManosconVoz_2011_Ax.pdf](https://www.conapred.org.mx/wp-content/uploads/2022/07/ManosconVoz_2011_Ax.pdf)

    Este diccionario contiene un extenso catálogo visual de señas en Lengua de Señas Mexicana (LSM), el cual ha sido fundamental para la generación de las imágenes asociadas a las palabras y etiquetas gramaticales (POS) en este proyecto.
