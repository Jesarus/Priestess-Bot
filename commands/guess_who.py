import os
import random
import interactions
import logging
from config import ORIGINAL_IMAGES_FOLDER, OBSCURED_IMAGES_FOLDER
from utils import load_alternative_names
from scores import load_scores, save_scores
from image_utils import obscure_image

# Global state for the current round (should be improved for production)
round_state = {"answers": {}, "current_operator": None, "correct_answer": None}


def reset_round():
    round_state["answers"] = {}
    round_state["current_operator"] = None
    round_state["correct_answer"] = None


# Helper functions for GuessWhoGame


# Helper for getting operator folders
def get_operator_folders(base_path):
    return [
        d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))
    ]


# Helper for getting valid images in a folder
def get_operator_images(folder_path):
    return [
        f
        for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
        and "_e2" not in f.lower()
        and "_skin" not in f.lower()
    ]


# Helper for choosing a random image
def choose_operator_image(images):
    import uuid

    chosen_image = random.choice(images)
    ext = os.path.splitext(chosen_image)[1].lower()
    random_name = f"{uuid.uuid4().hex}{ext}"
    return chosen_image, random_name


# Helper for preparing the obscured image
def prepare_obscured_image(original_path, dest_folder, random_name):
    if os.path.exists(dest_folder):
        for f in os.listdir(dest_folder):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    os.remove(os.path.join(dest_folder, f))
                except Exception as e:
                    logging.error(f"Error removing old image: {f} - {e}")
    else:
        os.makedirs(dest_folder)
    output_path = os.path.join(dest_folder, random_name)
    obscure_image(original_path, output_path)
    return output_path


# Helper for updating round state
def update_round_state(chosen_folder, output_path):
    alternative_names = load_alternative_names()
    key = chosen_folder.lower()
    if key in alternative_names:
        round_state["correct_answer"] = alternative_names[key]
    else:
        round_state["correct_answer"] = [key]
    round_state["current_operator"] = output_path
    round_state["answers"] = {}


async def start_new_round(ctx):
    if round_state["current_operator"]:
        await ctx.send("Já há uma rodada em andamento!", ephemeral=True)
        return
    base_path = ORIGINAL_IMAGES_FOLDER
    subfolders = get_operator_folders(base_path)
    if not subfolders:
        logging.error("No operator folder found in 'Original Images'.")
        return
    chosen_folder = random.choice(subfolders)
    folder_path = os.path.join(base_path, chosen_folder)
    images = get_operator_images(folder_path)
    if not images:
        logging.error(f"No valid image found in folder '{chosen_folder}'.")
        return
    chosen_image, random_name = choose_operator_image(images)
    original_path = os.path.join(folder_path, chosen_image)
    dest_folder = os.path.join(OBSCURED_IMAGES_FOLDER, chosen_folder)
    output_path = prepare_obscured_image(original_path, dest_folder, random_name)
    update_round_state(chosen_folder, output_path)
    with open(output_path, "rb") as f:
        await ctx.send(
            "Quem é esse operador?",
            files=interactions.File(f, file_name=random_name),
        )


async def register_answer(ctx, palpite):
    if round_state["current_operator"] is None:
        await ctx.send("No round in progress.", ephemeral=True)
        return
    user_id = str(ctx.author.id)
    if user_id in round_state["answers"]:
        await ctx.send("Você já respondeu a esta rodada!", ephemeral=True)
        return
    round_state["answers"][user_id] = palpite.lower()
    await ctx.send("Palpite registrado com sucesso!", ephemeral=True)


async def reveal_operator(ctx, client):
    if round_state["current_operator"] is None:
        await ctx.send("No round in progress.", ephemeral=True)
        return
    winners = []
    for user_id, guess in round_state["answers"].items():
        if guess in round_state["correct_answer"]:
            user = await client.fetch_user(int(user_id))
            winners.append((user_id, user))
    msg = f"O operador era **{round_state['correct_answer'][0].capitalize()}**!\n"
    if winners:
        msg += "Respostas corretas: " + ", ".join(user.mention for _, user in winners)
        scores = load_scores()
        for user_id, user in winners:
            if user_id in scores:
                scores[user_id]["pontos"] += 10
                scores[user_id]["username"] = str(user)
            else:
                scores[user_id] = {"username": str(user), "pontos": 10}
        save_scores(scores)
        msg += "\nPontuação atualizada!"
    else:
        msg += "Ninguém acertou desta vez."
    await ctx.send(msg)
    reset_round()




class GuessWhoGame(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.slash_command(
        name="guess_who",
        description="Inicia uma nova rodada (apenas para admins/mods)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR
        | interactions.Permissions.MANAGE_GUILD,
    )
    async def guess_who(self, ctx: interactions.SlashContext):
        await start_new_round(ctx)

    @interactions.slash_command(
        name="responder", description="Dê seu palpite para a rodada atual."
    )
    @interactions.slash_option(
        name="palpite",
        description="Seu palpite para o operador",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def answer(self, ctx: interactions.SlashContext, palpite: str):
        await register_answer(ctx, palpite)

    @interactions.slash_command(
        name="revelar",
        description="Revela o operador correto e atualiza a pontuação (apenas para admins/mods)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR
        | interactions.Permissions.MANAGE_GUILD,
    )
    async def reveal(self, ctx: interactions.SlashContext):
        await reveal_operator(ctx, self.client)



def setup(client):
    return GuessWhoGame(client)
