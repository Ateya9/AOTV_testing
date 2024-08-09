from temple_room import TempleRoom
from random import sample
from enum import Enum


class ValidRoomType(Enum):
    UNIQUE_SACRIFICE = "Unique Sacrifice"
    BODY_ARMOURS = "Body Armours"
    JEWELLERY = "Jewellery"
    PACK_SIZE = "Pack Size"
    MINIONS = "Minions"
    CURRENCY = "Currency"
    MONSTER_REGEN = "Monster Regen"
    EXPLOSIVES = "Explosives"
    ITEM_QUANTITY = "Item Quantity"
    ITEMS = "Items"
    TRAPS = "Traps"
    MONOLITH = "Monolith"
    ITEM_DOUBLE_CORRUPT = "Item Double Corrupt"
    FIRE = "Fire"
    ADJACENT_ROOM_LEVELS = "Adjacent Room Levels"
    POISON = "Poison"
    WEAPONS = "Weapons"
    TEMPESTS = "Tempests"
    TORMENTED_SPIRITS = "Tormented Spirits"
    MAPS = "Maps"
    ATZIRI = "Atziri"
    LIGHTNING = "Lightning"
    GEM_DOUBLE_CORRUPT = "Gem Double Corrupt"
    STRONGBOXES = "Strongboxes"
    BREACH = "Breach"


class Temple:
    def __init__(self, num_starting_tiered_rooms: int = 7,
                 desired_room: None | ValidRoomType = None,
                 start_with_desired_room: bool = False):
        """
        An object representing a temple of Atzoatl.
        :param num_starting_tiered_rooms: How many rooms to start at tier 1.
        :param desired_room: The desired T3 room for this Temple.
        :param start_with_desired_room: controls whether this temple starts with a T1 version of the desired room.
        """
        self._room_types_remaining = list(ValidRoomType)
        self.rooms: list[TempleRoom] = []
        for _ in range(11):
            self.rooms.append(TempleRoom())
        rooms_to_tier = sample(range(len(self.rooms)), num_starting_tiered_rooms)
        rooms_to_tier_types: list[ValidRoomType] = []
        starting_room_types_remaining = self._room_types_remaining.copy()
        if desired_room is not None:
            if start_with_desired_room:
                rooms_to_tier_types.append(desired_room)
                num_starting_tiered_rooms -= 1
            starting_room_types_remaining.remove(desired_room)
        rooms_to_tier_types.extend(sample(starting_room_types_remaining, num_starting_tiered_rooms))
        for room_num in rooms_to_tier:
            self.upgrade_room(room_num, rooms_to_tier_types[0])
            rooms_to_tier_types.pop(0)
        self.rooms[0].connections = [self.rooms[i] for i in (2, 3)]
        self.rooms[1].connections = [self.rooms[i] for i in (4, 5)]
        self.rooms[2].connections = [self.rooms[i] for i in (0, 3, 6)]
        self.rooms[3].connections = [self.rooms[i] for i in (0, 2, 4, 6, 7)]
        self.rooms[4].connections = [self.rooms[i] for i in (1, 3, 5, 7, 8)]
        self.rooms[5].connections = [self.rooms[i] for i in (1, 4, 8)]
        self.rooms[6].connections = [self.rooms[i] for i in (2, 3, 7, 9)]
        self.rooms[7].connections = [self.rooms[i] for i in (3, 4, 6, 8, 9, 10)]
        self.rooms[8].connections = [self.rooms[i] for i in (4, 5, 7, 10)]
        self.rooms[9].connections = [self.rooms[i] for i in (6, 7, 10)]
        self.rooms[10].connections = [self.rooms[i] for i in (7, 8, 9)]

    @property
    def valid_room_types_remaining(self) -> list[ValidRoomType]:
        """
        Returns a list of valid room types that aren't currently present within this temple.

        :return: list[str]
        """
        return self._room_types_remaining

    @property
    def valid_rooms_remaining(self) -> list[TempleRoom]:
        """
        Returns a list of rooms that aren't T3.

        :return: list[TempleRoom]
        """
        return [room for room in self.rooms if room.tier < 3]

    def get_room_upgrade_option(self) -> ValidRoomType:
        """
        Returns a single room type that currently isn't present within this temple to act as a non-resident upgrade
        option.

        :return: str
        """
        return sample(self._room_types_remaining, 1)[0]

    def upgrade_room(self, room: int | TempleRoom, new_room_type: ValidRoomType):
        """
        Upgrades the specified room tier and type.

        Raises IndexError if room is invalid.
        Raises ValueError if room_type is already present in temple.

        :param room: The room or room number to upgrade.
        :param new_room_type: The room type for this room to be changed to.

        :return: None
        """
        if isinstance(room, int):
            if 0 > room >= len(self.rooms):
                raise IndexError(f"room must be between 0 and {len(self.rooms) - 1}.")
            room = self.rooms[room]
        elif room not in self:
            raise IndexError('room does not exist in this temple.')
        if new_room_type not in ValidRoomType:
            raise TypeError("new_room_type must be a valid room type.")
        if new_room_type != room.type and new_room_type not in self._room_types_remaining:
            raise ValueError(f"room_type already present in temple.")
        if room.tier == 3:
            raise IndexError(f"Invalid room. Room is already tier 3.")

        if room.type is None:
            self._room_types_remaining.remove(new_room_type)
        elif new_room_type != room.type:
            self._room_types_remaining[self._room_types_remaining.index(new_room_type)] = room.type
        room += 1
        room.type = new_room_type

    def apply_nexus(self):
        """
        Updates the room tiers adjacent to an "Adjacent Room Levels" room. This should be called when a temple run is
        finished.

        :return: None
        """
        nexus_room: TempleRoom
        try:
            nexus_room_index = [room.type for room in self.rooms].index(ValidRoomType.ADJACENT_ROOM_LEVELS)
            nexus_room = self.rooms[nexus_room_index]
        except ValueError:
            return
        connections_to_upgrade = [room for room in nexus_room.connections if room.tier > 0]
        if len(connections_to_upgrade) == 0:
            return
        if 3 > nexus_room.tier < len(connections_to_upgrade):
            connections_to_upgrade = sample(connections_to_upgrade, nexus_room.tier)
        for room in connections_to_upgrade:
            room += 1 if room.tier < 3 else 0

    def __len__(self):
        return len(self.rooms)

    def __iter__(self):
        yield from self.rooms

    def __getitem__(self, item):
        return self.rooms[item]

    def __setitem__(self, key, value):
        self.rooms[key] = value

    def __contains__(self, item: ValidRoomType):
        return item in [room.type for room in self.rooms]


if __name__ == "__main__":
    temple = Temple()
    print(temple.rooms)
