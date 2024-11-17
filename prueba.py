import json
import pathlib
import uuid
from dataclasses import dataclass
from typing import Dict, List, Literal
from collections import defaultdict


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
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"The file {path} does not exist.")
    if pathlib.Path(path).suffix != ".json":
        raise ValueError(f"The file {path} is not a JSON file.")
    
    with open(path, "r") as f:
        data = json.load(f)
    
    return [Participant(**participant) for participant in data]


def get_experience_points(participant: Participant) -> int:
    experience_points = {
        "Beginner": 1,
        "Intermediate": 3,
        "Advanced": 6
    }
    return experience_points.get(participant.experience_level, 0)


def get_total_programming_skill(participant: Participant) -> int:
    return sum(participant.programming_skills.values())


def filter_by_availability(participants: List[Participant], required_periods: List[str]) -> List[Participant]:
    available_participants = []
    for p in participants:
        available_periods_count = sum(1 for period in required_periods if p.availability.get(period, False))
        if available_periods_count >= 3:
            available_participants.append(p)
    return available_participants


def group_by_objective(participants: List[Participant]) -> Dict[str, List[Participant]]:
    win_group = []
    learn_fun_group = []
    for p in participants:
        if "to win" in p.objective.lower(): 
            win_group.append(p)
        else:
            learn_fun_group.append(p)
    return {"to win": win_group, "learn_fun": learn_fun_group}


def group_learn_fun_by_interests_and_friends(participants: List[Participant], group_size: int) -> List[List[Participant]]:
    groups = []
    available_participants = participants.copy()
    
    while available_participants:
        current_group = []
        current_participant = available_participants.pop(0)
        current_group.append(current_participant)
        
        # Añadir amigos al grupo
        friends_to_add = []
        for friend_id in current_participant.friend_registration:
            for i, part in enumerate(available_participants):
                if part.id == friend_id:
                    friends_to_add.append(available_participants.pop(i))
                    break
        
        current_group.extend(friends_to_add)
        
        # Agrupar por intereses
        for p in available_participants[:]:
            if set(p.interests).intersection(current_participant.interests):
                current_group.append(p)
                available_participants.remove(p)
        
        # Respetar el tamaño del grupo
        if len(current_group) > group_size:
            current_group = current_group[:group_size]
        
        groups.append(current_group)
    return groups


def group_win_by_availability_experience_skills_and_interests(participants: List[Participant], required_periods: List[str], group_size: int) -> List[Dict[str, any]]:
    available_participants = filter_by_availability(participants, required_periods)
    groups = []
    
    while available_participants:
        current_group = []
        reasons = set()  # Razones basadas en frases
        
        # Seleccionar el primer participante como referencia
        current_participant = available_participants.pop(0)
        current_group.append(current_participant)
        
        # Añadir amigos al grupo
        for friend_id in current_participant.friend_registration:
            for i, part in enumerate(available_participants):
                if part.id == friend_id:
                    current_group.append(part)
                    available_participants.pop(i)
                    reasons.add("Joined because they are friends")
                    break
        
        # Intentar balancear el grupo por disponibilidad, experiencia y habilidades
        for p in available_participants[:]:
            if len(current_group) < group_size and p not in current_group:
                current_group.append(p)
                available_participants.remove(p)
                reasons.add("Availability matches")
        
        # Balancear por experiencia (nivel de experiencia)
        experience_points = sum(get_experience_points(p) for p in current_group)
        for p in available_participants[:]:
            if len(current_group) < group_size:
                new_experience_points = experience_points + get_experience_points(p)
                if abs(new_experience_points - experience_points) <= 6:  # Diferencia de experiencia no mayor a 6 puntos
                    current_group.append(p)
                    available_participants.remove(p)
                    reasons.add("Balanced experience level")
        
        # Balancear por habilidades (sumar puntos de programación)
        skill_points = sum(get_total_programming_skill(p) for p in current_group)
        for p in available_participants[:]:
            if len(current_group) < group_size:
                new_skill_points = skill_points + get_total_programming_skill(p)
                if abs(new_skill_points - skill_points) <= 10:  # Diferencia de habilidades no mayor a 10 puntos
                    current_group.append(p)
                    available_participants.remove(p)
                    reasons.add("Balanced programming skills")
        
        # Determinar palabra clave de intereses comunes
        common_interests = defaultdict(int)
        for participant in current_group:
            for interest in participant.interests:
                common_interests[interest] += 1
        
        # Seleccionar la palabra clave de interés más común
        if common_interests:
            most_common_interest = max(common_interests, key=common_interests.get)
            reasons.add(f"Shared interest in {most_common_interest}")
        
        # Si no hay una razón identificada, se usa "General compatibility"
        if not reasons:
            reasons.add("General compatibility")
        
        # Respetar el tamaño del grupo
        if len(current_group) > group_size:
            current_group = current_group[:group_size]
        
        groups.append({
            "group": current_group,
            "reason": " and ".join(reasons)  # La razón será una frase
        })
    
    return groups


def main():
    try:
        participants = load_participants("datathon_participants.json")
        print(f"Loaded {len(participants)} participants.")
        
        # Agrupar por objetivos
        objective_groups = group_by_objective(participants)
        
        # Grupos de aprender/divertirse
        learn_fun_groups = group_learn_fun_by_interests_and_friends(objective_groups["learn_fun"], group_size=4)
        
        # Grupos de ganar
        required_periods = ["Saturday morning", "Saturday afternoon", "Saturday night", "Sunday morning", "Sunday afternoon"]
        win_groups = group_win_by_availability_experience_skills_and_interests(objective_groups["to win"], required_periods, group_size=4)
        
        # Imprimir los resultados
        print("\nGroups of participants that wanna fun/learn/make friends:")
        for i, group in enumerate(learn_fun_groups):
            print(f"Group {i+1}:")
            for participant in group:
                print(f"    - {participant.name} (ID: {participant.id})")
        
        print("\nGroups that wanna win:")
        for i, group_data in enumerate(win_groups):
            group = group_data["group"]
            reason = group_data["reason"]
            print(f"Group {i+1} (Reason: {reason}):")
            for participant in group:
                print(f"    - {participant.name} (ID: {participant.id})")
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
