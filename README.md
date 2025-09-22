
# Priestess-Bot

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Discord bot for server management and fun interactions related to the game **Arknights**.

---

## ✨ Main Features

- **Modern Slash Commands**
- **“Guess Who” Quiz with Obscured Images**
- **Arkdle Minigame**
- **Persistent Scoring System and Ranking**
- **Alternative Names Support**
- **Private (ephemeral) responses**
- **Modular structure and best practices**

---

## 📦 Project Structure

- `bot.py`: Initializes the bot and loads commands
- `config.py`: Loads environment variables and folder names
- `db.py`: (If present) Data utilities
- `scores.py`: Scoring system (uses `data/scores.json`)
- `image_utils.py`: Image manipulation and obfuscation
- `utils.py`: Utilities and alternative names
- `commands/`: Command modules (`guess_who.py`, `arkdle.py`, `ranking.py`, `sextou.py`)
- `data/`: Persistent data (`scores.json`, `operators_structured.json`)
- `alternative_names.json`: Alternative character names
- `Imagens Originais/` and `Imagens Ofuscadas/`: Images for the quizzes
- `requirements.txt`: Python dependencies

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
   python bot.py
   ```

---

## 🗂️ Persistent Data

- All user scores and operator data are stored in `data/`:
    - `data/scores.json`: User scores
    - `data/operators_structured.json`: Operator data for quizzes

---

## 🔒 Security & Best Practices

- Never commit your Discord bot token or sensitive data
- Use environment variables for secrets
- Keep dependencies updated
- Follow PEP8 and use docstrings
- Use logging for errors/debug
- Separate data from code (use the `data/` folder)

---

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

## Security & Best Practices

- **Never commit your Discord bot token or other sensitive data.**
- Use environment variables for all secrets.
- Keep your dependencies updated (`requirements.txt`).
- Use the `data/` folder for all persistent data, never store data in code files.
- Follow PEP8 and use docstrings for all functions and modules.
- Use logging (not print) for errors and debug information.

---
- The bot uses the [interactions.py](https://github.com/interactions-py/library) library for Discord integration.
- Make sure the bot has sufficient permissions on the server to read and send messages and attachments.