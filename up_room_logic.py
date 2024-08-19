from temple_room import TempleRoom
from temple import Temple, ValidRoomType


def prio_upgrade_unless_target(temple: Temple,
                               room: TempleRoom,
                               target_rooms: None | list[ValidRoomType] = None) -> ValidRoomType:
    """
    Prioritises upgrading the room unless a target room is in the upgrade options, in which case that room type is
    chosen instead.

    :param temple: The temple object.
    :param room: The room object in the process of being upgraded.
    :param target_rooms: The desired target room types. Can be None.
    :return:
    """
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    upgrade_options = temple.get_room_upgrade_option(2 if room.tier == 0 else 1)
    room_type = upgrade_options[0] if room.type is None else room.type
    index = 0
    for room_present in [target_room in upgrade_options for target_room in target_rooms]:
        if room_present:
            room_type = target_rooms[index]
        index += 1
    return room_type


def prio_sidegrade_unless_target_no_t0(temple: Temple,
                                       room: TempleRoom,
                                       target_rooms: None | list[ValidRoomType] = None) -> ValidRoomType:
    """
    Prioritises side-grading the room unless the room is already a target room type. Will avoid choosing a target room
    type on a t0 room (unless both options are target rooms).

    :param temple: The temple object.
    :param room: The room object in the process of being upgraded.
    :param target_rooms: The desired target room types. Can be None.
    :return:
    """
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    upgrade_options = temple.get_room_upgrade_option(2 if room.tier == 0 else 1)
    if room.tier == 0:
        for target_room in target_rooms:
            if target_room in upgrade_options:
                upgrade_options.remove(target_room)
                break
        room_type = upgrade_options[0]
    else:
        room_type = prio_sidegrade_unless_target(temple=temple, room=room, target_rooms=target_rooms)
    return room_type


def prio_sidegrade_unless_target(temple: Temple,
                                 room: TempleRoom,
                                 target_rooms: None | list[ValidRoomType] = None) -> ValidRoomType:
    """
    Prioritises side-grading the room unless the room is already a target room type.

    :param temple: The temple object.
    :param room: The room object in the process of being upgraded.
    :param target_rooms: The desired target room types. Can be None.
    :return:
    """
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    upgrade_options = temple.get_room_upgrade_option(2 if room.tier == 0 else 1)
    room_type = room.type if room.type in target_rooms else upgrade_options[0]
    if room.tier == 0:
        index = 0
        for target_in_options in [target_room in upgrade_options for target_room in target_rooms]:
            if target_in_options:
                room_type = target_rooms[index]
            index += 1
    return room_type


def prio_adjacent_nexus(default_decision,
                        temple: Temple,
                        room: TempleRoom,
                        target_rooms: None | list[ValidRoomType] = None) -> ValidRoomType:
    """
    Prioritises placing a nexus (the room that upgrades adjacent rooms) next to a desired room. Unless the current room
    is a desired room, in which case, prioritises upgrading. If a Nexus isn't an upgrade option or room is not adjacent
    to a target room, falls back onto default_decision and returns that function result.

    :param default_decision: The up_room_logic function to fall back on.
    :param temple: The temple object.
    :param room: The room object in the process of being upgraded.
    :param target_rooms: The desired target room types. Can be None.
    :return:
    """
    if not isinstance(target_rooms, list):
        target_rooms = [target_rooms]
    if room.type is not None and room.type in target_rooms:
        return room.type
    upgrade_options = temple.get_room_upgrade_option(2 if room.tier == 0 else 1)
    adjacent_room_types = [adjacent_room.type for adjacent_room in room.connections]
    target_rooms_in_adjacent_rooms = [target_room in adjacent_room_types for target_room in target_rooms]
    nexus_is_upgrade_option = (ValidRoomType.ADJACENT_ROOM_LEVELS in upgrade_options
                               or room.type is ValidRoomType.ADJACENT_ROOM_LEVELS)
    if nexus_is_upgrade_option and any(target_rooms_in_adjacent_rooms):
        room_type = ValidRoomType.ADJACENT_ROOM_LEVELS
    else:
        room_type = default_decision(temple=temple,
                                     room=room,
                                     target_rooms=target_rooms)
    return room_type
