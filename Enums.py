import enum


class WaitingJob(enum.Enum):
    ApplyConfiguration = 0
    SelectRunnerPlace = 1
    SelectChaser1Place = 2
    SelectChaser2Place = 3
    SelectObstaclePlace = 4
    StartGame = 5
    PlayRunner = 6
    PlayChaser1 = 7
    PlayChaser2 = 8
    NoWaitingJob = 99
    EndGame = 100


class ButtonType(enum.Enum):
    Header = 'H'
    Grass = 'G'
    Obstacle = 'O'
    Runner = 'R'
    Chaser1 = 'C1'
    Chaser2 = 'C2'
    ApplyConfig = 'A'
    StartGame = 'S'
    TrainAgents = 'T'


class PlaceConfig(enum.Enum):
    Default = 0
    Random = 1
    Manual = 2


class BehaviorConfig(enum.Enum):
    Auto = 0
    Manual = 1
