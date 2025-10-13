import interactions
from scores import load_scores
from observability import log_command_usage


async def show_ranking(ctx):
    scores = load_scores()
    if not scores:
        await ctx.send("Ninguém acertou nenhum operador ainda.")
        return
    ranking = sorted(scores.items(), key=lambda x: x[1]["pontos"], reverse=True)
    msg = "**🏆 Ranking de Pontuação:**\n"
    for i, (user_id, data) in enumerate(ranking, 1):
        msg += f"{i}. {data['username']} — {data['pontos']} ponto(s)\n"
    await ctx.send(msg)


class RankingExtension(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.slash_command(
        name="ranking", description="Exibe o ranking de pontuação dos usuários."
    )
    @log_command_usage("ranking")
    async def ranking(self, ctx: interactions.SlashContext):
        await show_ranking(ctx)


def setup(client):
    return RankingExtension(client)
