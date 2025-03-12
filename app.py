from flask import Flask, request, jsonify
import openai
import logging
import re

# V 1.0.0
# https://github.com/NatanaelNunez/Dynamic-Translation--API-with-OpenAI-GPT-3

# Initialize Flask app / Inicializa la aplicación Flask
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Set OpenAI API key / Establece la clave API de OpenAI
openai.api_key = "your OpenAI API key"

# Original texts history per session / Historial de textos originales por sesión
original_texts = {}
# Full translations per session / Traducciones completas por sesión
complete_translations = {}
# Dialogue completion status per session / Indicador de diálogo completo por sesión
dialogue_complete = {}

@app.route('/api/translator', methods=['POST'])
def translate_api():
      """
    This function handles incoming requests to translate text and store session information. / 
    Esta función maneja las solicitudes entrantes para traducir texto y almacenar la información de la sesión.

    Parameters: 
    -----------
    None

    Returns:
    --------
    dict:
        JSON containing translated text or an error message. /
        JSON que contiene el texto traducido o un mensaje de error.
    """
    global original_texts, complete_translations, dialogue_complete
    app.logger.debug("Solicitud recibida en /api/translator")  # Request received at /api/translator / Solicitud recibida en /api/translator
    
   if request.is_json:  # Check if the request is JSON / Verifica si la solicitud es JSON
        data = request.get_json()  # Get the JSON data from the request / Obtiene los datos JSON de la solicitud
        text_to_translate = data.get('text', '')  # Get the text to translate / Obtiene el texto a traducir
        target_language = data.get('target_lang', 'Spanish')  # Get the target language / Obtiene el idioma objetivo
        session_id = data.get('session_id', 'default')  # Get the session ID / Obtiene el ID de la sesión
        is_complete = data.get('is_complete', False)  # Check if it's a complete dialogue / Verifica si es un diálogo completo
        force_complete = data.get('force_complete', False)  # Force completion of the translation / Forzar la finalización de la traducción
        reset = data.get('reset', False)  # Check if reset is requested / Verifica si se solicita reiniciar
        
        
        app.logger.debug(f"Text to translate: '{text_to_translate}'")  # Log the text to translate / Registrar el texto a traducir
        app.logger.debug(f"Is the dialogue complete?: {is_complete}")  # Log if the dialogue is complete / Registrar si el diálogo está completo
    else:
        return jsonify({"error": "Expected JSON format"}), 400  # Return an error if not JSON / Devuelve un error si no es JSON
    
     # Initialize session data if it doesn't exist / Inicializa los datos de la sesión si no existen
    if session_id not in original_texts:
        original_texts[session_id] = ""  # Initialize original texts for the session / Inicializa los textos originales para la sesión
        complete_translations[session_id] = ""  # Initialize complete translations for the session / Inicializa las traducciones completas para la sesión
        dialogue_complete[session_id] = False  # Initialize dialogue completion status / Inicializa el estado de completitud del diálogo
    
     # Handle reset request / Maneja la solicitud de reinicio
    if reset:
        original_texts[session_id] = ""  # Clear original text / Borra el texto original
        complete_translations[session_id] = ""  # Clear complete translation / Borra la traducción completa
        dialogue_complete[session_id] = False  # Reset dialogue completion status / Reinicia el estado de completitud del diálogo
        return jsonify({"result": ""})  # Return an empty result / Devuelve un resultado vacío
    
     # Handle full translation request / Maneja la solicitud de traducción completa
    if is_complete:
        dialogue_complete[session_id] = True  # Mark the dialogue as complete / Marca el diálogo como completo
        
        if complete_translations[session_id]:
            return jsonify({"result": complete_translations[session_id]})  # Return the complete translation / Devuelve la traducción completa
            
        if original_texts[session_id]:
            try:
                complete_translation = translate_text_gpt(original_texts[session_id], target_language)  # Get complete translation from GPT / Obtiene la traducción completa desde GPT
                if complete_translation:
                    complete_translations[session_id] = complete_translation  # Store the complete translation / Almacena la traducción completa
                    return jsonify({"result": complete_translation})  # Return the complete translation / Devuelve la traducción completa
            except Exception as e:
                app.logger.error(f"Error translating complete text: {str(e)}")  # Log error if translation fails / Registra el error si la traducción falla
                return jsonify({"result": complete_translations[session_id] or "Error in translation"}), 500  # Return error or previous translation / Devuelve el error o la traducción previa
    
    # Handle case where no text to translate / Maneja el caso sin texto para traducir
    if not text_to_translate:
        if dialogue_complete[session_id] and complete_translations[session_id]:
            return jsonify({"result": complete_translations[session_id]})  # Return the full translation if available / Devuelve la traducción completa si está disponible
        return jsonify({"error": "No text to translate"}), 400  # Return an error if no text is provided / Devuelve un error si no se proporciona texto
    
     try:
        is_new_fragment = not text_to_translate.strip() in original_texts[session_id]  # Check if this is a new fragment / Verifica si este es un nuevo fragmento
        
        if is_new_fragment:
            if original_texts[session_id] and text_to_translate.startswith(original_texts[session_id]):
                additional_text = text_to_translate[len(original_texts[session_id]):]  # Get additional text to append / Obtiene el texto adicional para agregar
                original_texts[session_id] += additional_text  # Append additional text / Agrega el texto adicional
            else:
                original_texts[session_id] = text_to_translate  # Set the original text for the session / Establece el texto original para la sesión
        
        if force_complete or dialogue_complete[session_id]:
            complete_translation = translate_text_gpt(original_texts[session_id], target_language)  # Get complete translation if requested / Obtiene la traducción completa si se solicita
            if complete_translation:
                complete_translations[session_id] = complete_translation  # Store the complete translation / Almacena la traducción completa
                return jsonify({"result": complete_translation})  # Return the complete translation / Devuelve la traducción completa
        
        translated_text = translate_text_gpt(text_to_translate, target_language)  # Get translation for the current fragment / Obtiene la traducción para el fragmento actual
        if not translated_text:
            app.logger.warning("Translation failed or is empty.")  # Log warning if translation fails / Registra una advertencia si la traducción falla
            if complete_translations[session_id]:
                return jsonify({"result": complete_translations[session_id]})  # Return complete translation if available / Devuelve la traducción completa si está disponible
            return jsonify({"error": "Error in translation"}), 500  # Return an error if no translation / Devuelve un error si no hay traducción
        
        if len(translated_text) > len(complete_translations[session_id]):
            complete_translations[session_id] = translated_text  # Store the updated translation / Almacena la traducción actualizada
        
        return jsonify({"result": translated_text})  # Return the translated text / Devuelve el texto traducido
    except Exception as e:
        app.logger.error(f"Error during translation process: {str(e)}")  # Log any error during the translation process / Registra cualquier error durante el proceso de traducción
        if complete_translations[session_id]:
            return jsonify({"result": complete_translations[session_id]})  # Return the complete translation if available / Devuelve la traducción completa si está disponible
        return jsonify({"error": f"Error in translation: {str(e)}"}), 500  # Return error if translation fails / Devuelve un error si la traducción falla

def translate_text_gpt(text, target_language):
    """
    Function to translate text using GPT from OpenAI. / 
    Función para traducir texto utilizando GPT de OpenAI.

    Parameters:
    -----------
    text : str / texto : str
        The text to be translated. / El texto que se va a traducir.
    
    target_language : str / idioma_objetivo : str
        The target language for the translation. / El idioma objetivo de la traducción.

    Returns:
    --------
    str: / str:
        The translated text. / El texto traducido.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Set the GPT engine / Establece el motor GPT
            prompt=f"Translate the following text to {target_language}: {text}",  # Translation prompt / Indicación para la traducción
            max_tokens=1024,  # Max tokens for the response / Máximo de tokens para la respuesta
            n=1,  # Number of responses to generate / Número de respuestas a generar
            stop=None,  # Stop sequence for completion / Secuencia de parada para la completación
            temperature=0.7  # Temperature setting for creativity / Configuración de temperatura para creatividad
        )
        translated_text = response.choices[0].text.strip()  # Get the translated text from response / Obtiene el texto traducido de la respuesta
        return translated_text  # Return the translated text / Devuelve el texto traducido
    except Exception as e:
        raise Exception(f"Error during translation API call: {str(e)}")  # Log and raise error if API call fails / Registra y lanza error si la llamada a la API falla
