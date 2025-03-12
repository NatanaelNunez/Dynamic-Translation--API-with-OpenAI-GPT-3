# API de Traducción Dinámica con OpenAI GPT-3
# Dynamic Translation API with OpenAI GPT-3

> Traducción dinámica e incremental para contenido en tiempo real  
> Dynamic and incremental translation for real-time content

## 🌍 Descripción | Description

**Español:**  
API diseñada para ofrecer traducciones dinámicas e incrementales utilizando la inteligencia artificial de OpenAI GPT-3. Permite traducir texto de manera continua por sesión, y también ofrece la opción de traducir textos completos una vez que se marca como finalizado.

**English:**  
API designed to provide dynamic and incremental translations using OpenAI GPT-3 AI. It allows translating text continuously per session, and also offers the option to translate complete texts once marked as finished.

## ✨ Beneficios | Benefits

### Traducción Incremental | Incremental Translation
- **ES:** Traducción continua de fragmentos de texto mientras el contenido se genera. Ideal para contenido en tiempo real.
- **EN:** Continuous translation of text fragments as content is generated. Ideal for real-time content.

### Traducción Completa | Complete Translation
- **ES:** Opción de traducir un texto completo cuando se marca como finalizado, útil para contenidos largos.
- **EN:** Option to translate a complete text once marked as finished, useful for longer content.

### Personalización | Customization
- **ES:** Posibilidad de ajustar el idioma de la traducción y el género (femenino o masculino), lo que permite una traducción más adaptada a las necesidades del proyecto.
- **EN:** Ability to adjust the translation language and gender (female or male), making it more tailored to the project's needs.

### Memoria Eficiente | Efficient Memory
- **ES:** Guarda el historial de traducción por sesión, lo que permite mantener el contexto y gestionar las traducciones previas.
- **EN:** Stores the translation history by session, allowing context to be maintained and previous translations to be managed.

### Flexibilidad y Modularidad | Flexibility and Modularity
- **ES:** Completamente modular y fácil de integrar en otros proyectos, ideal para desarrolladores que buscan soluciones rápidas y efectivas.
- **EN:** Fully modular and easy to integrate into other projects, ideal for developers looking for quick and effective solutions.

## 🚀 Instalación | Installation

1. **Clona este repositorio | Clone this repository:**
   ```bash
   git clone https://github.com/NatanaelNunez/Dynamic-Translation--API-with-OpenAI-GPT-3
   ```

2. **Instala las dependencias | Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la clave API de OpenAI | Configure your OpenAI API key:**
   ![image](https://github.com/user-attachments/assets/f9287b38-db09-40ea-aeb6-3e438f20eac1)

   - **ES:** Asegúrate de tener una cuenta en OpenAI y obtener tu clave API. Luego, reemplaza la clave en el script `app.py`.
   - **EN:** Make sure you have an OpenAI account and get your API key. Then, replace the key in the `app.py` script.

4. **Start API**
   python app.py


## 📝 Uso | Usage

### Endpoint: `/api/translator`
- **Método | Method:** POST
- **URL:** `/api/translator`

### Parámetros | Parameters
| Parámetro/Parameter | Tipo/Type | Descripción/Description | Valor predeterminado/Default |
|-----------|------|-------------|---------------------|
| text | str | ES: El texto a traducir<br>EN: The text to translate | - |
| target_lang | str | ES: El idioma de destino<br>EN: The target language | "Spanish" |
| session_id | str | ES: Identificador único para la sesión<br>EN: A unique identifier for the session | - |
| is_complete | bool | ES: Marca si el diálogo ha finalizado<br>EN: Marks if the dialogue has finished | False |
| force_complete | bool | ES: Fuerza la traducción completa<br>EN: Forces complete translation | False |
| reset | bool | ES: Reinicia el historial de traducción<br>EN: Resets the translation history | False |

### Ejemplos de Uso | Usage Examples

#### Traducción de Español a Inglés | Spanish to English Translation
```python
import requests
import json

url = "http://localhost:5000/api/translator"

# Datos para traducir de español a inglés | Data to translate from Spanish to English
data = {
    "text": "Hola, ¿cómo estás hoy? Espero que todo vaya bien con tu proyecto.",
    "target_lang": "English",
    "session_id": "session_example",
    "is_complete": False
}

response = requests.post(url, json=data)
result = response.json()

print(result)
# Salida/Output: {"result": "Hello, how are you today? I hope everything is going well with your project."}
```

#### Traducción de Inglés a Español | English to Spanish Translation
```python
import requests
import json

url = "http://localhost:5000/api/translator"

# Datos para traducir de inglés a español | Data to translate from English to Spanish
data = {
    "text": "Hello, how are you?",
    "target_lang": "Spanish",
    "session_id": "session_1",
    "is_complete": False
}

response = requests.post(url, json=data)
result = response.json()

print(result)
# Salida/Output: {"result": "Hola, ¿cómo estás?"}
```

## ⚙️ Cómo Funciona | How it Works

1. **Traducción Incremental | Incremental Translation:**
   - **ES:** Cuando se envía un fragmento de texto, la API lo acumula y lo traduce progresivamente. Si el texto ya fue traducido previamente, solo se traduce el nuevo fragmento.
   - **EN:** When a text fragment is sent, the API accumulates and translates it progressively. If the text has been previously translated, only the new fragment is translated.

2. **Traducción Completa | Complete Translation:**
   - **ES:** Cuando se marca un diálogo como completo, la API traduce todo el texto acumulado y devuelve la traducción final.
   - **EN:** When a dialogue is marked as complete, the API translates all the accumulated text and returns the final translation.

3. **Personalización | Customization:**
   - **ES:** Puedes elegir el idioma y el género de la traducción según las necesidades de tu proyecto.
   - **EN:** You can choose the language and gender of the translation according to your project's needs.



## 💻 Ejemplos | Examples and Configuration

**MORT:**

**Documentación oficial | Official documentation:** [https://github.com/killkimno/MORT/blob/main/README.md](https://github.com/killkimno/MORT/blob/main/README.md)

**ES:** He creado un video demostrativo que muestra cómo funciona la API en proyectos como Mort. [Ver demostración](https://tu-link-de-demo.com)

**EN:** I've created a demo video showing how the API works in projects like Mort. [Watch demo](https://your-demo-link.com)

**ES:** proyecto MORT, puedes consultar:
**EN:** MORT project , you can consult:

- **Blog de ejemplos | Examples blog:** [https://blog.naver.com/killkimno/221760617100](https://blog.naver.com/killkimno/221760617100) 



------------------------------------



## 🤝 Contribuciones | Contributions

**ES:** Si deseas contribuir a este proyecto, siéntete libre de abrir un pull request.

**EN:** If you want to contribute to this project, feel free to open a pull request.

## 📄 Licencia | License

**ES:** Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

**EN:** This project is licensed under the [MIT License](LICENSE).
