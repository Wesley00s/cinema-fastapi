from enum import Enum

class MovieGenre(str, Enum):
    ACTION = "Ação"
    COMEDY = "Comédia"
    DRAMA = "Drama"
    HORROR = "Terror"
    SCI_FI = "Ficção Científica"
    ROMANCE = "Romance"
    DOCUMENTARY = "Documentário"
    ANIMATION = "Animação"
    ADVENTURE = "Aventura"
    FANTASY = "Fantasia"
    OTHER = "Outro"