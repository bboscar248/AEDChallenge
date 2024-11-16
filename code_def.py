import json
import pathlib
from typing import List, Tuple
from collections import defaultdict
from participant import Participant  # Asegúrate de tener la clase Participant definida correctamente en un archivo 'participant.py'

# 1. Función para cargar los participantes desde un archivo JSON
def load_participants(path: str) -> List[Participant]:
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"The file {path} does not exist, are you sure you're using the correct path?")
    if not pathlib.Path(path).suffix == ".json":
        raise ValueError(f"The file {path} is not a JSON file, are you sure you're using the correct file?")
    
    with open(path, 'r') as file:
        return [Participant(**participant) for participant in json.load(file)]

# 2. Función para obtener los puntos de experiencia de un participante
def get_experience_points(participant: Participant) -> int:
    experience_points = {
        "Beginner": 1,
        "Intermediate": 3,
        "Advanced": 6
    }
    return experience_points.get(participant.experience_level, 0)

# 3. Función para agrupar a los participantes según su objetivo (ganar o aprender/divertirse)
def group_participants_by_objective(participants: List[Participant]) -> Tuple[List[Participant], List[Participant]]:
    win_objective = []
    learn_fun_objective = []
    
    for p in participants:
        if "win" in p.objective.lower() or "competition" in p.objective.lower() or "prize" in p.objective.lower():
            win_objective.append(p)
        else:
            learn_fun_objective.append(p)
    
    return win_objective, learn_fun_objective

# 4. Función para agrupar a los participantes por habilidades de programación
def group_by_programming_skills(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes por habilidades de programación similares."""
    participants_sorted = sorted(participants, key=lambda p: sum(p.programming_skills.values()))
    
    groups = []
    current_group = []
    current_skill_sum = 0

    for p in participants_sorted:
        skill_sum = sum(p.programming_skills.values())
        
        # Si la diferencia de habilidades es mayor a 5, crea un nuevo grupo
        if current_group and abs(current_skill_sum - sum([sum(p.programming_skills.values()) for p in current_group])) > 5:
            groups.append(current_group)
            current_group = []
            current_skill_sum = 0
        
        current_group.append(p)
        current_skill_sum += skill_sum

    if current_group:
        groups.append(current_group)
    
    return groups

# 5. Función para agrupar a los participantes por sus intereses
def group_by_interests(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes por intereses similares."""
    interest_groups = defaultdict(list)
    
    for p in participants:
        for interest in p.interests:
            interest_groups[interest].append(p)
    
    return [group for group in interest_groups.values()]

# 6. Función para agrupar a los participantes en equipos según su objetivo, habilidades e intereses
def group_participants(participants: List[Participant]) -> dict:
    """Agrupa a los participantes en equipos según sus objetivos, habilidades y otros criterios."""
    
    # 1. Agrupar por objetivo (ganar vs aprender/divertirse)
    win_objective, learn_fun_objective = group_participants_by_objective(participants)
    
    # 2. Agrupar por habilidades de programación para los que quieren ganar
    win_groups = group_by_programming_skills(win_objective)

    # 3. Agrupar por intereses para los que quieren aprender/divertirse
    learn_fun_groups = group_by_interests(learn_fun_objective)

    # Agrupar los resultados en un diccionario para facilitar su visualización
    result = {
        "Win Objective Groups": win_groups,
        "Learn/Fun Objective Groups": learn_fun_groups
    }

    return result

# 7. Función para imprimir los grupos de manera más detallada
def print_groups(grouped_participants: dict):
    """Imprime los grupos con las personas, correos y razones de la agrupación."""
    
    for group_type, groups in grouped_participants.items():
        print(f"\n{group_type}:")
        for i, group in enumerate(groups):
            print(f"\n  Grupo {i + 1}:")
            print(f"    Número de participantes: {len(group)}")
            
            for participant in group:
                print(f"      - {participant.name} ({participant.email})")
            
            # Imprimir la razón para agrupar este grupo
            if group_type == "Win Objective Groups":
                print(f"    Razón de agrupación: Este grupo está compuesto por personas que tienen el objetivo de ganar y competir, por lo que se agruparon según sus habilidades de programación.")
            elif group_type == "Learn/Fun Objective Groups":
                print(f"    Razón de agrupación: Este grupo está compuesto por personas cuyo objetivo es aprender o divertirse, por lo que se agruparon según sus intereses comunes.")

# 8. Función principal
def main():
    try:
        # Cargar los participantes desde el archivo JSON
        participants = load_participants("prueba.json")
        
        # Agrupar a los participantes según su objetivo, habilidades e intereses
        grouped_participants = group_participants(participants)
        
        # Imprimir los grupos resultantes
        print_groups(grouped_participants)
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

# Asegurarse de que la función main se ejecute solo si es el script principal
if __name__ == "__main__":
    main()