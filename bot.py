import discord
from discord.ext import commands
import random
import os
from config import TOKEN, PONTUACOES_PATH, PASTA_ORIGINAIS, PASTA_SILHUETAS
from pontuacao import carregar_pontuacoes, salvar_pontuacoes
from utils import carregar_nomes_alternativos

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Variáveis de estado da rodada
respostas = {}
operador_atual = None
resposta_certa = None

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command(name="iniciar")
@commands.has_any_role("Administradores", "Moderadores")
async def iniciar_rodada(ctx):
    global operador_atual, resposta_certa, respostas

    if operador_atual is not None:
        await ctx.send("Já há uma rodada em andamento!")
        return

    base_path = PASTA_SILHUETAS
    subpastas = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not subpastas:
        await ctx.send("Nenhuma pasta de operador encontrada em 'imagens'.")
        return

    pasta_escolhida = random.choice(subpastas)
    pasta_path = os.path.join(base_path, pasta_escolhida)
    imagens = [f for f in os.listdir(pasta_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not imagens:
        await ctx.send(f"Nenhuma imagem encontrada na pasta '{pasta_escolhida}'.")
        return

    imagem_escolhida = random.choice(imagens)
    nome_arquivo = os.path.join(pasta_path, imagem_escolhida)

    nomes_alternativos = carregar_nomes_alternativos()
    chave = pasta_escolhida.lower()
    if chave in nomes_alternativos:
        resposta_certa = nomes_alternativos[chave]
    else:
        resposta_certa = [chave]

    operador_atual = nome_arquivo
    respostas = {}

    with open(nome_arquivo, "rb") as f:
        imagem = discord.File(f)
        await ctx.send("❓ Quem é esse operador?", file=imagem)

@bot.command(name="responder")
async def responder(ctx, *, palpite: str):
    global respostas, operador_atual

    if operador_atual is None:
        await ctx.send("❌ Nenhuma rodada em andamento.")
        return

    if str(ctx.author.id) in respostas:
        await ctx.send("⛔ Você já respondeu nessa rodada!")
        return

    respostas[str(ctx.author.id)] = palpite.lower()
    await ctx.send("✅ Palpite registrado com sucesso!")
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass  # O bot não tem permissão para deletar mensagens

@bot.command(name="revelar")
@commands.has_any_role("Administradores", "Moderadores")
async def revelar(ctx):
    global operador_atual, resposta_certa, respostas

    if operador_atual is None:
        await ctx.send("❌ Nenhuma rodada em andamento.")
        return

    acertadores = []
    for user_id, palpite in respostas.items():
        if palpite in resposta_certa:
            user = await bot.fetch_user(int(user_id))
            acertadores.append((user_id, user))

    msg = f"🧊 O operador era **{resposta_certa[0].capitalize()}**!\n"
    if acertadores:
        msg += "🎉 Acertaram: " + ", ".join(user.mention for _, user in acertadores)
        # Sistema de pontuação
        pontuacoes = carregar_pontuacoes()
        for user_id, user in acertadores:
            if user_id in pontuacoes:
                pontuacoes[user_id]["pontos"] += 1
                pontuacoes[user_id]["username"] = str(user)  # Atualiza nome de usuário único
            else:
                pontuacoes[user_id] = {"username": str(user), "pontos": 1}
        salvar_pontuacoes(pontuacoes)
        msg += "\n🏅 Pontuação atualizada!"
    else:
        msg += "😢 Ninguém acertou dessa vez."

    await ctx.send(msg)

    # Reset
    operador_atual = None
    resposta_certa = None
    respostas = {}

@bot.command(name="ranking")
async def pontuacao(ctx):
    pontuacoes = carregar_pontuacoes()
    if not pontuacoes:
        await ctx.send("Ninguém acertou nenhum operador até o momento.")
        return
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1]["pontos"], reverse=True)
    msg = "**🏆 Ranking de Pontuação:**\n"
    for i, (user_id, dados) in enumerate(ranking, 1):
        msg += f"{i}. {dados['username']} — {dados['pontos']} ponto(s)\n"
    await ctx.send(msg)

bot.run(TOKEN)