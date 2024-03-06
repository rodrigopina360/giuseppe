from __future__ import annotations

from common import humanizer
from discord import Embed
from models.osu import Mode
from models.osu import Score
from models.osu import User


def _score_to_desc_str(score: Score) -> str:
    scoretime = str()
    rank = score.grade
    match rank:
        case "XH": rank = "<:silverssrank:1203058459809947698>"
        case "X": rank = "<:ssrank:1203058474418700410>"
        case "SH": rank = "<:silversrank:1203058412414304276>"
        case "S": rank = "<:srank:1203058484833165383>"
        case "A": rank = "<:arank:1203058503921705010>"
        case "B": rank = "<:brank:1203058514067456061>"
        case "C": rank = "<:crank:1203058524444426360>"
        case "D": rank = "<:drank:1203058534749708380>"
        case _: rank = "<:frank:1203058543595495454>"

    if(score.grade == "F"):
        scoretime = f"({((score.time_elapsed / (score.beatmap.total_length * 1000)) * 100):.1f}%)"

    desc = (
        f"[**{score.beatmap.title}** [{score.beatmap.version}]]({score.beatmap.url}) **+{score.mods} [{score.beatmap.diff:.2f}*]**\n"
    )
    desc += f"▸ {rank}{scoretime} ▸ **{score.pp:.2f}pp** ▸ {score.acc:.2f}%\n"
    desc += f"▸ {score.score:,} ▸ x{score.max_combo}/{score.beatmap.max_combo} ▸ [{score.n300}/{score.n100}/{score.n50}/{score.nmiss}]\n"
    desc += f"Score performed <t:{score.play_time.timestamp():.0f}:R>"

    return desc


class ScoreSingleEmbed(Embed):
    def __init__(self, ctx: commands.Context, user: User, mode: Mode, score: Score, **kwargs):
        super().__init__(
            **kwargs,
        )
        self.color = ctx.author.color
        self.set_author(
            name=f"Recent osu!{mode!r} play for {user.info.name}",
            icon_url=user.info.avatar_url,
            url=user.info.profile_url,
        )
        self.description = _score_to_desc_str(score)
        self.set_thumbnail(url=score.beatmap.cover_url)


class ScoreMultipleEmbed(Embed):
    def __init__(self, ctx: commands.Context, user: User, mode: Mode, scores: list[Score], **kwargs):
        super().__init__(
            **kwargs,
        )
        self.color = ctx.author.color
        self.set_author(
            name=f"Top osu!{mode!r} plays for {user.info.name}",
            icon_url=user.info.avatar_url,
            url=user.info.profile_url,
        )
        self.description = ""
        for idx, score in enumerate(scores):
            if(idx == 0):
                self.set_thumbnail(url=score.beatmap.cover_url)
            self.description += f"{idx+1}. {_score_to_desc_str(score)}\n\n"
