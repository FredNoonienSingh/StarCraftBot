"""
    MainClass of the Bot handling
"""
from common import MAP_LIST
from random import choice


"""SC2 Imports"""
from sc2 import maps
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer, Human
from sc2.ids.unit_typeid import UnitTypeId

"""Actions"""
from actions.expand import expand
from actions.build_supply import build_supply
from actions.build_structure import build_structure, build_gas
from actions.build_army import build_gateway_units, build_stargate_units, build_robo_units

"""Utils"""
from utils.get_build_pos import get_build_pos
from utils.can_build import can_build_unit, can_build_structure, can_research_upgrade

class HarstemsAunt(BotAI):

    def __init__(self, debug:bool=False) -> None:
        self.race:Race = Race.Protoss
        self.name:str = "HarstemsAunt"
        self.version:str = "0.1"
        self.debug:bool = debug
        self.gateway_count = 1

    async def on_start(self):
        pass

    async def on_step(self, iteration):
        if self.townhalls and self.units:
            for townhall in self.townhalls:
                if townhall.is_ready and self.structures(UnitTypeId.PYLON):
                    await build_gas(self, townhall)
                if townhall.is_idle and can_build_unit(self, UnitTypeId.PROBE):
                    townhall.train(UnitTypeId.PROBE)
                await self.distribute_workers(resource_ratio=2)

            build_pos = get_build_pos(self)
            worker = self.workers.prefer_idle.closest_to(build_pos)

            if not self.structures(UnitTypeId.PYLON) and can_build_structure(self, UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, build_worker=worker, near=build_pos, max_distance=0)
            if len(self.structures(UnitTypeId.GATEWAY))<self.gateway_count and can_build_structure(self, UnitTypeId.GATEWAY):
                await self.build(UnitTypeId.GATEWAY, build_worker=worker, near=build_pos)
            if not self.structures(UnitTypeId.CYBERNETICSCORE) and len(self.structures(UnitTypeId.NEXUS))==2:
                await build_structure(self, UnitTypeId.CYBERNETICSCORE, build_pos, worker)
            if not self.structures(UnitTypeId.TWILIGHTCOUNCIL) and not self.already_pending(UnitTypeId.TWILIGHTCOUNCIL):
                await build_structure(self, UnitTypeId.TWILIGHTCOUNCIL, build_pos, worker)

            await build_gateway_units(self, UnitTypeId.STALKER)
            await build_supply(self, build_pos)
            await expand(self)

            for stalker in self.units(UnitTypeId.STALKER):
                stalker.attack(self.enemy_start_locations[0])
            return
        await self.client.leave()
    
    async def on_building_construction_complete(self, unit):
        if unit.name == "Nexus":
            self.gateway_count += 2

    async def on_end(self,game_result):
        await self.client.leave()

if __name__ == "__main__":
    AiPlayer = HarstemsAunt()
    races:list = [
        Race.Terran,
        Race.Zerg,
        Race.Protoss
    ]
    enemy:Race = choice(races)
    run_game(maps.get(choice(MAP_LIST)),
             [
                 Bot(AiPlayer.race, HarstemsAunt(debug=True)),
                 Computer(enemy, difficulty=(Difficulty.Hard))
             ],
             realtime=False
        )
