# 🔑 Guía para Obtener API Keys

Esta guía te explica cómo obtener las claves API necesarias para usar Claude y ChatGPT en la aplicación.

## 🤖 API Key de Claude (Anthropic)

### Paso 1: Crear cuenta en Anthropic
1. Ve a: **https://console.anthropic.com/**
2. Haz clic en "Sign Up" (Registrarse)
3. Completa el registro con tu email
4. Verifica tu cuenta por email

### Paso 2: Obtener créditos
- Anthropic ofrece **$5 USD gratis** al registrarte
- Después necesitarás agregar un método de pago

### Paso 3: Crear API Key
1. Una vez dentro, ve a "API Keys" en el menú lateral
2. Haz clic en "Create Key"
3. Dale un nombre (ej: "Editor de Escritura")
4. **¡IMPORTANTE!** Copia la key inmediatamente (solo se muestra una vez)
5. Tu key se verá así: `sk-ant-api03-xxxxxxxxxxxxx`

### Paso 4: Usar en la aplicación
1. Abre la aplicación (localhost:5000)
2. En la sección "ASISTENTE IA", pestaña "Claude"
3. Pega tu API key en el campo "API Key de Claude"
4. ¡Listo! Ya puedes usar Claude

### 💰 Precios de Claude (2025)
- **Claude Sonnet 4**: ~$3 por millón de tokens de entrada, ~$15 por millón de salida
- **1000 tokens** ≈ 750 palabras
- **Ejemplo**: Un documento de 2000 palabras procesado 10 veces = ~$0.50 USD

---

## 💬 API Key de ChatGPT (OpenAI)

### Paso 1: Crear cuenta en OpenAI
1. Ve a: **https://platform.openai.com/**
2. Haz clic en "Sign Up"
3. Regístrate con tu email o cuenta de Google/Microsoft
4. Verifica tu cuenta

### Paso 2: Agregar método de pago
- OpenAI **NO ofrece créditos gratuitos** actualmente
- Necesitas agregar una tarjeta de crédito/débito
- Ve a "Billing" → "Payment methods"
- Agrega tu método de pago
- Establece un límite de gasto (recomendado: $5-10 para empezar)

### Paso 3: Crear API Key
1. Ve a "API Keys" en el menú
2. Haz clic en "Create new secret key"
3. Dale un nombre (ej: "Editor de Escritura")
4. **¡IMPORTANTE!** Copia la key inmediatamente (solo se muestra una vez)
5. Tu key se verá así: `sk-proj-xxxxxxxxxxxxx` o `sk-xxxxxxxxxxxxx`

### Paso 4: Usar en la aplicación
1. Abre la aplicación (localhost:5000)
2. En la sección "ASISTENTE IA", haz clic en la pestaña "ChatGPT"
3. Pega tu API key en el campo "API Key de OpenAI"
4. ¡Listo! Ya puedes usar ChatGPT

### 💰 Precios de ChatGPT (2025)
- **GPT-4**: ~$10 por millón de tokens de entrada, ~$30 por millón de salida
- **GPT-3.5-turbo**: ~$0.50 por millón de tokens de entrada, ~$1.50 por millón de salida
- **1000 tokens** ≈ 750 palabras
- **Ejemplo**: Un documento de 2000 palabras procesado 10 veces = ~$1.50 USD (GPT-4)

---

## 🔒 Seguridad de las API Keys

### ⚠️ MUY IMPORTANTE:

1. **NUNCA compartas tus API keys**
   - No las publiques en GitHub, foros, redes sociales
   - No las envíes por email o chat
   - No las incluyas en screenshots

2. **Guárdalas de forma segura**
   - Usa un administrador de contraseñas (LastPass, 1Password, Bitwarden)
   - O guárdalas en un archivo de texto encriptado

3. **Establece límites de gasto**
   - En Anthropic: "Settings" → "Billing" → "Usage limits"
   - En OpenAI: "Billing" → "Usage limits"
   - Recomendado: $10-20 USD/mes para uso personal

4. **Si una key se compromete**
   - Elimínala inmediatamente desde la consola
   - Crea una nueva
   - Revisa el historial de uso para detectar uso no autorizado

---

## 💡 Consejos para Ahorrar Dinero

### 1. Usa tokens eficientemente
- Sé específico en tus prompts (evita repeticiones)
- No envíes el mismo texto múltiples veces
- Usa las respuestas previas en lugar de regenerar

### 2. Elige el modelo apropiado
- **Claude Sonnet**: Equilibrio entre calidad y precio
- **GPT-3.5**: Más barato, bueno para tareas simples
- **GPT-4**: Más caro pero mejor calidad

### 3. Establece límites
```
Antropic Console → Settings → Usage limits → $10/mes
OpenAI Console → Billing → Usage limits → $10/mes
```

### 4. Monitorea tu uso
- Revisa el dashboard de uso diariamente al principio
- Ambas plataformas envían alertas por email

---

## 🆓 Alternativas Gratuitas

Si no quieres gastar dinero en APIs:

### 1. Claude.ai (Interfaz web)
- **Gratis** con límites diarios
- Ve a: https://claude.ai
- Puedes copiar/pegar desde tu editor

### 2. ChatGPT (Interfaz web)
- **Gratis** con GPT-3.5
- Ve a: https://chat.openai.com
- Limitado pero funcional

### 3. Generador Markov (local)
- **100% gratis**
- No requiere API keys
- Funciona sin internet
- Usa solo el texto de entrenamiento

---

## 📊 Comparación de Costos

| Tarea | Claude Sonnet | GPT-4 | GPT-3.5 |
|-------|--------------|-------|---------|
| Corregir un párrafo (100 palabras) | ~$0.001 | ~$0.003 | ~$0.0002 |
| Escribir un artículo (1000 palabras) | ~$0.02 | ~$0.06 | ~$0.003 |
| Procesar un libro (50,000 palabras) | ~$1.00 | ~$3.00 | ~$0.15 |
| Uso mensual moderado (100 consultas) | ~$2-5 | ~$6-15 | ~$0.30-1 |

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar la app sin API keys?**
R: Sí, el generador Markov funciona sin APIs. Las funciones de IA requieren keys.

**P: ¿Cuánto cuesta usar Claude/ChatGPT?**
R: Para uso personal moderado: $2-10 USD/mes. Puedes establecer límites.

**P: ¿Qué pasa si se me acaban los créditos?**
R: La API dejará de funcionar hasta que agregues más créditos. No hay cargos sorpresa.

**P: ¿Puedo compartir una API key con amigos?**
R: No recomendado. Cada persona debería tener su propia key para controlar gastos.

**P: ¿Las keys expiran?**
R: No expiran automáticamente, pero puedes eliminarlas manualmente en cualquier momento.

**P: ¿Necesito ambas APIs?**
R: No, puedes usar solo una. Claude o ChatGPT, tú eliges según tu preferencia.

---

## 🎯 Recomendación Final

**Para empezar:**
1. Crea cuenta en Anthropic (tiene $5 gratis)
2. Prueba Claude con el crédito gratuito
3. Si te gusta, agrega método de pago
4. Establece un límite de $10/mes
5. Monitorea tu uso la primera semana

**Alternativa sin costo:**
1. Usa solo el generador Markov (gratis)
2. Usa Claude.ai y ChatGPT web (gratis con límites)
3. Copia/pega resultados manualmente

---

## 📞 Soporte

Si tienes problemas:
- **Anthropic Support**: support@anthropic.com
- **OpenAI Support**: help.openai.com
- **Documentación Claude**: docs.anthropic.com
- **Documentación OpenAI**: platform.openai.com/docs

---

¡Buena suerte con tu escritura! 📝✨
