
# Priestess-Bot

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A modern Discord bot for server management and interactive games, inspired by **Arknights**.

---

## 🚀 Main Features

- Modern slash commands
- “Guess Who” quiz with obscured images
- Arkdle minigame
- Persistent scoring system and automated ranking
- Alternative names support for answers
- Private (ephemeral) responses
- Dynamic image manipulation
- Modular architecture with separation of logic, data, and configuration
- Structured logging, error tracking, and health monitoring (observability)
- Environment variable configuration for sensitive data

---

## 📦 Project Structure

Priestess-Bot/
├── src/ # All Python source code
│ ├── bot.py
│ ├── config.py
│ ├── config_manager.py
│ ├── constants.py
│ ├── exceptions.py
│ ├── game_state.py
│ ├── image_utils.py
│ ├── logging_utils.py
│ ├── monitor.py
│ ├── observability.py
│ ├── scores.py
│ ├── setup_observability.py
│ ├── utils.py
│ └── commands/
│ ├── arkdle.py
│ ├── guess_who.py
│ ├── health.py
│ ├── ranking.py
│ ├── sextou.py
├── data/ # Persistent data (JSON files)
│ ├── scores.json
│ ├── operators_structured.json
│ └── alternative_names.json
├── Imagens Originais/ # Original images for quizzes
├── Imagens Ofuscadas/ # Obscured images for quizzes
├── requirements.txt # Python dependencies
├── README.md
└── LICENSE

---

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Jesarus/Priestess-Bot.git
   cd Priestess-Bot
   ```
2. (Optional) Create a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Organize the images:
   - Make sure the folders `Imagens Originais` and `Imagens Ofuscadas` are present and organized by character.
5. Configure the environment variable for the token:
   - In PowerShell:
     ```powershell
     $env:PRIESTESS_BOT_TOKEN = "your_token_here"
     ```
   - Never share your token publicly!
6. Run the bot:
   ```sh
   python src/bot.py
   ```

---

## 🗂️ Persistent Data

- All user scores and operator data are stored in the data folder:
    - `data/scores.json`: User scores
    - `data/operators_structured.json`: Operator data for quizzes
    - `alternative_names.json`: Alternative character names

---

## 🔒 Security & Best Practices

   - Never commit your Discord bot token or other sensitive data.
   - Use environment variables for all secrets.
   - Keep your dependencies updated (requirements.txt).
   - Use the data folder for all persistent data; never store data in code files.
   - Follow PEP8 and use docstrings for all functions and modules.
   - Use logging (not print) for errors and debug information.
   - Separate logic, data, and configuration for maintainability.
   - Monitor bot health and errors using the observability modules.
---

## Observability
   - Structured logging for all major events and errors.
   - Error tracking and health monitoring modules for reliability.
   - All logs are stored and can be reviewed for debugging and analytics.

## How to Contribute

1. Fork this repository
2. Create a branch for your feature or fix
3. Submit a pull request

Suggestions, issues, and contributions are welcome!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Notes

The bot uses the interactions.py library for Discord integration.
Make sure the bot has sufficient permissions on the server to read and send messages and attachments.