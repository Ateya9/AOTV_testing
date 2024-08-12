from random import sample, randint
from collections import Counter
from temple_room import TempleRoom
from temple import Temple, ValidRoomType


def run_t_always_upgrade(temple: Temple, **kwargs) -> Temple:
    """
    Run a temple, always upgrading rooms. Choose a random room type when upgrading un-tiered rooms.

    :param temple: The Temple object to run.
    :keyword aotv (bool): (default False) Whether Resource Reallocation is active.
    :keyword rr (bool): (default False) Whether Resource Reallocation is active.
    :return: The completed Temple object.
    """
    aotv = kwargs['aotv'] if 'aotv' in kwargs else False
    rr = kwargs['rr'] if 'rr' in kwargs else False
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            room_type = temple.get_room_upgrade_option()[0] if picked_room.type is None else picked_room.type
            temple.upgrade_room(picked_room, room_type, rr)
    temple.apply_nexus()
    return temple


def run_t_always_pick_target_rooms(temple: Temple, **kwargs):
    """
    Run a temple, always picking target rooms, otherwise just upgrading.

    :param temple: The Temple Object to run.
    :keyword target_rooms (list[ValidRoomType] | ValidRoomType): (default ValidRoomType.ITEM_DOUBLE_CORRUPT)
    The desired target rooms.
    :keyword aotv (bool): (default False) Whether Resource Reallocation is active.
    :keyword rr (bool): (default False) Whether Resource Reallocation is active.
    :return: The completed Temple object.
    """
    target_rooms = kwargs['target_rooms'] if 'target_rooms' in kwargs else [ValidRoomType.ITEM_DOUBLE_CORRUPT]
    aotv = kwargs['aotv'] if 'aotv' in kwargs else False
    rr = kwargs['rr'] if 'rr' in kwargs else False
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            room_upgrade_options = temple.get_room_upgrade_option(2 if picked_room.tier == 0 else 1)
            room_type = picked_room.type
            for target_room in target_rooms:
                if target_room in room_upgrade_options:
                    room_type = target_room
                else:
                    room_type = room_upgrade_options[0] if picked_room.type is None else picked_room.type
            temple.upgrade_room(room=picked_room, new_room_type=room_type, rr=rr)
    temple.apply_nexus()
    return temple


def calc_ratio_t3_rooms(run_method_func, num_runs: int = 100000, aotv: bool = False, rr: bool = False) -> float:
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
        current_temple = run_method_func(Temple(), aotv=aotv, rr=rr)
        temple_room_level_totals += Counter(list(map(int, current_temple)))
    ratio = round(temple_room_level_totals[3] / temple_room_level_totals.total(), 4)
    return ratio


def calc_ratio_target_t3_rooms(run_method_func,
                               target_rooms: list[ValidRoomType],
                               num_runs: int = 100000,
                               aotv: bool = False):
    # TODO: add parameter to control whether the temple starts with a desired room or not.
    """
    Calculate the ratio of T3 desired rooms in temples using the supplied function to run them. rr is assumed active.

    :param run_method_func: The function to use for running the temples.
    :param target_rooms: The desired target rooms.
    :param num_runs: How many temple runs to do.
    :param aotv: Whether Artefacts of the Vaal is active.
    :return: The ratio of T3 desired target rooms.
    """
    results = Counter()
    for _ in range(num_runs):
        current_temple: Temple = run_method_func(Temple(), target_rooms=target_rooms, aotv=aotv, rr=True)
        current_result: list[bool] = []
        for target_room in target_rooms:
            try:
                current_result.append(current_temple[target_room].tier == 3)
            except ValueError:
                current_result.append(False)
        results += Counter([True in current_result])
    return round(results[True] / results.total(), 4)


if __name__ == '__main__':
    print("### Ratios of T3 rooms when always upgrading:")
    print(f"WITHOUT Artefacts of the Vaal: 0.2576")
    print(f"WITH Artefacts of the Vaal: 0.2473")
    print(f"WITHOUT AOTV and WITH Resource Reallocation: 0.4856")
    print(f"WITH AOTV and WITH Resource Reallocation: 0.4798")

    print("### Ratios of T3 Item Double Corrupt:")
    print(f"Baseline WITHOUT AOTV: 0.2149")
    print(f"Baseline WITH AOTV: 0.2107")
    # print(f"Always Pick WITHOUT AOTV: ")
    # print(f"Always Pick WITH AOTV: ")

    # print("### Ratios of T3 rooms when always upgrading:")
    # print(f"WITHOUT Artefacts of the Vaal:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade)}")
    # print(f"WITH Artefacts of the Vaal:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade, aotv=True)}")
    # print(f"WITHOUT AOTV and WITH Resource Reallocation:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade, rr=True)}")
    # print(f"WITH AOTV and WITH Resource Reallocation:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade, aotv=True, rr=True)}")

    # print("### Ratios of T3 Item Double Corrupt:")
    # print(f"Baseline WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_upgrade,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Baseline WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_upgrade,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    print(f"Always Pick WITHOUT AOTV: "
          f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
                                        target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    print(f"Always Pick WITH AOTV: "
          f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
                                        target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
