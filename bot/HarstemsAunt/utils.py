import math
import numpy as np

from typing import Union, Iterable

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

class Utils:

    @staticmethod
    def and_or(a:any, b:any)-> bool:
        return a or b or (a and b)

    @staticmethod
    def can_build_structure(bot:BotAI, structure_id:UnitTypeId)->bool:
        return bot.can_afford(structure_id) and bot.tech_requirement_progress(structure_id)

    @staticmethod
    def can_build_unit(bot:BotAI, unit_id:UnitTypeId) ->bool:
        return bot.can_afford(unit_id) and bot.can_feed(unit_id) and bot.tech_requirement_progress(unit_id)

    @staticmethod
    def can_research_upgrade(bot:BotAI,upgrade_id:UpgradeId)->bool:
        return bot.can_afford(upgrade_id) and not bot.already_pending_upgrade(upgrade_id)\
            and bot.tech_requirement_progress(upgrade_id)

    @staticmethod
    def get_army_target(bot:BotAI) -> Union[Point2, Point3]:
        if bot.enemy_units:
            return bot.enemy_units.center
        else:
            return bot.enemy_start_locations[0]

    @staticmethod
    def check_position(bot:BotAI) -> bool:
        if bot.units.filter(lambda unit: unit.distance_to(bot.last_enemy_army_pos) < unit.sight_range):
                return True
        return False

    @staticmethod
    def get_intersection(p0: Point2, r0: float, p1:Point2, r1:float) -> Iterable[Point2]:
        p01 = p1 - p0
        d = np.linalg.norm(p01)
        if d == 0:
            return  # intersection is empty or infinite
        if d < abs(r0 - r1):
                return  # circles inside of each other
        if r0 + r1 < d:
            return  # circles too far apart
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        pm = p0 + (a / d) * p01
        po = (h / d) * np.array([p01.y, -p01.x])
        yield pm + po
        yield pm - po

    @staticmethod
    def get_build_pos(bot:BotAI) -> Union[Point2, Point3, Unit]:
        if not bot.structures(UnitTypeId.PYLON):
            return bot.main_base_ramp.protoss_wall_pylon
        elif not bot.structures(UnitTypeId.GATEWAY) and not bot.already_pending(UnitTypeId.GATEWAY):
                return bot.main_base_ramp.protoss_wall_warpin
        else:
            return bot.structures(UnitTypeId.NEXUS)[0].position3d.towards(bot.game_info.map_center, 5)

    @staticmethod
    def get_warp_in_pos(bot:BotAI) -> Union[Point2, Point3, Unit]:
        if not bot.units(UnitTypeId.WARPPRISM):
            if bot.supply_army > 10:
                return bot.structures(UnitTypeId.PYLON).in_closest_distance_to_group([x for x in bot.units if x not in bot.workers])
            else:
                return bot.structures(UnitTypeId.PYLON).closest_to(bot.enemy_start_locations[0]).position.towards(bot.enemy_start_locations[0], distance=1, limit=False)
        else:
            if bot.enemy_units:
                active_prism = bot.units(UnitTypeId.WARPPRISM).closest_to(bot.enemy_units.center)
            else:
                active_prism = bot.units(UnitTypeId.WARPPRISM).closest_to(bot.enemy_start_locations[0]) 
            return active_prism.position

    @staticmethod
    def structure_in_proximity(bot:BotAI, structure_type:UnitTypeId, structure:Unit, max_distance:float)-> bool:
        if bot.structures(structure_type).filter(lambda struct: struct.distance_to(structure)<max_distance):
            return True
        return False

    @staticmethod
    def unit_in_proximity(bot:BotAI, unit_type:UnitTypeId, unit:Unit, max_distance:float) ->bool:
        if bot.units(unit_type).filter(lambda struct: struct.distance_to(unit)<max_distance):
            return True
        return False

    @staticmethod
    def in_proximity_to_point(unit:Unit, point:Union[Point2, Point3], max_distance:float) -> bool:
        return unit.distance_to(point) < max_distance

    @staticmethod
    def is_close_to_unit(unit_1:Unit, unit_2:Unit, max_distance:float) -> bool:
        return unit_1.distance_to(unit_2) <= max_distance