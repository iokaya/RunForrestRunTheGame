import enum


class WaitingJob(enum.Enum):
    NoWaitingJob = 0
    SelectRunnerPlace = 1
    SelectChaser1Place = 2
    SelectChaser2Place = 3
    SelectRockPlace = 4
    ChangeRunnerPlace = 5


class ButtonType(enum.Enum):
    Header = 'HD'
    Grass = 'GR'
    Obstacle = 'OB'
    Runner = 'RN'
    Chaser1 = 'C1'
    Chaser2 = 'C2'