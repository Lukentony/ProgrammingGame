import json

class Level:
    def __init__(self, title, instructions, valid_answers):
        self.title = title
        self.instructions = instructions
        self.valid_answers = valid_answers

def load_levels(filepath):
    """Load levels from a JSON file."""
    with open(filepath, "r") as file:
        data = json.load(file)
    return [Level(lvl["title"], lvl["instructions"], lvl["valid_answers"]) for lvl in data]
