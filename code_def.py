import json
import pathlib
import uuid
from dataclasses import dataclass
from typing import Dict, List, Literal
from collections import defaultdict

# ... (Participant class and load_participants function from previous response) ...


def group_participants(participants: List[Participant]) -> List[List[Participant]]:
    """Groups participants based on preferences."""

    # 1. Prioritize Preferred Languages
    language_groups = defaultdict(list)
    for p in participants:
        for lang in p.preferred_languages:
            language_groups[lang].append(p)

    # 2. Prioritize Preferred Team Size (within language groups)
    grouped_by_size = defaultdict(list)
    for lang, group in language_groups.items():
        for p in group:
            grouped_by_size[p.preferred_team_size].append(p)

    # 3. Prioritize Objective (win vs. learn/fun)
    win_objective = []
    learn_fun_objective = []
    for size_group in grouped_by_size.values():
        for p in size_group:
            if "win" in p.objective.lower() or "competition" in p.objective.lower() or "prize" in p.objective.lower():
                win_objective.append(p)
            else:
                learn_fun_objective.append(p)

    # 4. Consider Friends (this part is complex and requires further refinement)
    # A simple approach: try to keep friends together as much as possible within existing groups.
    final_groups = []
    #Process win objective group
    final_groups.extend(form_groups_with_friends(win_objective))
    #Process learn/fun objective group
    final_groups.extend(form_groups_with_friends(learn_fun_objective))

    return final_groups


def form_groups_with_friends(participants: List[Participant]) -> List[List[Participant]]:
    """Attempts to keep friends together when forming groups."""
    groups = []
    available_participants = participants.copy()
    while available_participants:
        current_group = [available_participants.pop(0)]
        friends_to_add = []
        for p in current_group:
            for friend_id in p.friend_registration:
                for i, part in enumerate(available_participants):
                    if part.id == friend_id:
                        friends_to_add.append(available_participants.pop(i))
                        break
        current_group.extend(friends_to_add)
        groups.append(current_group)
    return groups


def main():
    try:
        participants = load_participants("participants.json")
        groups = group_participants(participants)
        for i, group in enumerate(groups):
            print(f"Group {i+1}:")
            for participant in group:
                print(f"  - {participant.name} ({participant.preferred_languages}, {participant.objective})")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")


if _name_ == "_main_":
    main()