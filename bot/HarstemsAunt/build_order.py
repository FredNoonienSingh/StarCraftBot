from enum import Enum
from typing import Union, List
from functools import cached_property

from .common import ALL_STRUCTURES, INITIAL_TECH, DT_TIMING,logger

from sc2.unit import Unit
from sc2.data import Race
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId


class InstructionType(Enum):
    UNIT_PRODUCTION = 1
    BUILD_STRUCTURE = 2

class Build(Enum):
    CANNON_RUSH = 1
    FOUR_GATE = 2


class BuildInstruction:
    """ Instruction for the Bot to build a structure, not sure yet how to add upgrades, and multiple instructions at once
    and how to take unit production into account, i already got a set of all Structures in .common maybe i just add every instruction
    including upgrades and unit production. """

    def __new__(cls,type_id:UnitTypeId,position:Union[Point2,Point3,Unit]=None,accuracy:int=0):
        instance = super().__new__(cls)
        instance.type_id = type_id
        # Position is only used when a Warpprism is present
        instance.position = position
        instance.accuracy = accuracy
        return instance

    def __init__(self,type_id:UnitTypeId, position:Union[Point2,Point3,Unit], accuracy:int=0) -> None:
        self.type_id = type_id
        self.position = position
        self.accuracy = accuracy

    @property
    def instruction_type(self) -> InstructionType:
        if self.type_id in ALL_STRUCTURES:
            return InstructionType.BUILD_STRUCTURE
        return InstructionType.UNIT_PRODUCTION

    def __repr__(self):
        if self.instruction_type == InstructionType.BUILD_STRUCTURE:
            return f"build {self.type_id} at {self.position}"
        if self.instruction_type == InstructionType.UNIT_PRODUCTION:
            return f"train {self.type_id}"


class BuildOrder:

    def __init__(self, bot:BotAI, build:Build=Build.FOUR_GATE):
        self.bot = bot
        self.build = build
        self.step = 0
        self.buffer = []

    @cached_property
    def enemy_race(self) -> Race:
        return self.bot.enemy_race

    @cached_property
    def instruction_list(self) -> List[BuildInstruction]:

        tech:List[UnitTypeId] = INITIAL_TECH.get(self.enemy_race)

        start_pos: Point2 = self.bot.start_location
        minerals:Units = self.bot.expansion_locations_dict[self.bot.start_location].mineral_field
        wall_buildings:list = list(self.bot.main_base_ramp.protoss_wall_buildings)
        wall_pylon_pos:Point2 = self.bot.main_base_ramp.protoss_wall_pylon
        tech_pylon_pos:Point2 = self.bot.start_location.towards(self.bot.start_location.furthest(minerals).position, 10)
        angle_pylon_pos:Point2 = self.bot.start_location.towards(self.bot.game_info.map_center,10)
        vespene_position_0:Point2 = self.bot.vespene_geyser.closer_than(12, start_pos)[0]
        vespene_position_1:Point2 = self.bot.vespene_geyser.closer_than(12, start_pos)[1]

        cannon_pylon_0: Point2 = self.bot.enemy_start_locations[0].towards(self.bot.game_info.map_center, 5)

        FOUR_GATE = [
            BuildInstruction(UnitTypeId.PYLON,wall_pylon_pos),
            BuildInstruction(UnitTypeId.GATEWAY,wall_buildings[0]),
            BuildInstruction(UnitTypeId.ASSIMILATOR,vespene_position_0),
            BuildInstruction(UnitTypeId.ASSIMILATOR,vespene_position_1),
            BuildInstruction(UnitTypeId.CYBERNETICSCORE,wall_buildings[1]),
            BuildInstruction(UnitTypeId.NEXUS, start_pos),
            BuildInstruction(UnitTypeId.PYLON,tech_pylon_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.GATEWAY, wall_pylon_pos,5),
            BuildInstruction(UnitTypeId.PYLON, angle_pylon_pos, 1),
            BuildInstruction(tech[0],tech_pylon_pos,5),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(tech[1],wall_pylon_pos.towards(self.bot.game_info.map_center),5),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(UnitTypeId.PYLON, angle_pylon_pos.towards(wall_pylon_pos,-6),5),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
        ]

        CANNON_RUSH = [
            BuildInstruction(UnitTypeId.PYLON,wall_pylon_pos),
            BuildInstruction(UnitTypeId.FORGE,wall_buildings[0]),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
        ]

        match self.build:
            case Build.CANNON_RUSH:
                return CANNON_RUSH
            case Build.FOUR_GATE:
                return FOUR_GATE

    @property
    def constructed_structures(self) -> List[UnitTypeId]:
        return []

    @property
    def opponent_builds_air(self) -> bool:
        return False

    @opponent_builds_air.setter
    def opponent_builds_air(self, status:bool) -> None:
        self.opponent_builds_air = status

    @property
    def opponent_uses_cloak(self) -> bool:
        return False

    @opponent_uses_cloak.setter
    def opponent_uses_cloak(self, status:bool) -> None:
        self.opponent_uses_cloak = status

    @property
    def opponent_has_detection(self) -> bool:
        return False

    @opponent_has_detection.setter
    def opponent_has_detection(self, status:bool) -> None:
        # for some reason is this causing max iter-depth issues
        self.opponent_has_detection = status

    def increment_step(self) -> None:
        self.step = self.step + 1

    def add_constructed_structure(self, structure:UnitTypeId) -> None:
        self.constructed_structures.append(structure)

    def get_build_pos(self) -> Union[Point2, Point3, Unit]:
        if len(self.instruction_list) > self.step:
            return self.instruction_list[self.step].position
        last_pylon:Unit = self.bot.structures(UnitTypeId.PYLON).sorted(lambda struct: struct.age)[0]
        return last_pylon.position.towards_with_random_angle(self.bot.game_info.map_center)

    async def update(self):

        if self.build == "cannon":
            if self.bot.structures(UnitTypeId.PYLON)\
                .filter(lambda struct: struct.distance_to(self.bot.enemy_start_locations[0]) < 12):
                self.buffer.append(UnitTypeId.PYLON)
            else:
                self.buffer.append(UnitTypeId.PHOTONCANNON)
            return 

        #TODO: ADD Conditions under which more Economy gets added to the Build
        #TODO: #66 ADD Conditions for advanced Tech -> such as fleet beacon ...
        if self.opponent_builds_air and not self.bot.structures(UnitTypeId.STARGATE):
            self.instruction_list.append(BuildInstruction(UnitTypeId.STARGATE,self.get_build_pos()))

        if self.bot.time > DT_TIMING:
            if not self.opponent_has_detection and not self.bot.structures(UnitTypeId.DARKSHRINE)\
                and UnitTypeId.DARKSHRINE not in self.buffer:
                self.buffer.append(UnitTypeId.DARKSHRINE)

        #self.debug_build_pos(self.get_build_pos())
        self.bot.client.debug_text_screen(f"{self.next_instruction()} instruction {self.step}", \
            (0.01, 0.15), color=(255,255,255), size=15)
        self.bot.client.debug_text_screen(f"next struct in Buffer: {self.get_next_in_buffer()}", \
            (0.01, 0.20), color=(255,255,255), size=15)

    def debug_build_pos(self, pos:Union[Point2, Point3]):
        z = self.bot.get_terrain_z_height(pos)+1
        x,y = pos.x, pos.y
        pos_3d = Point3((x,y,z))
        self.bot.client.debug_sphere_out(pos_3d ,1, (255,255,0))

    def get_next_in_buffer(self) -> UnitTypeId:
        if self.buffer:
            return self.buffer[0]

    def get_instruction_from_buffer(self) -> BuildInstruction:
        structure_type:UnitTypeId = self.buffer[0]
        build_pos:Point2 = self.get_build_pos()
        accuracy:int = 10
        instruction:BuildInstruction = BuildInstruction(structure_type,build_pos,accuracy)
        return instruction

    def remove_from_buffer(self,structure:UnitTypeId) -> None:
        self.buffer.remove(structure)

    def next_instruction(self) -> BuildInstruction:
        if len(self.instruction_list) > self.step:
            return self.instruction_list[self.step]
