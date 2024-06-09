# TODO: write the mission node

import rclpy
from typing import List
from merlin2_mission import Merlin2FsmMissionNode
from merlin2_basic_actions.merlin2_basic_predicates import robot_at
from merlin2_basic_actions.merlin2_basic_types import wp_type
from kant_dto import PddlObjectDto, PddlConditionEffectDto
from .pddl import room_type, room_at, room_patrolled

from yasmin import Blackboard, CbState
from yasmin_ros.basic_outcomes import SUCCEED

class issionNode(Merlin2FsmMissionNode):
    
    def __init__(self) -> None:
        super().__init__('mission_node')

        END = "end"
        HAS_NEXT = "has_next"
        
        self.add_state(
            "PREPARING_GOALS",
            CbState([SUCCEED], self.prepare_goals),
            transitions={
                SUCCEED: "CHECKING_GOALS",
            }
        )
        
        self.add_state(
            "CHECKING_GOALS",
            CbState([self.END, self.HAS_NEXT], self.check_goals),
            transitions={
                SUCCEED: SUCCEED,
                HAS_NEXT: "EXECUTING_PATROL,
            }
        )
        
        self.add_state(
            "EXECUTING_PATROL",
            CbState([SUCCEED], self.execute_patrol),
            transitions={
                SUCCEED: "CHECKING_GOALS",
            }
        )
                
    
    
    def create_objects(self) ->  List[PddlObjectDto]:
        self.wp0 = PddlObjectDto(wp_type, "wp0")
        self.wp1 = PddlObjectDto(wp_type, "wp1")
        self.wp2 = PddlObjectDto(wp_type, "wp2")
        self.wp3 = PddlObjectDto(wp_type, "wp3")
        self.wp4 = PddlObjectDto(wp_type, "wp4")
        self.wp5 = PddlObjectDto(wp_type, "wp5")
        
        self.room1 = PddlObjectDto(room_type, "room1")
        self.room2 = PddlObjectDto(room_type, "room2")
        self.room3 = PddlObjectDto(room_type, "room3")
        self.room4 = PddlObjectDto(room_type, "room4")
        self.room5 = PddlObjectDto(room_type, "room5")
        
        return [self.wp0, self.wp1, self.wp2, self.wp3, self.wp4, self.wp5,
                self.room1, self.room2, self.room3, self.room4, self.room5]
    
    def create_positions(self) -> List[PddlPropositionDto]:
        return [
            PddlPropositionDto(room_at, [self.wp0]),
            PddlPropositionDto(room_at, [self.room1, self.wp1]),
            PddlPropositionDto(room_at, [self.room2, self.wp2]),
            PddlPropositionDto(room_at, [self.room3, self.wp3]),
            PddlPropositionDto(room_at, [self.room4, self.wp4]),
            PddlPropositionDto(room_at, [self.room5, self.wp5]),
        ]
        
    def prepare_goals(self, blackboard) -> str:
        blackboard.goals = [
            PddlPropositionDto(room_patrolled, [self.room1], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room2], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room3], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room4], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room5], is_goal=True)
        ]
        return SUCCEED
        
    def check_goals(self, blackboard) -> str:
        if(blackboard.goals):
            blackboard.next_goal = blackboard.goals.pop(0)
            return self.HAS_NEXT
        else:
            return self.END
            
        
    def execute_patrol(self, balckboard) -> str:
        self.execute_goal(blackboard.next_goal)
        return SUCCEED
        
        
def main():
    
        rclpy.init()
        node = MissionNode()
        node.execute_mission()
        node.join_spin()
        
        rclpy.shutdown()
        
if __name__ == "__main__":
    main()
        