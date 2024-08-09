class TempleRoom:
    def __init__(self, room_tier: int = 0, room_type=None):
        """
        An object that represents a room within a temple of Atzoatl.
        :param room_tier: The tier of this room. Defaults to 0. Should always be positive.
        :param room_type: The type for this room. Defaults to None
        """
        self.tier = room_tier
        self.type = room_type
        self.connections: list[TempleRoom] = []

    def __int__(self) -> int:
        return int(self.tier)

    def __add__(self, other):
        return TempleRoom(self.tier + int(other), self.type)

    def __iadd__(self, other):
        self.tier = self.tier + int(other)
        return self

    def __eq__(self, other):
        if isinstance(other, int):
            return self.tier == other
        elif isinstance(other, TempleRoom):
            return self.tier == other.tier and self.type == other.type
        return False

    def __repr__(self):
        if self.type is None:
            return f'TempleRoom()'
        return f'TempleRoom({self.tier}, "{self.type}")'

    def __str__(self):
        if self.type is None:
            return f'un-tiered'
        return f'T{self.tier} {self.type}'
