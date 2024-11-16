#CLassifiquem les persones en grups de 4 segons les dades que han escrit en el fitxer "participant.py".

from collections import defaultdict

def classify_participants(participants: List[Participant]) -> Dict[str, List[Participant]]:
    """
    Clasifica a los participantes según su nivel de experiencia y habilidades de programación.
    """
    classifications = {
        "Beginner": [],
        "Intermediate": [],
        "Advanced": [],
    }
    
    for participant in participants:
        if participant.experience_level in classifications:
            classifications[participant.experience_level].append(participant)
    
    return classifications


def display_classifications(classifications: Dict[str, List[Participant]]):
    """
    Muestra las clasificaciones de forma organizada.
    """
    for category, participants in classifications.items():
        print(f"\n=== {category} ===")
        for p in participants:
            print(f"- {p.name} ({p.email}) - {p.university}")


# Ejemplo de uso:
if __name__ == "__main__":
    # Cargar datos de participantes desde un archivo JSON
    try:
        participants = load_participants("participants.json")
        # Clasificar participantes
        classified = classify_participants(participants)
        # Mostrar clasificaciones
        display_classifications(classified)
    except Exception as e:
        print(f"Error: {e}")
