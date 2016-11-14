from enum import Enum


class Attr(Enum):

    OutcomeType = 'OutcomeType'
    OutcomeSubtype = 'OutcomeSubtype'
    AnimalType = 'AnimalType'
    SexuponOutcome = 'SexuponOutcome'
    AgeuponOutcome = 'AgeuponOutcome'
    AgeuponOutcomeInterval = 'AgeuponOutcome Interval'
    Breed = 'Breed'
    Color = 'Color'
    Lifespan = 'Lifespan'
    LifespanInterval = 'Lifespan Interval'
    Size = 'Size'
    Adaptability = 'Adaptability'
    Breed_definition = 'Breed_definition'
    ColorMix = 'Color Mix'
    PuppyPrice = 'Puppy Price'
    BarkingTendencies = 'Barking Tendencies'
    HealthIssues = 'Health Issues'
    Hypoallergic = 'Hypoallergic'
    LitterSize = 'Litter Size'
    CatFriendly = 'Cat Friendly'
    ExerciseNeeds = 'Exercise Needs'
    Grooming = 'Grooming'
    SheddingLevel = 'Shedding Level'
    ChildFriendly = 'Child Friendly'
    WatchdogAbility = 'Watchdog Ability'
    DogFriendly = 'Dog Friendly'
    StrangerFriendly = 'Stranger Friendly'
    OtherNames = 'Other Names'
    Intelligence = 'Intelligence'
    Trainability = 'Trainability'
    ApartmentFriendly = 'Apartment Friendly'
    Playfulness = 'Playfulness'
    SexSituationUponOutcome = 'SexSituationUponOutcome'

    AffectionLevel = 'Affection Level'
    Vocalization = 'Vocalization'
    MaxPounds = 'Max Pounds'
    SocialNeeds = 'Social Needs'
    EnergyLevel = 'Energy Level'
    KittenPrice = 'Kitten Price'
    LapCat = 'Lap Cat'
    Shedding = 'Shedding'


    def __repr__(self):
        return str(self.value)
