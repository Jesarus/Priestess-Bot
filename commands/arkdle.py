import interactions
import json
import random
import math
from scores import load_scores, save_scores

OPERATORS_JSON = (
    "c:/Users/user/OneDrive/Área de Trabalho/Priestess-Bot/operators_structured.json"
)


def load_operators():
    try:
        with open(OPERATORS_JSON, encoding="utf-8") as f:
            data = json.load(f)
        return data["operators"]
    except Exception as e:
        print(f"Erro ao carregar operadores: {e}")
        return []


# Store the current round's operator (shared) and per-user hint index
current_operator = None
user_hint_indices = {}  # {user_id: hint_index}


class ArkdleGame(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.slash_command(
        name="arkdle",
        description="Comece uma nova rodada Arkdle com um operador Arknights aleatório.",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    async def arkdle(self, ctx: interactions.SlashContext):
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
            print(f"Erro no comando arkdle: {e}")
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
            # Get user's current hint index, default to 1 (gender)
            hint_index = user_hint_indices.get(user_id, 1)
            correct_name = current_operator["name"].lower()
            if guess.strip().lower() == correct_name:
                
                hints_used = user_hint_indices.get(user_id, 1)
                pontos = math.ceil(20 / hints_used)
                # Atualiza scores.json
                scores = load_scores()
                username = str(ctx.author)
                if str(user_id) in scores:
                    scores[str(user_id)]["pontos"] += pontos
                    scores[str(user_id)]["username"] = username
                else:
                    scores[str(user_id)] = {"username": username, "pontos": pontos}
                save_scores(scores)
                await ctx.send(
                    f"Correto! O operador era {current_operator['name']}. Você usou {hints_used} dica(s) para acertar e ganhou {pontos} ponto(s)!",
                    ephemeral=True,
                )
                # Não encerra a rodada, permite que outros continuem tentando
            else:
                if hint_index < len(hint_fields):
                    field = hint_fields[hint_index]
                    value = current_operator.get(field, "Unknown")
                    await ctx.send(
                        f"Palpite incorreto. Próxima dica: {field.capitalize()} é '{value}'. Tente novamente!",
                        ephemeral=True,
                    )
                    user_hint_indices[user_id] = hint_index + 1
                else:
                    await ctx.send(
                        "Palpite incorreto. Não há mais dicas disponíveis! Tente novamente!",
                        ephemeral=True,
                    )
        except Exception as e:
            print(f"Erro no comando arkdle_guess: {e}")
            try:
                await ctx.send(
                    "Ocorreu um erro ao processar seu palpite. Tente novamente mais tarde.",
                    ephemeral=True,
                )
            except Exception:
                pass


def setup(client):
    return ArkdleGame(client)
