from random import sample, randint
from collections import Counter
from temple_room import TempleRoom
from temple import Temple, ValidRoomType


def run_temple_always_upgrade(temple: Temple, aotv: bool = False, rr: bool = False) -> Temple:
    """
    Run a temple, always upgrading rooms. Choose a random room type when upgrading un-tiered rooms.

    :param temple: The Temple object to run.
    :param aotv: Whether Artefacts of the Vaal is active.
    :param rr: Whether Resource Reallocation is active.
    :return: The completed Temple object.
    """
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            room_type = temple.get_room_upgrade_option()[0] if picked_room.type is None else picked_room.type
            temple.upgrade_room(picked_room, room_type, rr)
    temple.apply_nexus()
    return temple


def calc_results(run_method_func, num_runs: int = 100000, aotv: bool = False, rr: bool = False) -> float:
    """
    Calculate the ratio of T3 rooms in temples using the supplied function to run them, ignoring room types.

    :param run_method_func: The function to use for running the temples.
    :param num_runs: How many temple runs to do.
    :param aotv: Whether Artefacts of the Vaal is active.
    :param rr: Whether Resource Reallocation is active.
    :return: The ratio of T3 rooms.
    """
    temple_room_level_totals = Counter()
    for _ in range(num_runs):
        current_temple = run_method_func(Temple(), aotv, rr)
        temple_room_level_totals += Counter(list(map(int, current_temple)))
    ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    return ratio


def calc_results_specific_room(run_method_func, target_room: ValidRoomType, num_runs: int = 100000, aotv: bool = False):
    """
    Calculate the ratio of T3 desired rooms in temples using the supplied function to run them. rr is assumed active.

    :param run_method_func: The function to use for running the temples.
    :param target_room: The desired target room.
    :param num_runs: How many temple runs to do.
    :param aotv: Whether Artefacts of the Vaal is active.
    :return: The ratio of T3 desired target rooms.
    """
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
    print("### Ratios of T3 rooms when always upgrading:")
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
    print("### Ratios of T3 Item Double Corrupt:")
    print(f"Baseline WITHOUT AOTV: 0.2143")
    print(f"Baseline WITH AOTV: 0.211")
    # print(f"Baseline WITHOUT AOTV: "
    #       f"{calc_results_specific_room(run_temple_always_upgrade, ValidRoomType.ITEM_DOUBLE_CORRUPT)}")
    # print(f"Baseline WITH AOTV: "
    #       f"{calc_results_specific_room(run_temple_always_upgrade, ValidRoomType.ITEM_DOUBLE_CORRUPT, aotv=True)}")
