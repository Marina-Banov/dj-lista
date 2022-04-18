from dataclasses import dataclass


@dataclass
class Song:
    id: int
    tempo: float
    key: str

    def __repr__(self):
        return f"{self.id}"  # ,{self.tempo},{self.key}"
