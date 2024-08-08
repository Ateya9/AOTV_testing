from temple_room import TempleRoom
from random import sample


class Temple:
    _valid_room_types: list[str] = [
        "Unique Sacrifice",
        "Body Armours",
        "Jewellery",
        "Pack Size",
        "Minions",
        "Currency",
        "Monster Regen",
        "Explosives",
        "Item Quantity",
        "Items",
        "Traps",
        "Monolith",
        "Item Double Corrupt",
        "Fire",
        "Adjacent Room Levels",
        "Poison",
        "Weapons",
        "Tempests",
        "Tormented Spirits",
        "Maps",
        "Atziri",
        "Lightning",
        "Gem Double Corrupt",
        "Strongboxes",
        "Breach"
    ]

    def __init__(self, num_starting_tiered_rooms: int = 7):
        """
        An object representing a temple of Atzoatl.
        :param num_starting_tiered_rooms: How many rooms to start at tier 1.
        """
        self._room_types_remaining = Temple._valid_room_types.copy()
        self.rooms: list[TempleRoom] = []
        for _ in range(11):
            self.rooms.append(TempleRoom())
        rooms_to_tier = sample(self.rooms, num_starting_tiered_rooms)
        rooms_to_tier_types = sample(self._valid_room_types, num_starting_tiered_rooms)
        for i in range(len(rooms_to_tier)):
            rooms_to_tier[i] += 1
            rooms_to_tier[i].room_type = rooms_to_tier_types[i]
            self._room_types_remaining.remove(rooms_to_tier_types[i])
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
    def room_types_remaining(self) -> list[str]:
        return self._room_types_remaining

    def get_room_upgrade_option(self) -> str:
        return sample(self._room_types_remaining, 1)[0]

    def upgrade_room(self, room_num: int, room_type: str):
        if 0 > room_num >= len(self.rooms):
            raise IndexError(f"room must be between 0 and {len(self.rooms) - 1}")
        current_room_type = self.rooms[room_num].room_type
        if room_type != current_room_type and room_type not in self._room_types_remaining:
            raise ValueError(f"room_type already present in temple.")
        if self.rooms[room_num].room_tier == 3:
            raise IndexError(f"Invalid room. Room is already tier 3.")

        if room_type != current_room_type:
            self._room_types_remaining[self._room_types_remaining.index(room_type)] = current_room_type
        self.rooms[room_num] += 1
        self.rooms[room_num].room_type = room_type

    def apply_nexus(self):
        nexus_room: TempleRoom
        try:
            nexus_room_index = [room.room_type for room in self.rooms].index("Adjacent Room Levels")
            nexus_room = self.rooms[nexus_room_index]
        except ValueError:
            return
        valid_connections = [room for room in nexus_room.connections if room.room_type != "un-tiered"]
        connections_to_upgrade = valid_connections
        if len(valid_connections) == 0:
            return
        if nexus_room.room_tier != 3:
            connections_to_upgrade = sample(valid_connections, nexus_room.room_tier)
        for room in connections_to_upgrade:
            room += 1 if room.room_tier < 3 else 0

    def __len__(self):
        return len(self.rooms)

    def __iter__(self):
        yield from self.rooms

    def __getitem__(self, item):
        return self.rooms[item]

    def __setitem__(self, key, value):
        self.rooms[key] = value


if __name__ == "__main__":
    temple = Temple()
