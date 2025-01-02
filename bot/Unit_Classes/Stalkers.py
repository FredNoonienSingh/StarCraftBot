from HarstemsAunt.common import logger
from Unit_Classes.baseClassGround import BaseClassGround

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2

from HarstemsAunt.pathing import Pathing
from HarstemsAunt.common import ATTACK_TARGET_IGNORE, MIN_SHIELD_AMOUNT,\
    ALL_STRUCTURES, PRIO_ATTACK_TARGET, WORKER_IDS


class Stalkers(BaseClassGround):
    """ Extension of BaseClassGround """

    async def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        grid: np.ndarray = self.pathing.ground_grid
        for stalker in units:
            
            
            # Keep out of Range, if Shields are low, removes to much supply from fights to fast
            #if stalker.shield_percentage < MIN_SHIELD_AMOUNT \
             #   and not self.pathing.is_position_safe(grid, stalker.position):
              #  self.move_to_safety(stalker, grid)
               # continue

            # When enemy_units are visible
            if self.bot.enemy_units:
                visible_units = self.bot.enemy_units.closer_than(stalker.ground_range+2, stalker)
                enemy_structs = self.bot.enemy_structures.closer_than(20, stalker)

                # Attack if Possible
                if stalker.weapon_ready:
                    if visible_units:
                        target = self.pick_enemy_target(visible_units, stalker)
                        stalker.attack(target)
                    if not visible_units and enemy_structs:
                        target = enemy_structs.closest_to(stalker)
                        stalker.attack(target)
                    if not visible_units and not enemy_structs:
                        stalker.attack(
                            self.pathing.find_path_next_point(
                            stalker.position, attack_target, grid
                            )
                        )

                # Move out of range if attacking is not possible
                elif not stalker.weapon_ready and visible_units:
                    threads = self.bot.enemy_units\
                        .filter(lambda Unit: Unit.distance_to(stalker) <= Unit.ground_range+1)
                    if threads:
                        if not self.pathing.is_position_safe(grid, stalker.position):
                            self.move_to_safety(stalker, grid)
                        else:
                            continue
                else:
                    stalker.attack(
                         self.pathing.find_path_next_point(
                        stalker.position, attack_target, grid
                    )
                    )
            else:
                stalker.attack(
                     self.pathing.find_path_next_point(
                        stalker.position, attack_target, grid
                    )
                )

    async def _do_blink(self):
        logger.info(f"BLINK is not yet implemented")