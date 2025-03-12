from flask import Flask, request, jsonify
import openai
import logging
import re

# Initialize the Flask application
app = Flask(__name__)
# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# OpenAI API key (replace with your own key)
openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Dictionaries to store original texts and translations by session
original_texts = {}  # Historial de texto original por sesión
complete_translations = {}  # Traducciones completas por sesión
dialogue_complete = {}  # Indicador de finalización de diálogo por sesión

@app.route('/api/translator', methods=['POST'])
def translate_api():
    global original_texts, complete_translations, dialogue_complete
    # Log request received
    app.logger.debug("Solicitud recibida en /api/translator")  # Log the request

    # Check if the request is in JSON format
    if request.is_json:
        data = request.get_json()  # Get the JSON data from the request
        text_to_translate = data.get('text', '')  # Texto a traducir
        target_language = data.get('target_lang', 'Spanish')  # Target language (default is "Spanish")
        session_id = data.get('session_id', 'default')  # Session ID
        is_complete = data.get('is_complete', False)  # Flag to mark if the dialogue is complete
        force_complete = data.get('force_complete', False)  # Flag to force full translation
        reset = data.get('reset', False)  # Flag to reset history
        
        # Log the values obtained from the request
        app.logger.debug(f"Texto a traducir: '{text_to_translate}'")  # Log text to translate
        app.logger.debug(f"¿Diálogo completo?: {is_complete}")  # Log if dialogue is complete
    else:
        return jsonify({"error": "Se esperaba formato JSON"}), 400  # Return error if not in JSON format
    
    # Initialize history if it doesn't exist
    if session_id not in original_texts:
        original_texts[session_id] = ""
        complete_translations[session_id] = ""
        dialogue_complete[session_id] = False
    
    # If reset is requested, clear the history
    if reset:
        original_texts[session_id] = ""
        complete_translations[session_id] = ""
        dialogue_complete[session_id] = False
        return jsonify({"result": ""})  # Return an empty result
    
    # If the dialogue is marked as complete
    if is_complete:
        dialogue_complete[session_id] = True  # Mark as complete
        
        # If we already have a complete translation, return it
        if complete_translations[session_id]:
            return jsonify({"result": complete_translations[session_id]})
            
        # If we don't have a complete translation but we have the original text, proceed to translate everything
        if original_texts[session_id]:
            try:
                complete_translation = translate_text_gpt(original_texts[session_id], target_language)
                if complete_translation:
                    complete_translations[session_id] = complete_translation
                    return jsonify({"result": complete_translation})  # Return the full translation
            except Exception as e:
                app.logger.error(f"Error traduciendo texto completo: {str(e)}")  # Log error in translation
                return jsonify({"result": complete_translations[session_id] or "Error en la traducción"}), 500
    
    # If no text to translate
    if not text_to_translate:
        # If the dialogue is complete, return the full translation
        if dialogue_complete[session_id] and complete_translations[session_id]:
            return jsonify({"result": complete_translations[session_id]})
        return jsonify({"error": "No hay texto para traducir"}), 400  # Error if no text to translate
    
    try:
        # Check if the text is a new fragment or a repeat
        is_new_fragment = not text_to_translate.strip() in original_texts[session_id]
        
        # Only accumulate the text if it's a new fragment
        if is_new_fragment:
            # Process the text to avoid partial duplications
            if original_texts[session_id] and text_to_translate.startswith(original_texts[session_id]):
                # If the new text starts where the previous one ended, add only the new part
                additional_text = text_to_translate[len(original_texts[session_id]):]
                original_texts[session_id] += additional_text
            else:
                # If no match, add the entire text
                original_texts[session_id] = text_to_translate
        
        # If requested to force a full translation or the dialogue is marked as complete
        if force_complete or dialogue_complete[session_id]:
            complete_translation = translate_text_gpt(original_texts[session_id], target_language)
            if complete_translation:
                complete_translations[session_id] = complete_translation
                return jsonify({"result": complete_translation})
        
        # For incremental translation
        translated_text = translate_text_gpt(text_to_translate, target_language)
        if not translated_text:
            app.logger.warning("La traducción ha fallado o está vacía.")  # Log warning if translation failed
            # If we have a full translation, use it as a fallback
            if complete_translations[session_id]:
                return jsonify({"result": complete_translations[session_id]})
            return jsonify({"error": "Error en la traducción"}), 500
        
        # Update the complete translation if the new translation is longer
        if len(translated_text) > len(complete_translations[session_id]):
            complete_translations[session_id] = translated_text
        
        # Return the translated text
        return jsonify({"result": translated_text})
    except Exception as e:
        app.logger.error(f"Error en el proceso de traducción: {str(e)}")  # Log error in translation process
        # If we have a complete translation, use it as a fallback
        if complete_translations[session_id]:
            return jsonify({"result": complete_translations[session_id]})
        return jsonify({"error": f"Error en la traducción: {str(e)}"}), 500  # Return error if translation failed

# Function to translate text using OpenAI GPT
def translate_text_gpt(text, target_language):
    try:
        # Using the old syntax of the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Model used for translation
            messages=[ 
                {"role": "system", "content": "Eres un asistente útil."},  # System message to set context
                {"role": "user", "content": f"Traduce el siguiente texto a {target_language} y pon todo en femenino: {text.strip()}"}  # User message to translate
            ],
            temperature=0.5,  # Adjust the temperature for randomness
        )
        
        # Accessing the translation from the response
        translated_text = response['choices'][0]['message']['content'].strip()
        
        # Log the complete response for inspection
        app.logger.debug(f"Respuesta de OpenAI: {translated_text}")
        
        # Check if the response is empty
        if not translated_text:
            app.logger.warning("La respuesta de GPT está vacía.")  # Log if the response is empty
        return translated_text
    except Exception as e:
        app.logger.error(f"Error durante la traducción: {e}")  # Log error during translation
        return None

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Run the app
