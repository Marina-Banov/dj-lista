class Song:
    def __init__(self, id_, tempo, key):
        self.id = int(id_)
        self.tempo = float(tempo)
        self.key = key

    def __repr__(self):
        return f"{self.id}"  # ,{self.tempo},{self.key}"
