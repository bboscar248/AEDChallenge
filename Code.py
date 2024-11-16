#CLassifiquem les persones en grups de 4 segons les dades que han escrit en el fitxer "participant.py".

from participant import Participant, load_participants
from collections import defaultdict
from typing import List, Dict

def classify_participants_by_experience(participants: List[Participant]) -> Dict[str, List[Participant]]:
    """
    Classifica els participants segons el seu nivell d'experiència.
    """
    classifications = defaultdict(list)
    for participant in participants:
        classifications[participant.experience_level].append(participant)
    return classifications

def classify_participants_by_university(participants: List[Participant]) -> Dict[str, List[Participant]]:
    """
    Classifica els participants segons la universitat.
    """
    classifications = defaultdict(list)
    for participant in participants:
        classifications[participant.university].append(participant)
    return classifications

def display_classifications(classifications: Dict[str, List[Participant]]):
    """
    Imprime las clasificaciones de manera organizada.
    """
    for category, participants in classifications.items():
        print(f"\n=== {category} ===")
        for participant in participants:
            print(f"- {participant.name} ({participant.email}) - {participant.university}")

if __name__ == "__main__":
    try:
        # Cargar los participantes desde un archivo JSON
        participants = load_participants("participants.json")
        
        # Clasificar por nivel de experiencia
        experience_classifications = classify_participants_by_experience(participants)
        print("Clasificación por nivel de experiencia:")
        display_classifications(experience_classifications)

        # Clasificar por universidad
        university_classifications = classify_participants_by_university(participants)
        print("\nClasificación por universidad:")
        display_classifications(university_classifications)

    except Exception as e:
        print(f"Error: {e}")
