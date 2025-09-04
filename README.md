
# Priestess-Bot

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Discord bot for server management and fun interactions related to the game **Arknights**, such as:
- Character guessing quizzes with a scoring system, image manipulation, and support for alternative names.

---

## Priestess-Bot Highlights

- **Modern Slash Commands:** Uses Discord slash commands for an intuitive and integrated experience.
- **Image Integration:** Automatically generates and manipulates images, creating unique visual quizzes.
- **Interactive Game:** “Guess Who” mode challenges users to guess characters from silhouettes.
- **Real-Time Ranking:** Persistent scoring system and leaderboard for top players.
- **Alternative Names:** Accepts multiple correct answers for greater accessibility.
- **Private (ephemeral) responses:** Ensures privacy and a modern user experience.
- **Clean and tested code:** Modular structure, automated tests, and best practices.

---

## Features

- **Guess Who Game:** Sends an obscured image of a character and challenges users to guess who it is.
- **Scoring system:** Persistent scores for participants.
- **Alternative names:** Accepts different names for the same character.
- **Automatic silhouette generation:** Creates obscured images from the originals.

---

## Usage Example

```
/guess_who
```
The bot replies with a silhouette image and waits for users' answers.

[See an example image](https://drive.google.com/file/d/1VeAJHNcv65lXXQJEl6S9bsz9iJm8nBU4/view?usp=sharing)

---

## Installation

1. **Clone the repository:**
	```sh
	git clone https://github.com/Jesarus/Priestess-Bot.git
	cd Priestess-Bot
	```

2. **(Optional) Create a virtual environment:**
	```sh
	python -m venv venv
	.\venv\Scripts\activate
	```

3. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```

4. **Organize the images:**
	- Make sure the folders `Imagens Originais` and `Imagens Ofuscadas` are present and organized by character.

---

## How to Run

```sh
python bot.py
```
The bot will connect to Discord and be ready to receive commands.

---

## File Structure

- `bot.py`: Initializes the bot and loads the commands.
- `commands/guess_who.py`: Main quiz command.
- `image_utils.py`: Functions for image manipulation and obfuscation.
- `pontuacao.py`: User scoring system.
- `utils.py`: Utilities for alternative names.
- `nomes_alternativos.json`: List of alternative names for characters.
- `pontuacoes.json`: Persistent score file.
- `Imagens Originais/`: Original character images.
- `Imagens Ofuscadas/`: Processed images for the quiz.

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

- The bot uses the [interactions.py](https://github.com/interactions-py/library) library for Discord integration.
- Make sure the bot has sufficient permissions on the server to read and send messages and attachments.