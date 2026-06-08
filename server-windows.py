from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import markovify
import os
import requests

app = Flask(__name__)
CORS(app)

# Obtener el directorio donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    # Servir el archivo HTML desde el mismo directorio
    return send_from_directory(BASE_DIR, 'writing-app.html')

@app.route('/markov_generate', methods=['POST'])
def markov_generate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        sentences = data.get('sentences', 3)
        state_size = data.get('state_size', 2)
        
        if not text.strip():
            return jsonify({'error': 'No se proporcionó texto de entrenamiento'}), 400
        
        # Build the Markov model
        text_model = markovify.Text(text, state_size=state_size)
        
        # Generate sentences
        result_sentences = []
        for _ in range(sentences):
            sentence = text_model.make_sentence(tries=100)
            if sentence:
                result_sentences.append(sentence)
        
        if not result_sentences:
            return jsonify({'error': 'No se pudo generar texto. Intenta con más texto de entrenamiento o ajusta los parámetros.'}), 400
        
        result = ' '.join(result_sentences)
        
        return jsonify({
            'result': result,
            'sentences_generated': len(result_sentences)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/claude_call', methods=['POST'])
def claude_call():
    """
    Endpoint para llamar a Claude API
    Nota: Requiere API key de Anthropic
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        api_key = data.get('api_key', '')
        
        if not prompt.strip():
            return jsonify({'error': 'No se proporcionó prompt'}), 400
        
        if not api_key.strip():
            return jsonify({
                'error': 'Se requiere API key de Anthropic',
                'info': 'Obtén tu API key en: https://console.anthropic.com/',
                'instructions': 'Agrégala en el campo "API Key de Claude" en la interfaz'
            }), 400
        
        # Llamar a la API de Claude
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'messages': [{
                    'role': 'user',
                    'content': prompt
                }]
            },
            timeout=30
        )
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({
                'error': f"Error de API: {error_data.get('error', {}).get('message', 'Error desconocido')}"
            }), response.status_code
        
        result = response.json()
        text_content = result['content'][0]['text']
        
        return jsonify({
            'result': text_content
        })
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'La solicitud tardó demasiado. Intenta de nuevo.'}), 408
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de red: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/chatgpt_call', methods=['POST'])
def chatgpt_call():
    """
    Endpoint para llamar a ChatGPT API
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        api_key = data.get('api_key', '')
        
        if not prompt.strip():
            return jsonify({'error': 'No se proporcionó prompt'}), 400
        
        if not api_key.strip():
            return jsonify({
                'error': 'Se requiere API key de OpenAI',
                'info': 'Obtén tu API key en: https://platform.openai.com/'
            }), 400
        
        # Llamar a la API de OpenAI
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4',
                'messages': [{
                    'role': 'user',
                    'content': prompt
                }],
                'max_tokens': 2000
            },
            timeout=30
        )
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({
                'error': f"Error de API: {error_data.get('error', {}).get('message', 'Error desconocido')}"
            }), response.status_code
        
        result = response.json()
        text_content = result['choices'][0]['message']['content']
        
        return jsonify({
            'result': text_content
        })
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'La solicitud tardó demasiado. Intenta de nuevo.'}), 408
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de red: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("   📝 Editor de Escritura Avanzado")
    print("   Servidor iniciado correctamente")
    print("=" * 60)
    print(f"\n✓ Archivos en: {BASE_DIR}")
    print(f"✓ Servidor corriendo en: http://localhost:5000")
    print(f"✓ Abre tu navegador en: http://localhost:5000")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
