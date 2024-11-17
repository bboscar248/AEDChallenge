import json
import pathlib
import uuid
from dataclasses import dataclass
from typing import Dict, List, Literal


@dataclass
class Participant:
    id: uuid.UUID
    name: str
    email: str
    age: int
    year_of_study: Literal["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"]
    shirt_size: Literal["S", "M", "L", "XL"]
    university: str
    dietary_restrictions: Literal["None", "Vegetarian", "Vegan", "Gluten-free", "Other"]
    programming_skills: Dict[str, int]
    experience_level: Literal["Beginner", "Intermediate", "Advanced"]
    hackathons_done: int
    interests: List[str]
    preferred_role: Literal[
        "Analysis", "Visualization", "Development", "Design", "Don't know", "Don't care"
    ]
    objective: str
    interest_in_challenges: List[str]
    preferred_languages: List[str]
    friend_registration: List[uuid.UUID]
    preferred_team_size: int
    availability: Dict[str, bool]
    introduction: str
    technical_project: str
    future_excitement: str
    fun_fact: str


def load_participants(path: str) -> List[Participant]:
    """
    Load participants from a JSON file.
    """
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"The file {path} does not exist.")
    if pathlib.Path(path).suffix != ".json":
        raise ValueError(f"The file {path} is not a JSON file.")
    
    with open(path, "r") as f:
        data = json.load(f)
    
    return [Participant(**participant) for participant in data]


def calculate_experience_points(experience: str) -> int:
    """
    Assign points to experience levels.
    """
    experience_map = {"Beginner": 1, "Intermediate": 3, "Advanced": 6}
    return experience_map.get(experience, 0)


def calculate_total_programming_skills(skills: Dict[str, int]) -> int:
    """
    Calculate the total programming skill points.
    """
    return sum(skills.values())


def check_availability(participant: Participant, required_periods: List[str]) -> bool:
    """
    Check if a participant is available for at least three of the required periods.
    """
    available_periods = sum(1 for period in required_periods if participant.availability.get(period, False))
    return available_periods >= 3


def group_by_objective(participants: List[Participant]) -> Dict[str, List[Participant]]:
    """
    Separate participants into groups based on their objective.
    """
    win_group = [p for p in participants if "to win" in p.objective.lower()]
    learn_fun_group = [p for p in participants if "to win" not in p.objective.lower()]
    return {"to win": win_group, "learn_fun": learn_fun_group}


def create_groups(participants: List[Participant], group_size: int, required_periods: List[str]) -> List[List[Participant]]:
    """
    Group participants based on shared interests, experience, and availability.
    """
    groups = []
    available_participants = participants.copy()
    
    while available_participants:
        current_group = []
        current_participant = available_participants.pop(0)
        current_group.append(current_participant)
        
        # Add friends
        friends_to_add = []
        for friend_id in current_participant.friend_registration:
            for i, part in enumerate(available_participants):
                if part.id == friend_id:
                    friends_to_add.append(available_participants.pop(i))
                    break
        
        current_group.extend(friends_to_add)
        
        # Add participants with shared interests
        for p in available_participants[:]:
            if len(current_group) >= group_size:
                break
            if set(p.interests).intersection(current_participant.interests):
                current_group.append(p)
                available_participants.remove(p)
        
        groups.append(current_group[:group_size])
    
    return groups


def explain_grouping(group: List[Participant], required_periods: List[str]) -> str:
    """
    Provide a detailed explanation of why each participant is in the group.
    """
    explanations = []
    for participant in group:
        total_skills = calculate_total_programming_skills(participant.programming_skills)
        experience_points = calculate_experience_points(participant.experience_level)
        is_available = check_availability(participant, required_periods)
        explanations.append(
            f"- {participant.name} (ID: {participant.id})\n"
            f"  Programming Skills: {total_skills}\n"
            f"  Experience Level: {participant.experience_level} ({experience_points} points)\n"
            f"  Available in required periods: {'Yes' if is_available else 'No'}"
        )
    return "\n".join(explanations)


def main():
    try:
        participants = load_participants("datathon_participants.json")
        objective_groups = group_by_objective(participants)
        required_periods = ["Saturday morning", "Saturday afternoon", "Saturday night", "Sunday morning", "Sunday afternoon"]

        learn_fun_groups = create_groups(objective_groups["learn_fun"], group_size=4, required_periods=required_periods)
        win_groups = create_groups(objective_groups["to win"], group_size=4, required_periods=required_periods)

        print("\nGroups of participants that want to learn/fun/make friends:")
        for i, group in enumerate(learn_fun_groups, 1):
            print(f"\nGroup {i}:")
            print(explain_grouping(group, required_periods))

        print("\nGroups of participants that want to win:")
        for i, group in enumerate(win_groups, 1):
            print(f"\nGroup {i}:")
            print(explain_grouping(group, required_periods))
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
