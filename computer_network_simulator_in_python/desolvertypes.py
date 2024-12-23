from enum import Enum

class Layer1HdrTypes(Enum):
    Void = 0
    PHY802dot15dot4 = 6
    PHYEtherII = 8
    PHY802dot3 = 8

class Layer2HdrTypes(Enum):
    Void = 0
    MAC802dot15dot4 = 23
    MACEtherII = 18
    MAC802dot3 = 22

class Layer3HdrTypes(Enum):
    Void = 0
    IPv4 = 20
    IPv6 = 40

class ServiceTypes(Enum):
    IoTMornitor = 1  # IOT monitoring
    IPerf = 2        # IP Performance testing
    Misc = 3         # miscellaneous, consisting of diverse traffic

class DropTypes(Enum):
    NoDrop = 0
    PktErr = 1
    