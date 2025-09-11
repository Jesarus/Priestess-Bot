import interactions
import json
import random
import math
import logging
from scores import load_scores, save_scores

OPERATORS_JSON = (
    "c:/Users/user/OneDrive/Área de Trabalho/Priestess-Bot/operators_structured.json"
)


def load_operators():
    """Carrega operadores do arquivo JSON."""
    try:
        with open(OPERATORS_JSON, encoding="utf-8") as f:
            data = json.load(f)
        return data["operators"]
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {OPERATORS_JSON}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar JSON: {OPERATORS_JSON}")
        return []
    except Exception as e:
        logging.error(f"Erro ao carregar operadores: {e}")
        return []


# Store the current round's operator (shared) and per-user hint index
current_operator = None
user_hint_indices = {}  # {user_id: hint_index}


def normalize_guess(guess):
    """Normaliza o palpite do usuário."""
    return guess.strip().lower()


def already_won(scores, user_id, operator_name):
    return (
        str(user_id) in scores
        and scores[str(user_id)].get("arkdle_last_win") == operator_name
    )


def update_score(scores, user_id, username, operator_name, pontos):
    if str(user_id) in scores:
        scores[str(user_id)]["pontos"] += pontos
        scores[str(user_id)]["username"] = username
        scores[str(user_id)]["arkdle_last_win"] = operator_name
    else:
        scores[str(user_id)] = {
            "username": username,
            "pontos": pontos,
            "arkdle_last_win": operator_name,
        }
    save_scores(scores)


async def send_hint(ctx, current_operator, hint_fields, hint_index, user_id):
    field = hint_fields[hint_index]
    value = current_operator.get(field, "Unknown")
    await ctx.send(
        f"Palpite incorreto. Próxima dica: {field.capitalize()} é '{value}'. Tente novamente!",
        ephemeral=True,
    )
    user_hint_indices[user_id] = hint_index + 1


async def send_correct(ctx, current_operator, hints_used, pontos):
    await ctx.send(
        f"Correto! O operador era {current_operator['name']}. Você usou {hints_used} dica(s) para acertar e ganhou {pontos} ponto(s)!",
        ephemeral=True,
    )


async def send_no_more_hints(ctx):
    await ctx.send(
        "Palpite incorreto. Não há mais dicas disponíveis! Tente novamente!",
        ephemeral=True,
    )


class ArkdleGame(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.slash_command(
        name="arkdle",
        description="Comece uma nova rodada Arkdle com um operador Arknights aleatório.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    async def arkdle(self, ctx: interactions.SlashContext):
        """Inicia uma nova rodada do Arkdle (apenas para administradores)."""
        global current_operator, user_hint_indices
        await ctx.defer()
        try:
            operators = load_operators()
            if not operators:
                await ctx.send(
                    "Erro ao carregar operadores. Tente novamente mais tarde."
                )
                return
            chosen = random.choice(operators)
            current_operator = chosen
            user_hint_indices = {}  # Reset all users' hint indices
            hint_fields = [
                "gender",
                "faction",
                "rarity",
                "class",
                "subclass",
                "nationality",
                "infection_status",
            ]
            hint = chosen.get(hint_fields[0], "Unknown")
            await ctx.send(
                f"Arkdle começou! Dica: {hint_fields[0].capitalize()} é '{hint}'. Use /arkdle_guess para fazer um palpite."
            )
        except Exception as e:
            logging.error(f"Erro no comando arkdle: {e}")
            try:
                await ctx.send(
                    "Ocorreu um erro ao iniciar o Arkdle. Tente novamente mais tarde."
                )
            except Exception:
                pass

    @interactions.slash_command(
        name="arkdle_guess",
        description="Faça um palpite para o operador atual do Arkdle.",
    )
    @interactions.slash_option(
        name="guess",
        description="Seu palpite para o nome do operador.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def arkdle_guess(self, ctx: interactions.SlashContext, guess: str):
        """Processa o palpite do usuário e atualiza pontuação conforme dicas usadas."""
        global current_operator, user_hint_indices
        await ctx.defer(ephemeral=True)
        try:
            if not current_operator:
                await ctx.send(
                    "No Arkdle round in progress. Use /arkdle to start one.",
                    ephemeral=True,
                )
                return
            user_id = ctx.author.id
            hint_fields = [
                "gender",
                "faction",
                "rarity",
                "class",
                "subclass",
                "nationality",
                "infection_status",
            ]
            guess_normalized = normalize_guess(guess)
            correct_name = current_operator["name"].lower()
            hint_index = user_hint_indices.get(user_id, 1)
            scores = load_scores()
            username = str(ctx.author)
            if already_won(scores, user_id, current_operator["name"]):
                await ctx.send(
                    "Você já acertou esse operador nesta rodada!", ephemeral=True
                )
                return
            if guess_normalized == correct_name:
                hints_used = hint_index
                pontos = math.ceil(30 / hints_used)
                update_score(
                    scores, user_id, username, current_operator["name"], pontos
                )
                await send_correct(ctx, current_operator, hints_used, pontos)
            elif hint_index < len(hint_fields):
                await send_hint(ctx, current_operator, hint_fields, hint_index, user_id)
            else:
                await send_no_more_hints(ctx)
        except (KeyError, ValueError) as e:
            logging.error(f"Erro de dados no comando arkdle_guess: {e}")
            await ctx.send(
                "Erro de dados ao processar seu palpite. Tente novamente mais tarde.",
                ephemeral=True,
            )
        except Exception as e:
            logging.error(f"Erro inesperado no comando arkdle_guess: {e}")
            try:
                await ctx.send(
                    "Ocorreu um erro ao processar seu palpite. Tente novamente mais tarde.",
                    ephemeral=True,
                )
            except Exception:
                pass


def setup(client):
    return ArkdleGame(client)
