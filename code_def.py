import json
import pathlib
import uuid
from dataclasses import dataclass
from typing import Dict, List, Literal
from collections import defaultdict


# Definición de la clase Participant
@dataclass
class Participant:
    id: uuid.UUID  # Identificador único
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
    """Carga los participantes desde un archivo JSON."""
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"The file {path} does not exist.")
    if pathlib.Path(path).suffix != ".json":
        raise ValueError(f"The file {path} is not a JSON file.")
    
    with open(path, "r") as f:
        data = json.load(f)
    
    return [Participant(**participant) for participant in data]


# Funciones de puntuación por experiencia y habilidades
def get_experience_points(participant: Participant) -> int:
    """Devuelve los puntos basados en el nivel de experiencia del participante."""
    experience_points = {
        "Beginner": 1,
        "Intermediate": 3,
        "Advanced": 6
    }
    return experience_points.get(participant.experience_level, 0)


def get_total_programming_skill(participant: Participant) -> int:
    """Devuelve el total de habilidades de programación del participante."""
    return sum(participant.programming_skills.values())


def filter_by_availability(participants: List[Participant], required_periods: List[str]) -> List[Participant]:
    """Filtra participantes que tienen disponibilidad en al menos 3 períodos."""
    available_participants = []
    for p in participants:
        available_periods = sum(1 for period in required_periods if p.availability.get(period, False))
        if available_periods >= 3:
            available_participants.append(p)
    return available_participants


# Funciones de agrupamiento
def group_by_language(participants: List[Participant]) -> Dict[str, List[Participant]]:
    """Agrupa a los participantes según sus lenguajes preferidos."""
    language_groups = defaultdict(list)
    for p in participants:
        for lang in p.preferred_languages:
            language_groups[lang].append(p)
    return language_groups


def group_by_team_size(participants: List[Participant]) -> Dict[int, List[Participant]]:
    """Agrupa a los participantes según su tamaño de equipo preferido."""
    size_groups = defaultdict(list)
    for p in participants:
        size_groups[p.preferred_team_size].append(p)
    return size_groups


def group_by_objective(participants: List[Participant]) -> Dict[str, List[Participant]]:
    """Separa a los participantes según su objetivo (ganar o aprender/fun/amigos)."""
    win_group = []
    learn_fun_group = []
    for p in participants:
        if "win" in p.objective.lower() or "competition" in p.objective.lower() or "prize" in p.objective.lower():
            win_group.append(p)
        else:
            learn_fun_group.append(p)
    return {"win": win_group, "learn_fun": learn_fun_group}


def group_learn_fun_by_interests_and_friends(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes que quieren aprender o hacer amigos según sus intereses y amigos, con un límite de 4 personas por grupo."""
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
        
        # Asegurarse de que no haya más de 4 personas en el grupo
        if len(current_group) > 4:
            current_group = current_group[:4]
        
        groups.append(current_group)
    return groups


def group_win_by_availability_and_balance(participants: List[Participant], required_periods: List[str]) -> List[List[Participant]]:
    """Agrupa a los participantes que quieren ganar según su disponibilidad, nivel de experiencia y habilidades, con un límite de 4 personas por grupo."""
    available_participants = filter_by_availability(participants, required_periods)
    
    # Agrupar por disponibilidad
    groups = []
    assigned_ids = set()
    
    while available_participants:
        current_group = []
        current_participant = available_participants.pop(0)
        current_group.append(current_participant)
        assigned_ids.add(current_participant.id)
        
        # Añadir amigos
        for friend_id in current_participant.friend_registration:
            for i, part in enumerate(available_participants):
                if part.id == friend_id and part.id not in assigned_ids:
                    current_group.append(available_participants.pop(i))
                    assigned_ids.add(part.id)
                    break
        
        # Balancear los grupos según puntos de experiencia y habilidades de programación
        current_experience_points = sum(get_experience_points(p) for p in current_group)
        current_skill_points = sum(get_total_programming_skill(p) for p in current_group)
        
        for p in available_participants[:]:
            if abs(sum(get_experience_points(p) for p in current_group) - current_experience_points) <= 6 and \
               abs(sum(get_total_programming_skill(p) for p in current_group) - current_skill_points) <= 5:
                current_group.append(p)
                available_participants.remove(p)
        
        # Asegurarse de que no haya más de 4 personas en el grupo
        if len(current_group) > 4:
            current_group = current_group[:4]
        
        groups.append(current_group)
    
    return groups


# Función principal para ejecutar el código
def main():
    try:
        participants = load_participants("participants.json")
        
        # Agrupar por idiomas y tamaño de equipo
        language_groups = group_by_language(participants)
        team_size_groups = group_by_team_size(participants)
        
        # Separar por objetivo
        objective_groups = group_by_objective(participants)
        
        # Agrupar los que quieren aprender/fun/amigos por intereses y amigos
        learn_fun_groups = group_learn_fun_by_interests_and_friends(objective_groups["learn_fun"])
        
        # Agrupar los que quieren ganar por disponibilidad, nivel de experiencia y habilidades
        required_periods = ["Saturday morning", "Saturday afternoon", "Saturday night", "Sunday morning", "Sunday afternoon"]
        win_groups = group_win_by_availability_and_balance(objective_groups["win"], required_periods)
        
        # Imprimir los grupos
        print("Grupos de participantes que quieren aprender/fun/amigos:")
        for i, group in enumerate(learn_fun_groups):
            print(f"  Grupo {i+1}:")
            for participant in group:
                print(f"    - {participant.name} ({participant.preferred_languages}, {participant.objective})")
        
        print("\nGrupos de participantes que quieren ganar:")
        for i, group in enumerate(win_groups):
            print(f"  Grupo {i+1}:")
            for participant in group:
                print(f"    - {participant.name} ({participant.preferred_languages}, {participant.objective})")
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
