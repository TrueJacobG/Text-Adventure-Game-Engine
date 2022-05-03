class Enemy:
    def __init__(self, current_location, difficulty, story):
        e = story[current_location]["enemy"]
        self.hp: float = e["hp"] * difficulty
        self.attacksDescription: str = e["attacksDescription"]
        self.attacksDMG = e["attacksDMG"]
        self.getDMG = e["getDMG"]
        self.defeated = e["deafeted"]