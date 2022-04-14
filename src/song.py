class Song:
    def __init__(self, _id, tempo, key):
        self.id = int(_id)
        self.tempo = float(tempo)
        self.key = key

    def __repr__(self):
        return f"{self.id},{self.tempo},{self.key}"
