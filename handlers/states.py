import enum


class ConversationStates(int, enum.Enum):
    SELECTOR = 0
    TALKING = 1
    RESERVATION = 2
    DESTINATION = 3
    PHONE = 4
    SAVE_REQUEST = 5


class InitialSelectors(str, enum.Enum):
    FORWARDING_PREFIX = "Soporte"
    FORWARDING = f"{FORWARDING_PREFIX} 👩🏽‍💻"
    REQUEST_RIDE_PREFIX = "Quiero Viajar"
    REQUEST_RIDE = f"{REQUEST_RIDE_PREFIX} 💺"
