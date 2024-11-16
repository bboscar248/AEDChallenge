from participant import Participant, load_participants
from typing import List
from itertools import combinations

def calcula_puntuacio_similitud(p1: Participant, p2: Participant) -> int:
    """
    Calcula una puntuació de similitud entre dos participants basada en interessos,
    habilitats i nivell d'experiència.
    """
    puntuacio = 0
    
    # Comparar nivell d'experiència
    if p1.experience_level == p2.experience_level:
        puntuacio += 3

    # Comparar interessos
    interessos_comuns = set(p1.interests) & set(p2.interests)
    puntuacio += len(interessos_comuns)

    # Comparar habilitats de programació
    habilitats_comunes = set(p1.programming_skills.keys()) & set(p2.programming_skills.keys())
    puntuacio += len(habilitats_comunes)
    
    return puntuacio

def agrupa_participants_flexible(participants: List[Participant], tamanys_grups: List[int]) -> List[List[Participant]]:
    """
    Agrupa els participants en equips flexibles segons els tamanys indicats.
    """
    if not participants:
        return []

    equips = []
    usats = set()

    for tamany in tamanys_grups:
        possibles_equips = [
            combo for combo in combinations(participants, tamany)
            if all(p.id not in usats for p in combo)
        ]
        
        # Ordenar possibles grups per puntuació de similitud
        equips_puntuats = [
            (equip, sum(calcula_puntuacio_similitud(p1, p2) for p1, p2 in combinations(equip, 2)))
            for equip in possibles_equips
        ]
        equips_puntuats.sort(key=lambda x: -x[1])  # Ordenar per puntuació descendent
        
        for equip, _ in equips_puntuats:
            if all(p.id not in usats for p in equip):
                equips.append(list(equip))
                usats.update(p.id for p in equip)
                break  # Només agafar el millor grup en aquesta iteració

    # Assignar els participants restants que no s'han pogut agrupar
    restants = [p for p in participants if p.id not in usats]
    for p in restants:
        equips.append([p])  # Grups d'1 si no hi ha altres opcions

    return equips

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
        
        # Definir els tamanys possibles dels grups
        tamanys_grups = [4, 3, 2]  # Prioritzar grups de 4, després de 3 i després de 2

        # Formar equips flexibles
        equips = agrupa_participants_flexible(participants, tamanys_grups)

        # Mostrar els equips
        mostra_equips(equips)

    except Exception as e:
        print(f"Error: {e}")
