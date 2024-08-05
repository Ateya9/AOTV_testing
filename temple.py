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
