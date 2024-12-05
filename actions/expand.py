
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

async def expand(bot:BotAI):
    if not bot.already_pending(UnitTypeId.NEXUS) and len(bot.structures(UnitTypeId.NEXUS))<bot.base_count:
        await bot.expand_now()