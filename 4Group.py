from participant import Participant, load_participants
from typing import List, Dict
from itertools import combinations

def calculate_similarity_score(p1: Participant, p2: Participant) -> int:
    """
    Calcula un puntaje de similitud entre dos participantes basado en intereses,
    habilidades y nivel de experiencia.
    """
    score = 0
    
    # Comparar nivel de experiencia
    if p1.experience_level == p2.experience_level:
        score += 3

    # Comparar intereses
    common_interests = set(p1.interests) & set(p2.interests)
    score += len(common_interests)

    # Comparar habilidades de programación
    common_skills = set(p1.programming_skills.keys()) & set(p2.programming_skills.keys())
    score += len(common_skills)
    
    return score

def group_participants(participants: List[Participant]) -> List[List[Participant]]:
    """
    Agrupa a los participantes en equipos de 4 con base en la similitud.
    """
    if len(participants) < 4:
        raise ValueError("Debe haber al menos 4 participantes para formar equipos.")
    
    teams = []
    used = set()

    # Ordenar las combinaciones según el puntaje de similitud
    for combo in combinations(participants, 4):
        if any(p.id in used for p in combo):
            continue

        # Calcular el puntaje promedio del grupo
        score = sum(calculate_similarity_score(p1, p2) for p1, p2 in combinations(combo, 2))
        teams.append((combo, score))

    # Ordenar grupos por puntaje y seleccionar los mejores equipos
    teams.sort(key=lambda x: -x[1])  # Ordenar por puntaje descendente
    final_teams = []

    for team, _ in teams:
        if all(p.id not in used for p in team):
            final_teams.append(list(team))
            used.update(p.id for p in team)

        if len(used) == len(participants):  # Si todos están en un equipo, detenemos
            break

    return final_teams

def display_teams(teams: List[List[Participant]]):
    """
    Imprime los equipos formados.
    """
    for i, team in enumerate(teams, 1):
        print(f"\nEquipo {i}:")
        for participant in team:
            print(f"- {participant.name} ({participant.email}) - {participant.university}")

if __name__ == "__main__":
    try:
        # Cargar los participantes desde el archivo JSON
        participants = load_participants("participants.json")

        # Formar equipos
        teams = group_participants(participants)

        # Mostrar los equipos
        display_teams(teams)

    except Exception as e:
        print(f"Error: {e}")
