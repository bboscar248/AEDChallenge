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


# Función de agrupamiento por tamaño de equipo preferido
def group_by_preferred_team_size(participants: List[Participant]) -> Dict[int, List[Participant]]:
    """Agrupa a los participantes según su tamaño de equipo preferido."""
    size_groups = defaultdict(list)
    for p in participants:
        size_groups[p.preferred_team_size].append(p)
    return size_groups


# Función para dividir los grupos grandes (más de 4 personas) en grupos más pequeños
def split_into_smaller_groups(groups: Dict[int, List[Participant]]) -> List[List[Participant]]:
    """Divide los grupos grandes en subgrupos de 4 personas como máximo."""
    all_groups = []
    
    for size, group in groups.items():
        while len(group) > 4:
            all_groups.append(group[:4])  # Añadir el primer subgrupo de 4
            group = group[4:]  # Eliminar las primeras 4 personas del grupo original
        if group:  # Si hay personas restantes (menos de 4)
            all_groups.append(group)
    
    return all_groups


# Función principal para ejecutar el código
def main():
    try:
        participants = load_participants("prueba.json")
        
        # Agrupar por tamaño de equipo preferido
        size_groups = group_by_preferred_team_size(participants)
        
        # Dividir los grupos grandes (más de 4 personas) en grupos más pequeños
        final_groups = split_into_smaller_groups(size_groups)
        
        # Imprimir los grupos
        for i, group in enumerate(final_groups):
            print(f"Grupo {i+1}:")
            for participant in group:
                print(f"    - {participant.name} (ID: {participant.id}, Preferred Team Size: {participant.preferred_team_size})")
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
