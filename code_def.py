import json
import pathlib
import uuid
from dataclasses import dataclass
from typing import Dict, List, Literal
from collections import defaultdict
from participant import Participant  # Importamos la clase Participant desde participant.py

# 1. Función para cargar los participantes
def load_participants(path: str) -> List[Participant]:
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"The file {path} does not exist, are you sure you're using the correct path?")
    if not pathlib.Path(path).suffix == ".json":
        raise ValueError(f"The file {path} is not a JSON file, are you sure you're using the correct file?")

    return [Participant(**participant) for participant in json.load(open(path))]

# 2. Función para obtener los puntos de experiencia
def get_experience_points(participant: Participant) -> int:
    """Asigna puntos según el nivel de experiencia del participante."""
    experience_points = {
        "Beginner": 1,
        "Intermediate": 3,
        "Advanced": 6
    }
    return experience_points.get(participant.experience_level, 0)

# 3. Función para obtener los puntos totales de habilidades de programación
def get_total_programming_skill(participant: Participant) -> int:
    """Suma los puntos de habilidad de programación de un participante."""
    return sum(participant.programming_skills.values())

# 4. Función para agrupar participantes
def group_participants(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes según sus preferencias y objetivos."""
    
    # 1. Separar los participantes por objetivo (ganar vs aprender/divertirse)
    win_objective = []
    learn_fun_objective = []
    
    for p in participants:
        if "win" in p.objective.lower() or "competition" in p.objective.lower() or "prize" in p.objective.lower():
            win_objective.append(p)
        else:
            learn_fun_objective.append(p)

    # 2. Agrupar a los que quieren ganar por nivel de experiencia
    win_objective_sorted = sorted(win_objective, key=lambda p: get_experience_points(p), reverse=True)
    
    groups_win = []  # Lista final de grupos para los participantes que quieren ganar
    current_group = []
    current_experience_points = 0

    for p in win_objective_sorted:
        p_experience = get_experience_points(p)
        # Si la diferencia de puntos de experiencia excede los 6, crear un nuevo grupo
        if current_group and current_experience_points + p_experience - min(get_experience_points(p) for p in current_group) > 6:
            groups_win.append(current_group)
            current_group = []
            current_experience_points = 0
        
        current_group.append(p)
        current_experience_points += p_experience

    # Asegurarse de agregar el último grupo
    if current_group:
        groups_win.append(current_group)

    # 5. Agrupar por habilidades de programación (diferencia no mayor a 5)
    def group_by_programming_skills(groups: List[List[Participant]]) -> List[List[Participant]]:
        final_groups = []
        for group in groups:
            current_group = []
            current_skill_points = 0
            for p in group:
                p_skills = get_total_programming_skill(p)
                # Si la diferencia de puntos de habilidades excede los 5, iniciar un nuevo grupo
                if current_group and abs(current_skill_points + p_skills - sum([get_total_programming_skill(x) for x in current_group])) > 5:
                    final_groups.append(current_group)
                    current_group = []
                    current_skill_points = 0
                current_group.append(p)
                current_skill_points += p_skills
            
            if current_group:
                final_groups.append(current_group)
        
        return final_groups
    
    groups_win = group_by_programming_skills(groups_win)

    # 6. Si no se pueden cumplir las restricciones, intentar cambiar el tamaño de los equipos
    def adjust_team_sizes(groups: List[List[Participant]]):
        for group in groups:
            total_skill_points = sum(get_total_programming_skill(p) for p in group)
            if total_skill_points > 5:  # Si la diferencia es mayor a 5, pedir revisión
                print(f"Group with total programming skill points exceeding the allowed difference. Consider changing preferred team size for this group.")
    
    adjust_team_sizes(groups_win)

    # 7. Agrupar por intereses para los participantes de 'learn/fun'
    def group_by_interests(participants: List[Participant]) -> List[List[Participant]]:
        """Agrupa a los participantes por intereses similares."""
        interest_groups = defaultdict(list)
        
        # Usamos un enfoque de coincidencia de intereses para agrupar a los participantes
        for p in participants:
            for interest in p.interests:
                interest_groups[interest].append(p)
        
        # Crear grupos de participantes con intereses similares
        final_groups = []
        for group in interest_groups.values():
            # Puedes aplicar más lógica para dividir los grupos si son demasiado grandes.
            final_groups.append(group)
        
        return final_groups

    # Agrupar a los que quieren aprender/divertirse por sus intereses
    learn_fun_groups = group_by_interests(learn_fun_objective)

    # 8. Ahora tenemos los grupos de 'ganar' y 'aprender/divertirse' agrupados por intereses
    return groups_win, learn_fun_groups

# 9. Función principal
def main():
    try:
        participants = load_participants("participants.json")
        groups_win, learn_fun_groups = group_participants(participants)
        
        print("Win Objective Groups:")
        for i, group in enumerate(groups_win):
            print(f"Group {i+1}:")
            for participant in group:
                print(f"  - {participant.name} ({participant.preferred_languages}, {participant.objective})")
        
        print("\nLearn/Fun Objective Groups:")
        for i, group in enumerate(learn_fun_groups):
            print(f"Group {i+1}:")
            for participant in group:
                print(f"  - {participant.name} ({participant.interests}, {participant.objective})")
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

# Asegurarse de que la función main se ejecute solo si es el script principal
if __name__ == "__main__":
    main()
