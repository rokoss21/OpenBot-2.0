# config.py

# Токен вашего бота в Telegram, который вы получите от @BotFather
TELEGRAM_BOT_TOKEN = '{YOUR API KEY}'

# Путь к файлу логирования
LOG_FILE = 'log.txt'

# Настройки подключения к базе данных SQLite
DATABASE_URL = 'sqlite:///chatbot.db'

API_VALIDATE_URL = 'https://openrouter.ai/api/v1/validate_key'

# Список доступных моделей для выбора
AVAILABLE_MODELS = {
    1: {"name": "openrouter/auto", "max_tokens": 128000},
    2: {"name": "nousresearch/nous-capybara-7b", "max_tokens": 4096},
    3: {"name": "mistralai/mistral-7b-instruct", "max_tokens": 8192},
    4: {"name": "huggingfaceh4/zephyr-7b-beta", "max_tokens": 4096},
    5: {"name": "openchat/openchat-7b", "max_tokens": 8192},
    6: {"name": "gryphe/mythomist-7b", "max_tokens": 32768},
    7: {"name": "openrouter/cinematika-7b", "max_tokens": 8000},
    8: {"name": "rwkv/rwkv-5-world-3b", "max_tokens": 10000},
    9: {"name": "recursal/rwkv-5-3b-ai-town", "max_tokens": 10000},
    10: {"name": "recursal/eagle-7b", "max_tokens": 10000},
    11: {"name": "jondurbin/bagel-34b", "max_tokens": 8000},
    12: {"name": "jebcarter/psyfighter-13b", "max_tokens": 4096},
    13: {"name": "koboldai/psyfighter-13b-2", "max_tokens": 4096},
    14: {"name": "neversleep/noromaid-mixtral-8x7b-instruct", "max_tokens": 8000},
    15: {"name": "nousresearch/nous-hermes-llama2-13b", "max_tokens": 4096},
    16: {"name": "meta-llama/codellama-34b-instruct", "max_tokens": 8192},
    17: {"name": "phind/phind-codellama-34b", "max_tokens": 4096},
    18: {"name": "intel/neural-chat-7b", "max_tokens": 4096},
    19: {"name": "nousresearch/nous-hermes-2-mixtral-8x7b-dpo", "max_tokens": 32000},
    20: {"name": "nousresearch/nous-hermes-2-mixtral-8x7b-sft", "max_tokens": 32000},
    21: {"name": "haotian-liu/llava-13b", "max_tokens": 2048},
    22: {"name": "nousresearch/nous-hermes-2-vision-7b", "max_tokens": 4096},
    23: {"name": "meta-llama/llama-2-13b-chat", "max_tokens": 4096},
    24: {"name": "gryphe/mythomax-l2-13b", "max_tokens": 4096},
    25: {"name": "nousresearch/nous-hermes-llama2-70b", "max_tokens": 4096},
    26: {"name": "teknium/openhermes-2-mistral-7b", "max_tokens": 4096},
    27: {"name": "teknium/openhermes-2.5-mistral-7b", "max_tokens": 4096},
    28: {"name": "undi95/remm-slerp-l2-13b", "max_tokens": 4096},
    29: {"name": "undi95/toppy-m-7b", "max_tokens": 4096},
    30: {"name": "01-ai/yi-34b-chat", "max_tokens": 4096},
    31: {"name": "01-ai/yi-6b", "max_tokens": 4096},
    32: {"name": "togethercomputer/stripedhyena-nous-7b", "max_tokens": 32768},
    33: {"name": "togethercomputer/stripedhyena-hessian-7b", "max_tokens": 32768},
    34: {"name": "mistralai/mixtral-8x7b", "max_tokens": 32768},
    35: {"name": "nousresearch/nous-hermes-yi-34b", "max_tokens": 4096},
    36: {"name": "open-orca/mistral-7b-openorca", "max_tokens": 8192},
    37: {"name": "openai/gpt-3.5-turbo", "max_tokens": 4095},
    38: {"name": "openai/gpt-3.5-turbo-16k", "max_tokens": 16385},
    39: {"name": "openai/gpt-4-turbo-preview", "max_tokens": 128000},
    40: {"name": "openai/gpt-4", "max_tokens": 8191},
    41: {"name": "openai/gpt-4-32k", "max_tokens": 32767},
    42: {"name": "openai/gpt-4-vision-preview", "max_tokens": 128000},
    43: {"name": "openai/gpt-3.5-turbo-instruct", "max_tokens": 4095},
    44: {"name": "google/palm-2-chat-bison", "max_tokens": 36864},
    45: {"name": "google/palm-2-codechat-bison", "max_tokens": 28672},
    46: {"name": "google/palm-2-chat-bison-32k", "max_tokens": 131072},
    47: {"name": "google/palm-2-codechat-bison-32k", "max_tokens": 131072},
    48: {"name": "google/gemini-pro", "max_tokens": 131040},
    49: {"name": "google/gemini-pro-vision", "max_tokens": 65536},
    50: {"name": "perplexity/pplx-70b-online", "max_tokens": 4096},
    51: {"name": "perplexity/pplx-7b-online", "max_tokens": 4096},
    52: {"name": "perplexity/pplx-7b-chat", "max_tokens": 8192},
    53: {"name": "perplexity/pplx-70b-chat", "max_tokens": 4096},
    54: {"name": "meta-llama/llama-2-70b-chat", "max_tokens": 4096},
    55: {"name": "nousresearch/nous-capybara-34b", "max_tokens": 32768},
    56: {"name": "jondurbin/airoboros-l2-70b", "max_tokens": 4096},
    57: {"name": "austism/chronos-hermes-13b", "max_tokens": 4096},
    58: {"name": "migtissera/synthia-70b", "max_tokens": 8192},
    59: {"name": "pygmalionai/mythalion-13b", "max_tokens": 8192},
    60: {"name": "undi95/remm-slerp-l2-13b-6k", "max_tokens": 6144},
    61: {"name": "xwin-lm/xwin-lm-70b", "max_tokens": 8192},
    62: {"name": "gryphe/mythomax-l2-13b-8k", "max_tokens": 8192},
    63: {"name": "alpindale/goliath-120b", "max_tokens": 6144},
    64: {"name": "lizpreciatior/lzlv-70b-fp16-hf", "max_tokens": 4096},
    65: {"name": "neversleep/noromaid-20b", "max_tokens": 8192},
    66: {"name": "mistralai/mixtral-8x7b-instruct", "max_tokens": 32768},
    67: {"name": "cognitivecomputations/dolphin-mixtral-8x7b", "max_tokens": 32000},
    68: {"name": "anthropic/claude-2", "max_tokens": 200000},
    69: {"name": "anthropic/claude-2.0", "max_tokens": 100000},
    70: {"name": "anthropic/claude-instant-v1", "max_tokens": 100000},
    71: {"name": "mancer/weaver", "max_tokens": 8000},
    72: {"name": "mistralai/mistral-tiny", "max_tokens": 32000},
    73: {"name": "mistralai/mistral-small", "max_tokens": 32000},
    74: {"name": "mistralai/mistral-medium", "max_tokens": 32000},
}

