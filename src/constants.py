"""
Constants and configuration values for the Discord bot.
"""

# File paths
ORIGINAL_IMAGES_FOLDER = "Imagens Originais"
OBSCURED_IMAGES_FOLDER = "Imagens Ofuscadas"
OPERATORS_JSON_PATH = "data/operators_structured.json"
SCORES_JSON_PATH = "data/scores.json"
ALTERNATIVE_NAMES_PATH = "data/alternative_names.json"

# Image processing
SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")
EXCLUDED_IMAGE_PATTERNS = ("_e2", "_skin")
IMAGE_PROCESSING_THRESHOLD = 0.05  # Minimum area threshold for image processing

# Game configuration
GUESS_WHO_POINTS = 10
ARKDLE_BASE_POINTS = 30
ARKDLE_HINT_FIELDS = [
    "gender",
    "faction", 
    "rarity",
    "class",
    "subclass",
    "nationality",
    "infection_status"
]

# Discord permissions
ADMIN_PERMISSIONS = 0x8  # ADMINISTRATOR
MOD_PERMISSIONS = 0x20   # MANAGE_GUILD

# Logging configuration
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Health check thresholds
DEFAULT_CPU_THRESHOLD = 80.0
DEFAULT_MEMORY_THRESHOLD = 85.0
DEFAULT_DISK_THRESHOLD = 90.0

# Performance thresholds
DEFAULT_SLOW_THRESHOLD = 1.0
DEFAULT_CRITICAL_THRESHOLD = 5.0

# File size limits
MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Retry configuration
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 1

# Message limits
DISCORD_MESSAGE_LIMIT = 2000
EMBED_DESCRIPTION_LIMIT = 4096

# Timeouts
COMMAND_TIMEOUT_SECONDS = 30
HEALTH_CHECK_TIMEOUT_SECONDS = 10

# Environment variable names
ENV_BOT_TOKEN = "PRIESTESS_BOT_TOKEN"
ENV_LOG_LEVEL = "LOG_LEVEL"
ENV_LOG_DIR = "LOG_DIR"
ENV_CPU_THRESHOLD = "CPU_THRESHOLD"
ENV_MEMORY_THRESHOLD = "MEMORY_THRESHOLD"
ENV_DISK_THRESHOLD = "DISK_THRESHOLD"
ENV_DEBUG_MODE = "DEBUG_MODE"

# Error messages
ERROR_MESSAGES = {
    "NO_OPERATORS": "Nenhuma pasta de operador encontrada.",
    "NO_IMAGES": "Nenhuma imagem válida encontrada na pasta.",
    "NO_ROUND": "Nenhuma rodada em andamento.",
    "ALREADY_ANSWERED": "Você já respondeu a esta rodada!",
    "FILE_NOT_FOUND": "Arquivo não encontrado: {}",
    "JSON_DECODE_ERROR": "Erro ao decodificar JSON: {}",
    "LOAD_ERROR": "Erro ao carregar dados: {}",
    "SAVE_ERROR": "Erro ao salvar dados: {}",
    "IMAGE_PROCESSING_ERROR": "Erro ao processar imagem: {}",
    "INVALID_GAME_STATE": "Estado do jogo inválido.",
    "OPERATOR_NOT_FOUND": "Operador não encontrado: {}",
}

# Success messages
SUCCESS_MESSAGES = {
    "GUESS_REGISTERED": "Palpite registrado com sucesso!",
    "SCORES_UPDATED": "Pontuação atualizada!",
    "ROUND_STARTED": "Nova rodada iniciada!",
    "OPERATOR_REVEALED": "Operador revelado: {}",
    "DATA_LOADED": "Dados carregados com sucesso.",
    "DATA_SAVED": "Dados salvos com sucesso.",
}

# Regular expressions
OPERATOR_NAME_PATTERN = r"^[a-zA-Z\s'-]+$"
USER_ID_PATTERN = r"^\d+$"

# Default values
DEFAULT_SCORE = 0
DEFAULT_HINT_INDEX = 1
DEFAULT_ROUND_STATE = {
    "answers": {},
    "current_operator": None,
    "correct_answer": None
}

# Configuration validation
REQUIRED_ENV_VARS = [ENV_BOT_TOKEN]
OPTIONAL_ENV_VARS = [
    ENV_LOG_LEVEL,
    ENV_LOG_DIR,
    ENV_CPU_THRESHOLD,
    ENV_MEMORY_THRESHOLD,
    ENV_DISK_THRESHOLD,
    ENV_DEBUG_MODE
]

# File validation
REQUIRED_FILES = [
    OPERATORS_JSON_PATH,
    SCORES_JSON_PATH,
    ALTERNATIVE_NAMES_PATH
]

REQUIRED_DIRECTORIES = [
    ORIGINAL_IMAGES_FOLDER,
    OBSCURED_IMAGES_FOLDER,
    "data"
]
