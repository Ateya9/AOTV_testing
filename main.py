from random import sample, randint
from collections import Counter
from temple_room import TempleRoom
from temple import Temple, ValidRoomType


def run_temple_always_upgrade(temple: Temple, aotv: bool = False, rr: bool = False) -> Temple:
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            room_type = temple.get_room_upgrade_option()[0] if picked_room.type is None else picked_room.type
            temple.upgrade_room(picked_room, room_type, rr)
    temple.apply_nexus()
    return temple


def calc_results(run_method_func, num_runs: int = 100000, aotv: bool = False, rr: bool = False) -> float:
    temple_room_level_totals = Counter()
    for _ in range(num_runs):
        current_temple = run_method_func(Temple(), aotv, rr)
        temple_room_level_totals += Counter(list(map(int, current_temple)))
    ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    return ratio


def calc_results_specific_room(run_method_func, target_room: ValidRoomType, num_runs: int = 100000, aotv: bool = False):
    results = Counter()
    for _ in range(num_runs):
        current_temple: Temple = run_method_func(Temple(), aotv, True)
        try:
            current_result = current_temple[target_room].tier == 3
        except ValueError:
            current_result = False
        results += Counter([current_result])
    return round(results[True] / results.total(), 4)


if __name__ == '__main__':
    print("Ratios for T3 rooms when always upgrading:")
    print(f"WITHOUT Artefacts of the Vaal: 0.2572")
    print(f"WITH Artefacts of the Vaal: 0.2462")
    print(f"WITHOUT AOTV and WITH Resource Reallocation: 0.4853")
    print(f"WITH AOTV and WITH Resource Reallocation: 0.4798")
    # print(f"WITHOUT Artefacts of the Vaal: {calc_results(run_temple_always_upgrade)}")
    # print(f"WITH Artefacts of the Vaal: {calc_results(run_temple_always_upgrade, aotv=True)}")
    # print(f"WITHOUT AOTV and WITH Resource Reallocation: "
    #       f"{calc_results(run_temple_always_upgrade, rr=True)}")
    # print(f"WITH AOTV and WITH Resource Reallocation: "
    #       f"{calc_results(run_temple_always_upgrade, aotv=True, rr=True)}")
    print("Ratios for T3 Item Double Corrupt:")
    # print(f"WITHOUT AOTV: {}")
    # print(f"WITH AOTV: {}")
    print(f"WITHOUT AOTV: "
          f"{calc_results_specific_room(run_temple_always_upgrade, ValidRoomType.ITEM_DOUBLE_CORRUPT)}")
    print(f"WITH AOTV: "
          f"{calc_results_specific_room(run_temple_always_upgrade, ValidRoomType.ITEM_DOUBLE_CORRUPT, aotv=True)}")
