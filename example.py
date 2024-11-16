from rich import print

from participant import load_participants

data_path = "data/datathon_participants.json"
participants = load_participants(data_path)

print(participants[0])

<<<<<<< HEAD
print("Hello")
=======
print("Hola")
>>>>>>> 5fe7a256e94dafc4f30ce20c3aa35feaa3c6617a
