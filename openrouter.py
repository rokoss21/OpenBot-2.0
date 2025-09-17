#openrouter.py
import requests
import logging

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def send_to_openrouter(message, api_key, model_id, max_tokens=4096, message_history=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages_payload = list(message_history) if message_history else []
    messages_payload.append({"role": "user", "content": message})

    payload = {
        "model": model_id,
        "messages": messages_payload,
        "max_tokens": max_tokens
    }
    logging.info(f"Sending request to OpenRouter: {payload}")
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Response from OpenRouter: {data}")
        if data.get("choices"):
            return data["choices"][0].get("message", {}).get("content", "")
        else:
            logging.error("OpenRouter API returned no choices.")
            return "Извините, произошла ошибка при обработке вашего сообщения."
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with OpenRouter API: {e}")
        return "Извините, не удалось связаться с OpenRouter API."
