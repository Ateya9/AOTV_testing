from random import sample, randint
from collections import Counter
from temple_room import TempleRoom
from temple import Temple, ValidRoomType
from up_room_logic import (prio_upgrade_unless_target,
                           prio_sidegrade_unless_target,
                           prio_sidegrade_unless_target_no_t0)


def text_red(text, conditional: bool) -> str:
    """
    Surrounds the provided text with ANSI codes to make it red when printed. This is for debugging.

    :param text: What will be printed as a str.
    :param conditional: whether the text should be red.
    :return:
    """
    return '\033[91m' + str(text) + '\033[0m' if conditional else str(text)


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
            temple.upgrade_room(room=picked_room,
                                new_room_type=prio_upgrade_unless_target(temple=temple,
                                                                         room=picked_room,
                                                                         target_rooms=None),
                                rr=rr)
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
    if 'target_room' in kwargs:
        raise KeyError('invalid key target_room. Should be target_rooms.')
    target_rooms = kwargs['target_rooms'] if 'target_rooms' in kwargs else [ValidRoomType.ITEM_DOUBLE_CORRUPT]
    aotv = kwargs['aotv'] if 'aotv' in kwargs else False
    rr = kwargs['rr'] if 'rr' in kwargs else False
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            temple.upgrade_room(room=picked_room,
                                new_room_type=prio_upgrade_unless_target(temple=temple,
                                                                         room=picked_room,
                                                                         target_rooms=target_rooms),
                                rr=rr)
    temple.apply_nexus()
    return temple


def run_t_place_desired_room_on_t2_no_t0(temple: Temple, **kwargs) -> Temple:
    """
    Run a temple that is missing a desired room, prioritising getting rooms to t2 by side-grading them, and then
    hopefully hitting a desired room when landing on them a second time. Will (if possible) not pick a desired room as
    an upgrade option on a T0 room.

    :param temple: The Temple Object to run.
    :keyword target_rooms (list[ValidRoomType] | ValidRoomType): (default ValidRoomType.ITEM_DOUBLE_CORRUPT)
    The desired target rooms.
    :keyword aotv (bool): (default False) Whether Resource Reallocation is active.
    :keyword rr (bool): (default False) Whether Resource Reallocation is active.
    :return:
    """
    if 'target_room' in kwargs:
        raise KeyError('invalid key target_room. Should be target_rooms.')
    target_rooms = kwargs['target_rooms'] if 'target_rooms' in kwargs else [ValidRoomType.ITEM_DOUBLE_CORRUPT]
    aotv = kwargs['aotv'] if 'aotv' in kwargs else False
    rr = kwargs['rr'] if 'rr' in kwargs else False
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            temple.upgrade_room(room=picked_room,
                                new_room_type=prio_sidegrade_unless_target_no_t0(temple=temple,
                                                                                 room=picked_room,
                                                                                 target_rooms=target_rooms),
                                rr=rr)
    temple.apply_nexus()
    return temple


def run_t_place_desired_room_on_t2(temple: Temple, **kwargs) -> Temple:
    """
    Run a temple that is missing a desired room, prioritising getting rooms to t2 by side-grading them, and then
    hopefully hitting a desired room when landing on them a second time.

    :param temple: The Temple Object to run.
    :keyword target_rooms (list[ValidRoomType] | ValidRoomType): (default ValidRoomType.ITEM_DOUBLE_CORRUPT)
    The desired target rooms.
    :keyword aotv (bool): (default False) Whether Resource Reallocation is active.
    :keyword rr (bool): (default False) Whether Resource Reallocation is active.
    :return:
    """
    if 'target_room' in kwargs:
        raise KeyError('invalid key target_room. Should be target_rooms.')
    target_rooms = kwargs['target_rooms'] if 'target_rooms' in kwargs else [ValidRoomType.ITEM_DOUBLE_CORRUPT]
    aotv = kwargs['aotv'] if 'aotv' in kwargs else False
    rr = kwargs['rr'] if 'rr' in kwargs else False
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            temple.upgrade_room(room=picked_room,
                                new_room_type=prio_sidegrade_unless_target(temple=temple,
                                                                           room=picked_room,
                                                                           target_rooms=target_rooms),
                                rr=rr)
    temple.apply_nexus()
    return temple


def run_t_prio_t2_until_target_exists(temple: Temple, **kwargs) -> Temple:
    """
    Run a temple that is missing a desired room, prioritising getting rooms to t2 by side-grading them, and then
    hopefully hitting a desired room when landing on them a second time. Once a target room exists in the temple,
    prioritise upgrading rooms instead of side-grading rooms, Even if target room was upgraded from a t0 room.

    :param temple: The Temple Object to run.
    :keyword target_rooms (list[ValidRoomType] | ValidRoomType): (default ValidRoomType.ITEM_DOUBLE_CORRUPT)
    The desired target rooms.
    :keyword aotv (bool): (default False) Whether Resource Reallocation is active.
    :keyword rr (bool): (default False) Whether Resource Reallocation is active.
    :return:
    """
    if 'target_room' in kwargs:
        raise KeyError('invalid key target_room. Should be target_rooms.')
    target_rooms = kwargs['target_rooms'] if 'target_rooms' in kwargs else [ValidRoomType.ITEM_DOUBLE_CORRUPT]
    aotv = kwargs['aotv'] if 'aotv' in kwargs else False
    rr = kwargs['rr'] if 'rr' in kwargs else False
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    incurs_per_area, num_areas = (4, 3) if aotv else (3, 4)
    for _ in range(num_areas):
        for picked_room in sample(temple.valid_rooms_remaining, incurs_per_area):
            target_exists = any([target_room not in temple.valid_room_types_remaining for target_room in target_rooms])
            decision_type = prio_upgrade_unless_target if target_exists else prio_sidegrade_unless_target
            temple.upgrade_room(room=picked_room,
                                new_room_type=decision_type(temple=temple, room=picked_room, target_rooms=target_rooms),
                                rr=rr)
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
                               initial_room: ValidRoomType | None = None,
                               start_with_initial_room: bool = False,
                               num_runs: int = 100000,
                               aotv: bool = False):
    """
    Calculate the ratio of T3 desired rooms in temples using the supplied function to run them. rr is assumed active.

    :param run_method_func: The function to use for running the temples.
    :param target_rooms: The desired target rooms.
    :param initial_room: Which room to start the temple with or not, depending on start_with_initial_room.
    :param start_with_initial_room: Controls whether the room specified by initial_room starts in the temple.
    :param num_runs: How many temple runs to do.
    :param aotv: Whether Artefacts of the Vaal is active.
    :return: The ratio of T3 desired target rooms.
    """
    results = Counter()
    for _ in range(num_runs):
        if initial_room:
            temple = Temple(desired_room=initial_room, start_with_desired_room=start_with_initial_room)
        else:
            temple = Temple()
        current_temple: Temple = run_method_func(temple, target_rooms=target_rooms, aotv=aotv, rr=True)
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

    print("")
    print("### Ratios of T3 Item Double Corrupt:")
    print(f"Baseline WITHOUT AOTV: 0.2149")
    print(f"Baseline WITH AOTV: 0.2107")
    print(f"Baseline, always pick target room WITHOUT AOTV: 0.3955")
    print(f"Baseline, always pick target room WITH AOTV: 0.3815")
    print(f"Room in initial temple, always pick target room WITHOUT AOTV: 0.6138")
    print(f"Room in initial temple, always pick target room WITH AOTV: 0.6158")

    print("")
    print("### Ratios of T3 Item Double Corrupt, room NOT in initial Temple:")
    print(f"Always pick target room WITHOUT AOTV: 0.3107")
    print(f"Always pick target room WITH AOTV: 0.2910")
    print(f"Prio t2 rooms, pick target room on t2, no target on t0 WITHOUT AOTV: 0.2636")
    print(f"Prio t2 rooms, pick target room on t2, no target on t0 WITH AOTV: 0.2528")
    print(f"Prio t2 rooms, pick target room on t2, target on t0 WITHOUT AOTV: 0.2973")
    print(f"Prio t2 rooms, pick target room on t2, target on t0 WITH AOTV: 0.2807")
    print(f"Prio t2 rooms, until target exists, then always upgrade WITHOUT AOTV: 0.3145")
    print(f"Prio t2 rooms, until target exists, then always upgrade WITH AOTV: 0.298")

    # print("### Ratios of T3 rooms when always upgrading:")
    # print(f"WITHOUT Artefacts of the Vaal:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade)}")
    # print(f"WITH Artefacts of the Vaal:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade, aotv=True)}")
    # print(f"WITHOUT AOTV and WITH Resource Reallocation:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade, rr=True)}")
    # print(f"WITH AOTV and WITH Resource Reallocation:"
    #       f"{calc_ratio_t3_rooms(run_t_always_upgrade, aotv=True, rr=True)}")
    #
    # print("")
    # print("### Ratios of T3 Item Double Corrupt:")
    # print(f"Baseline WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_upgrade,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Baseline WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_upgrade,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    # print(f"Baseline, always pick target room WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Baseline, always pick target room WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    # print(f"Room in initial temple, always pick target room WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=True,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Room in initial temple, always pick target room WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=True,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    # print("")
    # print("### Ratios of T3 Item Double Corrupt, room NOT in initial Temple:")
    # print(f"Always pick target room WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=False,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Always pick target room WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_always_pick_target_rooms,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=False,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    # print(f"Prio t2 rooms, pick target room on t2, no target on t0 WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_place_desired_room_on_t2_no_t0,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=False,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Prio t2 rooms, pick target room on t2, no target on t0 WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_place_desired_room_on_t2_no_t0,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=False,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    # print(f"Prio t2 rooms, pick target room on t2, target on t0 WITHOUT AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_place_desired_room_on_t2,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=False,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    # print(f"Prio t2 rooms, pick target room on t2, target on t0 WITH AOTV: "
    #       f"{calc_ratio_target_t3_rooms(run_t_place_desired_room_on_t2,
    #                                     initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
    #                                     start_with_initial_room=False,
    #                                     target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
    print(f"Prio t2 rooms, until target exists, then always upgrade WITHOUT AOTV: "
          f"{calc_ratio_target_t3_rooms(run_t_prio_t2_until_target_exists,
                                        initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
                                        start_with_initial_room=False,
                                        target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT])}")
    print(f"Prio t2 rooms, until target exists, then always upgrade WITH AOTV: "
          f"{calc_ratio_target_t3_rooms(run_t_prio_t2_until_target_exists,
                                        initial_room=ValidRoomType.ITEM_DOUBLE_CORRUPT,
                                        start_with_initial_room=False,
                                        target_rooms=[ValidRoomType.ITEM_DOUBLE_CORRUPT], aotv=True)}")
