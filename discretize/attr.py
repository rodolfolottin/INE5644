from enum import Enum


class Attr(Enum):

    OutcomeType = 'OutcomeType'
    OutcomeSubtype = 'OutcomeSubtype'
    AnimalType = 'AnimalType'
    SexuponOutcome = 'SexuponOutcome'
    AgeuponOutcome = 'AgeuponOutcome'
    Breed = 'Breed'
    Color = 'Color'
    Lifespan = 'Lifespan'
    Size = 'Size'
    Adaptability = 'Adaptability'

    def __repr__(self):
        return str(self.value)
