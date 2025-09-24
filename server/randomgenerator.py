import json
import random

def generate_nickname(json_file_path="words.json"):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            adjectives = data.get("adjectives")
            nouns = data.get("nouns")

            if adjectives and nouns:
                adjective = random.choice(adjectives)
                noun = random.choice(nouns)
                number = random.randint(0, 99)

                nickname = f"{adjective}{noun}{number}"
                return nickname
            else:
                return "Fehler: Adjektive oder Nomen in der JSON-Datei fehlen."

    except FileNotFoundError:
        return "Fehler: JSON-Datei nicht gefunden."
    except json.JSONDecodeError:
        return "Fehler: JSON-Datei ist ungültig."
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}"
    

def generate_parceltime():
    parcel_times = ["1-2", "2-3", "3-4", "4-5", "9-10", "4-6", "8-10",
                     "ca. 30", "ca. 3485"]
    probabilities = [0.4, 0.3, 0.135, 0.04, 0.04, 0.0425, 0.02, 0.0125, 0.01]

    random_parceltime = random.choices(parcel_times, weights=probabilities, k=1)[0]

    return random_parceltime

