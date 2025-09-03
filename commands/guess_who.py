import os
import random
import interactions
from config import PASTA_ORIGINAIS, PASTA_SILHUETAS
from utils import carregar_nomes_alternativos
from pontuacao import carregar_pontuacoes, salvar_pontuacoes
from image_utils import obscurecer_imagem

# Estado global para a rodada (pode ser melhorado para produção)
rodada = {
    "respostas": {},
    "operador_atual": None,
    "resposta_certa": None
}

def reset_rodada():
    rodada["respostas"] = {}
    rodada["operador_atual"] = None
    rodada["resposta_certa"] = None

class Jogo(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.slash_command(
        name="guess_who",
        description="Inicia uma nova rodada (apenas para admins/mods)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR | interactions.Permissions.MANAGE_GUILD
    )
    async def guess_who(self, ctx: interactions.SlashContext):
        if rodada["operador_atual"] is not None:
            await ctx.send("Já há uma rodada em andamento!", ephemeral=True)
            return
        base_path = PASTA_ORIGINAIS
        subpastas = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        if not subpastas:
            await ctx.send("Nenhuma pasta de operador encontrada em 'Imagens Originais'.", ephemeral=True)
            return
        pasta_escolhida = random.choice(subpastas)
        pasta_path = os.path.join(base_path, pasta_escolhida)
        imagens = [
            f for f in os.listdir(pasta_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
            and "_e2" not in f.lower()
            and "_skin" not in f.lower()
        ]
        if not imagens:
            await ctx.send(f"Nenhuma imagem válida encontrada na pasta '{pasta_escolhida}'.", ephemeral=True)
            return
        import uuid
        imagem_escolhida = random.choice(imagens)
        caminho_original = os.path.join(pasta_path, imagem_escolhida)
        pasta_destino = os.path.join(PASTA_SILHUETAS, pasta_escolhida)
        if os.path.exists(pasta_destino):
            for f in os.listdir(pasta_destino):
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    try:
                        os.remove(os.path.join(pasta_destino, f))
                    except Exception as e:
                        print(f"Erro ao remover imagem antiga: {f} - {e}")
        else:
            os.makedirs(pasta_destino)
        # Gerar nome aleatório para a imagem ofuscada
        ext = os.path.splitext(imagem_escolhida)[1].lower()
        nome_aleatorio = f"{uuid.uuid4().hex}{ext}"
        caminho_saida = os.path.join(pasta_destino, nome_aleatorio)
        obscurecer_imagem(caminho_original, caminho_saida)
        nomes_alternativos = carregar_nomes_alternativos()
        chave = pasta_escolhida.lower()
        if chave in nomes_alternativos:
            rodada["resposta_certa"] = nomes_alternativos[chave]
        else:
            rodada["resposta_certa"] = [chave]
        rodada["operador_atual"] = caminho_saida
        rodada["respostas"] = {}
        with open(caminho_saida, "rb") as f:
            await ctx.send("Quem é esse operador?", files=interactions.File(f, file_name=nome_aleatorio))

    @interactions.slash_command(
        name="responder",
        description="Dê seu palpite para a rodada atual."
    )
    @interactions.slash_option(
        name="palpite",
        description="Seu palpite para o operador",
        opt_type=interactions.OptionType.STRING,
        required=True
    )
    async def responder(self, ctx: interactions.SlashContext, palpite: str):
        if rodada["operador_atual"] is None:
            await ctx.send("Nenhuma rodada em andamento.", ephemeral=True)
            return
        user_id = str(ctx.author.id)
        if user_id in rodada["respostas"]:
            await ctx.send("Você já respondeu nessa rodada!", ephemeral=True)
            return
        rodada["respostas"][user_id] = palpite.lower()
        await ctx.send("Palpite registrado com sucesso!", ephemeral=True)

    @interactions.slash_command(
        name="revelar",
        description="Revela o operador correto e atualiza a pontuação (apenas para admins/mods)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR | interactions.Permissions.MANAGE_GUILD
    )
    async def revelar(self, ctx: interactions.SlashContext):
        if rodada["operador_atual"] is None:
            await ctx.send("Nenhuma rodada em andamento.", ephemeral=True)
            return
        acertadores = []
        for user_id, palpite in rodada["respostas"].items():
            if palpite in rodada["resposta_certa"]:
                user = await self.client.fetch_user(int(user_id))
                acertadores.append((user_id, user))
        msg = f"O operador era **{rodada['resposta_certa'][0].capitalize()}**!\n"
        if acertadores:
            msg += "Acertaram: " + ", ".join(user.mention for _, user in acertadores)
            pontuacoes = carregar_pontuacoes()
            for user_id, user in acertadores:
                if user_id in pontuacoes:
                    pontuacoes[user_id]["pontos"] += 10
                    pontuacoes[user_id]["username"] = str(user)
                else:
                    pontuacoes[user_id] = {"username": str(user), "pontos": 10}
            salvar_pontuacoes(pontuacoes)
            msg += "\nPontuação atualizada!"
        else:
            msg += "Ninguém acertou dessa vez."
        await ctx.send(msg)
        reset_rodada()

    @interactions.slash_command(
        name="ranking",
        description="Exibe o ranking de pontuação dos usuários."
    )
    async def ranking(self, ctx: interactions.SlashContext):
        pontuacoes = carregar_pontuacoes()
        if not pontuacoes:
            await ctx.send("Ninguém acertou nenhum operador até o momento.")
            return
        ranking = sorted(pontuacoes.items(), key=lambda x: x[1]["pontos"], reverse=True)
        msg = "**🏆 Ranking de Pontuação:**\n"
        for i, (user_id, dados) in enumerate(ranking, 1):
            msg += f"{i}. {dados['username']} — {dados['pontos']} ponto(s)\n"
        await ctx.send(msg)

def setup(client):
    return Jogo(client)