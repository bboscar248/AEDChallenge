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

# 4. Filtrar por disponibilidad (al menos 3 períodos como 'True')
def filter_by_availability(participants: List[Participant]) -> List[Participant]:
    """Filtra los participantes que tienen al menos 3 'True' en los períodos de disponibilidad especificados."""
    filtered_participants = []
    required_periods = [
        "Saturday morning", "Saturday afternoon", "Saturday night", 
        "Sunday morning", "Sunday afternoon"
    ]
    
    for p in participants:
        available_periods = sum(1 for period in required_periods if p.availability.get(period, False))
        if available_periods >= 3:
            filtered_participants.append(p)
    
    return filtered_participants

# 5. Agrupar participantes por 'preferred_languages' y 'preferred_team_size'
def group_participants(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes según sus preferencias de idiomas y tamaño de equipo."""
    language_size_groups = defaultdict(list)
    
    for p in participants:
        language_size_groups[(p.preferred_languages, p.preferred_team_size)].append(p)
    
    return list(language_size_groups.values())

# 6. Función para agrupar participantes que quieren aprender, hacer amigos o divertirse
def group_learn_fun(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes que quieren aprender, hacer amigos o divertirse según intereses y amigos."""
    interest_groups = defaultdict(list)
    friend_groups = defaultdict(list)
    
    for p in participants:
        for interest in p.interests:
            interest_groups[interest].append(p)
        for friend_id in p.friend_registration:
            friend_groups[friend_id].append(p)
    
    final_groups = []
    
    # Agrupamos los que quieren aprender/fun según intereses y amigos
    for group in interest_groups.values():
        final_groups.append(group)
    
    # Si quedan participantes sin grupo, intentamos agregar amigos
    for group in friend_groups.values():
        if group:
            final_groups.append(group)
    
    return final_groups

# 7. Agrupar participantes que quieren ganar
def group_win(participants: List[Participant]) -> List[List[Participant]]:
    """Agrupa a los participantes que quieren ganar según disponibilidad, experiencia, habilidades y roles."""
    available_participants = filter_by_availability(participants)
    
    win_groups = []
    current_group = []
    current_experience_points = 0
    
    for p in sorted(available_participants, key=lambda x: get_experience_points(x), reverse=True):
        if current_group and (get_experience_points(p) - min(get_experience_points(p) for p in current_group)) > 6:
            win_groups.append(current_group)
            current_group = []
            current_experience_points = 0
        
        current_group.append(p)
        current_experience_points += get_experience_points(p)
    
    if current_group:
        win_groups.append(current_group)
    
    final_win_groups = []
    
    for group in win_groups:
        current_group = []
        current_skill_points = 0
        for p in sorted(group, key=lambda x: get_total_programming_skill(x)):
            if current_group and abs(current_skill_points + get_total_programming_skill(p) - sum(get_total_programming_skill(x) for x in current_group)) > 5:
                final_win_groups.append(current_group)
                current_group = []
                current_skill_points = 0
            current_group.append(p)
            current_skill_points += get_total_programming_skill(p)
        
        if current_group:
            final_win_groups.append(current_group)
    
    return final_win_groups

# 8. Función principal para agrupar participantes
def main():
    try:
        participants = load_participants("participants.json")
        groups = group_participants(participants)
        
        # Primera etapa: agrupar por preferencias de idioma y tamaño de equipo
        for group in groups:
            win_objective, learn_fun_objective = [], []
            for participant in group:
                if "win" in participant.objective.lower():
                    win_objective.append(participant)
                else:
                    learn_fun_objective.append(participant)
            
            # Agrupar participantes que quieren aprender, hacer amigos o divertirse
            learn_fun_groups = group_learn_fun(learn_fun_objective)
            
            print("\nGrupo de aprender, amigos o diversión:")
            for i, group in enumerate(learn_fun_groups):
                print(f"Grupo {i+1}:")
                for participant in group:
                    print(f"  - {participant.name} ({participant.interests}, {participant.objective})")
            
            # Agrupar participantes que quieren ganar
            win_groups = group_win(win_objective)
            
            print("\nGrupo de ganar:")
            for i, group in enumerate(win_groups):
                print(f"Grupo {i+1}:")
                for participant in group:
                    print(f"  - {participant.name} ({participant.preferred_languages}, {participant.objective})")
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

# Ejecuta solo si es el script principal
if __name__ == "__main__":
    main()
