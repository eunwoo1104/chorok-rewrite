import dico  # noqa
import dico_command
import dico_interaction as dico_inter
import psutil
from humanize import naturalsize

import utils
from models import ChorokBot, Colors


def load(bot: ChorokBot) -> None:
    bot.load_addons(Default)


def unload(bot: ChorokBot) -> None:
    bot.unload_addons(Default)


class Default(dico_command.Addon):  # type: ignore[call-arg, misc]
    bot: ChorokBot
    name = "기본"

    @dico_inter.command(name="information", description="봇의 정보를 확인합니다.")
    async def _information(self, ctx: dico_inter.InteractionContext) -> None:
        embed = dico.Embed(title="정보", color=Colors.information)
        embed.add_field(
            name="봇",
            value=f"{len(self.bot.audio.voice_clients)}/{self.bot.guild_count} (노래를 재생중인 서버/총 서버)",
        )

        memory = psutil.virtual_memory()
        embed.add_field(
            name="서버",
            value=f"CPU: {psutil.cpu_percent()}%\n"
            f"RAM: {naturalsize(memory.used)}/{naturalsize(memory.total)}",
            inline=False,
        )

        await ctx.send(embed=embed)

    @dico_inter.command(name="ping", description="봇의 명령어 응답 속도를 확인합니다.")
    async def _ping(self, ctx: dico_inter.InteractionContext) -> None:
        await ctx.send(embed=dico.Embed(
            title="퐁!",
            description=f"**Discord 게이트웨이:** `{round(self.bot.get_shard(ctx.guild_id).ping * 1000)}ms"
            f"({self.bot.get_shard_id(ctx.guild_id) + 1}호기)`",
            color=Colors.information,
        ))

    @dico_inter.command(name="invite", description="봇의 초대 링크를 보냅니다.")
    async def _invite(self, ctx: dico_inter.InteractionContext) -> None:
        await ctx.send(embed=dico.Embed(
            title="초대하기",
            description=f"[여기를 눌러]({utils.formatter.create_invite_link(str(self.bot.application_id), 28624960)})"
            f" 초록을 초대하실 수 있습니다.",
            color=Colors.information,
        ))

    @dico_inter.command(name="support", description="공식 서포트 서버의 링크를 보냅니다.")
    async def _support(self, ctx: dico_inter.InteractionContext) -> None:
        await ctx.send(embed=dico.Embed(
            title="공식 서포트 서버",
            description=f"[여기를 눌러](https://discord.gg/P25nShtqFX) 공식 서포트 서버에 입장하실 수 있습니다.",
            color=Colors.information,
        ))

    @dico_inter.command(name="help", description="도움말을 확인합니다.")
    async def _help(self, ctx: dico_inter.InteractionContext) -> None:
        embed = dico.Embed(
            title="도움말",
            description="자세한 사용 방법은 [여기](https://sslr.notion.site/36732f88e6214ee6af049bce101922fb)를 참고하시기 바랍니다.\n"
            "`[인자]`는 선택적 인자, `<인자>`는 필수 인자를 뜻합니다.",
            color=Colors.information)

        for addon in self.bot.addons:
            embed.add_field(
                name=addon.name,
                value="\n".join([
                    f"**/{command.name}{' ' + ' '.join([('<{}>' if option.required else '[{}]').format(option.name) for option in command.options])}:** `{command.description}`"
                    for command in map(lambda x: x.command, addon.interactions)
                    if command.description
                ]),
                inline=False)

        await ctx.send(embed=embed)
