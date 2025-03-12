# GPT-3-Translation-API-for-Projects-like
GPT-3 Translation API for Projects like Mort

# Mort - API de Traducción Dinámica con OpenAI GPT-3

<p align="center">
  <img src="/api/placeholder/400/200" alt="Mort Logo" />
</p>

> Traducción dinámica e incremental para contenido en tiempo real

## 🌍 Descripción

Mort es una API diseñada para ofrecer traducciones dinámicas e incrementales utilizando la inteligencia artificial de OpenAI GPT-3. Permite traducir texto de manera continua por sesión, y también ofrece la opción de traducir textos completos una vez que se marca como finalizado.

## ✨ Beneficios

### Traducción Incremental
- Traducción continua de fragmentos de texto mientras el contenido se genera
- Ideal para contenido en tiempo real

### Traducción Completa
- Opción de traducir un texto completo cuando se marca como finalizado
- Útil para contenidos largos

### Personalización
- Posibilidad de ajustar el idioma de la traducción
- Opciones de género (femenino o masculino)
- Traducciones más adaptadas a las necesidades del proyecto

### Memoria Eficiente
- Guarda el historial de traducción por sesión
- Mantiene el contexto y gestiona las traducciones previas

### Flexibilidad y Modularidad
- Completamente modular y fácil de integrar en otros proyectos
- Ideal para desarrolladores que buscan soluciones rápidas y efectivas

## 🚀 Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/miusuario/Mort
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la clave API de OpenAI:**
   - Asegúrate de tener una cuenta en OpenAI y obtener tu clave API
   - Reemplaza la clave en el script `app.py`

## 📝 Uso

### Endpoint: `/api/translator`
- **Método:** POST
- **URL:** `/api/translator`

### Parámetros
| Parámetro | Tipo | Descripción | Valor predeterminado |
|-----------|------|-------------|---------------------|
| text | str | El texto a traducir | - |
| target_lang | str | El idioma de destino | "Spanish" |
| session_id | str | Identificador único para la sesión | - |
| is_complete | bool | Marca si el diálogo ha finalizado | False |
| force_complete | bool | Fuerza la traducción completa | False |
| reset | bool | Reinicia el historial de traducción | False |

### Ejemplo de solicitud
```json
{
  "text": "Hello, how are you?",
  "target_lang": "Spanish",
  "session_id": "session_1",
  "is_complete": false
}
```

### Respuesta
```json
{
  "result": "Hola, ¿cómo estás?"
}
```

## ⚙️ Cómo Funciona

1. **Traducción Incremental:**
   - Cuando se envía un fragmento de texto, la API lo acumula y lo traduce progresivamente
   - Si el texto ya fue traducido previamente, solo se traduce el nuevo fragmento

2. **Traducción Completa:**
   - Cuando se marca un diálogo como completo, la API traduce todo el texto acumulado y devuelve la traducción final

3. **Personalización:**
   - Puedes elegir el idioma y el género de la traducción según las necesidades de tu proyecto

## 🎥 Demo

He creado un video demostrativo que muestra cómo funciona la API en proyectos como Mort. [Ver demostración](https://tu-link-de-demo.com)

## 💻 Ejemplo de Implementación

Puedes encontrar ejemplos de cómo integrar esta API en tu proyecto en el siguiente enlace de GitHub:
[GitHub: miusuario/Mort](https://github.com/miusuario/Mort)

## 🤝 Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de abrir un pull request.

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

Contribuciones / Contributions
Si deseas contribuir a este proyecto, siéntete libre de abrir un pull request.
If you want to contribute to this project, feel free to open a pull request.

Licencia / License
Este proyecto está licenciado bajo la Licencia MIT.
This project is licensed under the MIT License.
