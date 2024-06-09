# TODO: write the PDDL domain

from merlin2_basic_actions.merlin2_basic_types import wp_type
from kant_dto import PddlTypeDto, PddlPredicateDto

# types
room_type = PddlTypeDto("room")
# pre
room_patrolled = PddlPredicateDto("room_patrolled", [room_type])
room_at = PddlPredicateDto("room_at", [room_typem wp_type])