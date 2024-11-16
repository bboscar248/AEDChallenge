from participant import Participant, load_participants
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from typing import List

def calcula_vector_participant(participant: Participant) -> np.ndarray:
    """
    Converteix un participant en un vector numèric per al clustering.
    """
    # Codificació d'experiència (Beginner: 0, Intermediate: 1, Advanced: 2)
    experience_mapping = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    experience_level = experience_mapping[participant.experience_level]
    
    # Tamany de programació: Número d'habilitats que coneix
    programming_skills = len(participant.programming_skills)
    
    # Número d'interessos
    interests = len(participant.interests)
    
    # Hackathons fets
    hackathons_done = participant.hackathons_done
    
    # Tornem un vector amb els valors numèrics
    return np.array([experience_level, programming_skills, interests, hackathons_done])

def agrupa_participants_clustering(participants: List[Participant], num_grups: int) -> List[List[Participant]]:
    """
    Agrupa els participants utilitzant un mètode de clustering.
    """
    # Convertir els participants en vectors numèrics
    vectors = np.array([calcula_vector_participant(p) for p in participants])

    # Aplicar Agglomerative Clustering
    clustering = AgglomerativeClustering(n_clusters=num_grups, linkage="ward")
    labels = clustering.fit_predict(vectors)

    # Crear grups basats en els labels
    grups = [[] for _ in range(num_grups)]
    for participant, label in zip(participants, labels):
        grups[label].append(participant)
    
    return grups

def mostra_equips(equips: List[List[Participant]]):
    """
    Mostra els equips formats.
    """
    for i, equip in enumerate(equips, 1):
        print(f"\nEquip {i}:")
        for participant in equip:
            print(f"- {participant.name} ({participant.email}) - {participant.university}")

if __name__ == "__main__":
    try:
        # Carregar els participants des del fitxer JSON
        participants = load_participants("participants.json")

        # Especificar el nombre de grups
        num_grups = 4  # Canvia aquest valor segons les necessitats

        # Agrupar els participants amb clustering
        equips = agrupa_participants_clustering(participants, num_grups)

        # Mostrar els equips
        mostra_equips(equips)

    except Exception as e:
        print(f"Error: {e}")
