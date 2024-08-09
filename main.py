from random import sample, randint
from collections import Counter
from temple_room import TempleRoom
from temple import Temple


def run_temple_always_upgrade(temple: Temple, aotv: bool = False, rr: bool = False) -> Temple:
    num_temple_rooms = len(temple)
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    available_rooms = list(range(num_temple_rooms))
    for _ in range(num_areas):
        for picked_room in sample(available_rooms, incurs_per_area):
            if rr and temple[picked_room] == 1:
                temple[picked_room] += randint(0, 1)
            temple[picked_room] += 1
            if temple[picked_room] == 3:
                available_rooms.remove(picked_room)
    temple.apply_nexus()
    return temple


def calc_results(run_method_func, num_runs: int = 100000, aotv: bool = False, rr: bool = False) -> float:
    temple_room_level_totals = Counter()
    for _ in range(num_runs):
        current_temple = run_method_func(Temple(), aotv, rr)
        temple_room_level_totals += Counter(list(map(int, current_temple)))
    ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    return ratio


if __name__ == '__main__':
    print(f"Ratio of t3 rooms WITHOUT Artefacts of the Vaal: 0.2507")
    print(f"Ratio of t3 rooms WITH Artefacts of the Vaal: 0.2397")
    print(f"Ratio of t3 rooms WITHOUT AOTV and WITH Resource Reallocation: 0.4812")
    print(f"Ratio of t3 rooms WITH AOTV and WITH Resource Reallocation: 0.4749")
    # print(f"Ratio of t3 rooms WITHOUT Artefacts of the Vaal: {calc_results(run_temple_always_upgrade)}")
    # print(f"Ratio of t3 rooms WITH Artefacts of the Vaal: {calc_results(run_temple_always_upgrade, aotv=True)}")
    # print(f"Ratio of t3 rooms WITHOUT AOTV and WITH Resource Reallocation: "
    #       f"{calc_results(run_temple_always_upgrade, rr=True)}")
    # print(f"Ratio of t3 rooms WITH AOTV and WITH Resource Reallocation: "
    #       f"{calc_results(run_temple_always_upgrade, aotv=True, rr=True)}")
