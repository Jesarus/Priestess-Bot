# Priestess-Bot

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Um bot de Discord para gerenciamento do servidor e interações divertidas com relação ao jogo **Arknights**, como:
- Quizzes de adivinhação de personagens do jogo com sistema de pontuação, manipulação de imagens e suporte a nomes alternativos.

---

## Diferenciais do Priestess-Bot

- **Comandos Slash modernos:** Utiliza comandos slash do Discord para experiência intuitiva e integrada.
- **Integração com imagens:** Gera e manipula imagens automaticamente, criando quizzes visuais únicos.
- **Jogo interativo:** Modo “Guess Who” desafia usuários a adivinhar personagens a partir de silhuetas.
- **Ranking em tempo real:** Sistema de pontuação persistente e ranking dos melhores jogadores.
- **Nomes alternativos:** Aceita múltiplas respostas corretas para maior acessibilidade.
- **Respostas privadas (ephemeral):** Garante privacidade e experiência moderna nas interações.
- **Código limpo e testado:** Estrutura modular, testes automatizados e uso de boas práticas.

---

## Funcionalidades

- **Jogo Guess Who:** Envia uma imagem ofuscada de um personagem e desafia os usuários a adivinharem quem é.
- **Sistema de pontuação:** Pontuação persistente para os participantes.
- **Nomes alternativos:** Aceita diferentes nomes para o mesmo personagem.
- **Geração automática de silhuetas:** Cria imagens ofuscadas a partir das originais.

---


## Exemplo de uso

```
/guess_who
```
O bot responde com uma imagem silhuetada e aguarda a resposta dos usuários.

[Veja um exemplo em imagem](https://drive.google.com/file/d/1VeAJHNcv65lXXQJEl6S9bsz9iJm8nBU4/view?usp=sharing)

---

## Instalação

1. **Clone o repositório:**
	```sh
	git clone https://github.com/Jesarus/Priestess-Bot.git
	cd Priestess-Bot
	```

2. **(Opcional) Crie um ambiente virtual:**
	```sh
	python -m venv venv
	.\venv\Scripts\activate
	```

3. **Instale as dependências:**
	```sh
	pip install -r requirements.txt
	```

4. **Organize as imagens:**
	- Certifique-se de que as pastas `Imagens Originais` e `Imagens Ofuscadas` estejam presentes e organizadas por personagem.

---

## Como rodar

```sh
python bot.py
```
O bot irá conectar ao Discord e ficará pronto para receber comandos.

---

## Estrutura dos arquivos

- `bot.py`: Inicializa o bot e carrega os comandos.
- `commands/guess_who.py`: Comando principal do quiz.
- `image_utils.py`: Funções para manipulação e ofuscação de imagens.
- `pontuacao.py`: Sistema de pontuação dos usuários.
- `utils.py`: Utilitários para nomes alternativos.
- `nomes_alternativos.json`: Lista de nomes alternativos para personagens.
- `pontuacoes.json`: Arquivo de pontuação persistente.
- `Imagens Originais/`: Imagens originais dos personagens.
- `Imagens Ofuscadas/`: Imagens processadas para o quiz.

---

## Como contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature ou correção
3. Envie um pull request

Sugestões, issues e contribuições são bem-vindas!

---

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## Observações

- O bot utiliza a biblioteca [interactions.py](https://github.com/interactions-py/library) para integração com o Discord.
- Certifique-se de que o bot tem permissões suficientes no servidor para ler e enviar mensagens e anexos.