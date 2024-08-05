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
        self.room_types_remaining = Temple._valid_room_types.copy()
        self.rooms: list[TempleRoom] = []
        for _ in range(11):
            self.rooms.append(TempleRoom())
        rooms_to_tier = sample(self.rooms, num_starting_tiered_rooms)
        rooms_to_tier_types = sample(self._valid_room_types, num_starting_tiered_rooms)
        for i in range(len(rooms_to_tier)):
            rooms_to_tier[i] += 1
            rooms_to_tier[i].room_type = rooms_to_tier_types[i]
            self.room_types_remaining.remove(rooms_to_tier_types[i])
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
