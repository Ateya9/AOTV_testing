from random import sample, randint
from collections import Counter


def gen_temple(num_temple_rooms: int = 11) -> list:
    temple: list[int] = [0] * num_temple_rooms
    for room_num in sample(range(num_temple_rooms), 7):  # Set up 7 random rooms to be tier 1 already.
        temple[room_num] += 1
    return temple


def run_temple_always_upgrade(temple: list, aotv: bool = False, rr: bool = False) -> list:
    num_temple_rooms = len(temple)
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        available_rooms = [ele for ele in range(num_temple_rooms) if temple[ele] < 3]  # Rooms that aren't maxed.
        for i in sample(available_rooms, incurs_per_area):
            temple[i] += 1
    return temple


if __name__ == '__main__':
    temple_room_level_totals = Counter()
    for i in range(100000):
        temple_room_level_totals += Counter(run_temple_always_upgrade(gen_temple()))
    vanilla_t3_room_ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    print(f"Ratio of t3 rooms WITHOUT Artefacts of the Vaal: {vanilla_t3_room_ratio}")

    temple_room_level_totals = Counter()
    for i in range(100000):
        temple_room_level_totals += Counter(run_temple_always_upgrade(gen_temple(), True))
    aotv_t3_room_ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    print(f"Ratio of t3 rooms WITH Artefacts of the Vaal: {aotv_t3_room_ratio}")
