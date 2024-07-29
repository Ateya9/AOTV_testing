from random import sample
from collections import Counter


def gen_new_temple_run(incurs_per_area: int = 3, num_areas: int = 4) -> list:
    num_temple_rooms = 11
    temple: list[int] = [0] * num_temple_rooms
    for i in sample(range(num_temple_rooms), 7):  # Set up 7 random rooms to be tier 1 already.
        temple[i] += 1
    for _ in range(num_areas):
        available_rooms = [ele for ele in range(num_temple_rooms) if temple[ele] < 3]  # Rooms that aren't maxed.
        for i in sample(available_rooms, incurs_per_area):
            temple[i] += 1
    return temple


if __name__ == '__main__':
    temple_room_level_totals = Counter()
    for i in range(100000):
        temple_room_level_totals += Counter(gen_new_temple_run())
    vanilla_t3_room_ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    print(f"Ratio of t3 rooms WITHOUT Artefacts of the Vaal: {vanilla_t3_room_ratio}")

    temple_room_level_totals = Counter()
    for i in range(100000):
        temple_room_level_totals += Counter(gen_new_temple_run(4, 3))
    aotv_t3_room_ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    print(f"Ratio of t3 rooms WITH Artefacts of the Vaal: {aotv_t3_room_ratio}")
