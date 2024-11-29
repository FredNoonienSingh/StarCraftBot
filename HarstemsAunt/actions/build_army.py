
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from utils.can_build import can_build_unit

async def build_gateway_units(bot:BotAI,unit_type:UnitTypeId):
    if can_build_unit(bot, unit_type):
        for gate in bot.structures(UnitTypeId.GATEWAY):
            gate.train(unit_type)

async def build_stargate_units(bot:BotAI, unit_type:UnitTypeId):
    if can_build_unit(bot, unit_type):
        for gate in bot.structures(UnitTypeId.STARGATE):
            gate.train(unit_type)

async def build_robo_units(bot:BotAI, unit_type:UnitTypeId):
    if can_build_unit(bot, unit_type):
        for robo in bot.structures(UnitTypeId.ROBOTICSFACILITY):
            robo.train(unit_type)