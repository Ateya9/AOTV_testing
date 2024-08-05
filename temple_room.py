class TempleRoom:
    def __init__(self, room_tier: int = 0, room_type: str = "un-tiered"):
        """
        An object that represents a room within a temple of Atzoatl.
        :param room_tier: The tier of this room. Defaults to 0. Should always be positive.
        :param room_type: The type for this room. Defaults to 'un-tiered'
        """
        self.room_tier = room_tier
        self.room_type = room_type
        self.connections: list[TempleRoom] = []

    def __int__(self) -> int:
        return int(self.room_tier)

    def __add__(self, other):
        return TempleRoom(self.room_tier + int(other), self.room_type)

    def __iadd__(self, other):
        self.room_tier = self.room_tier + int(other)
        return self

    def __eq__(self, other):
        if isinstance(other, int):
            return self.room_tier == other
        elif isinstance(other, TempleRoom):
            return self.room_tier == other.room_tier and self.room_type == other.room_type
        return False

    def __repr__(self):
        return f'TempleRoom({self.room_tier}, "{self.room_type}")'

    def __str__(self):
        return f'T{self.room_tier} {self.room_type}'
