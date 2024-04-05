import enum

from rtmidi.midiconstants import BREATH_CONTROLLER, MODULATION

MANUFACTURER_ID_AKAI = 0x47
MODEL_ID_EWI_USB = 0x6D
MSG_ID_DUMP_REQUEST = 0x40
OFF = 0


class Fingering(enum.IntEnum):
    EWI = 0
    SAXOPHONE = 1
    FLUTE = 2
    OBOE = 3
    EVI_VALVE_1 = 4
    EVI_VALVE_2 = 5


class NRPN(enum.Enum):
    BREATH_GAIN = (0, 0)
    BITE_GAIN = (0, 1)
    BITE_AC_GAIN = (0, 2)
    PB_GAIN = (0, 3)
    KEY_DELAY = (0, 4)
    UNKNOWN_1 = (0, 5)
    MIDI_CHANNEL = (2, 0)
    FINGERING = (2, 1)
    TRANSPOSITION = (2, 2)
    VELOCITY = (2, 3)
    BREATH_CC_1 = (2, 4)
    BREATH_CC_2 = (2, 5)
    UNKNOWN_2 = (2, 6)
    BITE_CC_1 = (2, 7)
    BITE_CC_2 = (2, 8)
    PB_UP_CC = (2, 9)
    PB_DOWN_CC = (2, 10)


MIDI_CHANNEL = (
    ("Channel 1", 0),
    ("Channel 2", 1),
    ("Channel 3", 2),
    ("Channel 4", 3),
    ("Channel 5", 4),
    ("Channel 6", 5),
    ("Channel 7", 6),
    ("Channel 8", 7),
    ("Channel 9", 8),
    ("Channel 10", 9),
    ("Channel 11", 10),
    ("Channel 12", 11),
    ("Channel 13", 12),
    ("Channel 14", 13),
    ("Channel 15", 14),
    ("Channel 16", 15),
)

TRANSPOSITION = {
    "-12 = -C": 52,
    "-11 = -Db": 53,
    "-10 = -D": 54,
    "-9 = -Eb": 55,
    "-8 = -E": 56,
    "-7 = -F": 57,
    "-6 = -Gb": 58,
    "-5 = -G": 59,
    "-4 = -Ab": 60,
    "-3 = -A": 61,
    "-2 = -Bb": 62,
    "-1 = -B": 63,
    "0 = C": 64,
    "1 = +C#": 65,
    "2 = +D": 66,
    "3 = +D#": 67,
    "4 = +E": 68,
    "5 = +F": 69,
    "6 = +F#": 70,
    "7 = +G": 71,
    "8 = +G#": 72,
    "9 = +A": 73,
    "10 = +A#": 74,
    "11 = +B": 75,
    "12 = +C": 76,
}

CONTROLLERS = (
    ("OFF", 0),
    ("1 Modulation Wheel (coarse)", 1),
    ("2 Breath controller (coarse)", 2),
    ("3", 3),
    ("4 Foot Pedal (coarse)", 4),
    ("5 Portamento Time (coarse)", 5),
    ("6 Data Entry (coarse)", 6),
    ("7 Volume (coarse)", 7),
    ("8 Balance (coarse)", 8),
    ("9", 9),
    ("10 Pan position (coarse)", 10),
    ("11 Expression (coarse)", 11),
    ("12 Effect Control 1 (coarse)", 12),
    ("13 Effect Control 2 (coarse)", 13),
    ("14", 14),
    ("15", 15),
    ("16 General Purpose Slider 1", 16),
    ("17 General Purpose Slider 2", 17),
    ("18 General Purpose Slider 3", 18),
    ("19 General Purpose Slider 4", 19),
    ("20", 20),
    ("21", 21),
    ("22", 22),
    ("23", 23),
    ("24", 24),
    ("25", 25),
    ("26", 26),
    ("27", 27),
    ("28", 28),
    ("29", 29),
    ("30", 30),
    ("31", 31),
    ("32  Bank Select (fine)", 32),
    ("33  Modulation Wheel (fine)", 33),
    ("34  Breath controller (fine)", 34),
    ("35", 35),
    ("36  Foot Pedal (fine)", 36),
    ("37  Portamento Time (fine)", 37),
    ("38  Data Entry (fine)", 38),
    ("39  Volume (fine)", 39),
    ("40  Balance (fine)", 40),
    ("41", 41),
    ("42  Pan position (fine)", 42),
    ("43  Expression (fine)", 43),
    ("44  Effect Control 1 (fine)", 44),
    ("45  Effect Control 2 (fine)", 45),
    ("46", 46),
    ("47", 47),
    ("48", 48),
    ("49", 49),
    ("50", 50),
    ("51", 51),
    ("52", 52),
    ("53", 53),
    ("54", 54),
    ("55", 55),
    ("56", 56),
    ("57", 57),
    ("58", 58),
    ("59", 59),
    ("60", 60),
    ("61", 61),
    ("62", 62),
    ("63", 63),
    ("64 Hold Pedal (on/off)", 64),
    ("65 Portamento (on/off)", 65),
    ("66 Sustenuto Pedal (on/off)", 66),
    ("67 Soft Pedal (on/off)", 67),
    ("68 Legato Pedal (on/off)", 68),
    ("69 Hold 2 Pedal (on/off)", 69),
    ("70 Sound Variation", 70),
    ("71 Sound Timbre", 71),
    ("72 Sound Release Time", 72),
    ("73 Sound Attack Time", 73),
    ("74 Sound Brightness", 74),
    ("75 Sound Control 6", 75),
    ("76 Sound Control 7", 76),
    ("77 Sound Control 8", 77),
    ("78 Sound Control 9", 78),
    ("79  Sound Control 10", 79),
    ("80 General Purpose Button 1 (on/off)", 80),
    ("81 General Purpose Button 2 (on/off)", 81),
    ("82 General Purpose Button 3 (on/off)", 82),
    ("83 General Purpose Button 4 (on/off)", 83),
    ("84", 84),
    ("85", 85),
    ("86", 86),
    ("87", 87),
    ("88", 88),
    ("89", 89),
    ("90", 90),
    ("91 Effects Level", 91),
    ("92 Tremulo Level", 92),
    ("93 Chorus Level", 93),
    ("94 Celeste Level", 94),
    ("95 Phaser Level", 95),
    ("96 Data Button increment", 96),
    ("97 Data Button decrement", 97),
    ("98 Non-registered Parameter (fine)", 98),
    ("99 Non-registered Parameter (coarse)", 99),
    ("100 Registered Parameter (fine)", 100),
    ("101 Registered Parameter (coarse)", 101),
    ("102", 102),
    ("103", 103),
    ("104", 104),
    ("105", 105),
    ("106", 106),
    ("107", 107),
    ("108", 108),
    ("109", 109),
    ("110", 110),
    ("111", 111),
    ("112", 112),
    ("113", 113),
    ("114", 114),
    ("115", 115),
    ("116", 116),
    ("117", 117),
    ("118", 118),
    ("119", 119),
)

CONTROLLERS_BREATH_CC_1 = CONTROLLERS + (("Aftertouch", 127),)

CONTROLLERS_BREATH_CC_2 = CONTROLLERS + (("Aftertouch", 127),)

CONTROLLERS_BITE_CC_1 = CONTROLLERS + (
    ("124 Pitchbend Up", 124),
    ("125 Pitchbend Down", 125),
    ("126 Pitchbend up-down", 126),
    ("127 Pitchbend down-up", 127),
)

CONTROLLERS_BITE_CC_2 = CONTROLLERS + (("Aftertouch", 127),)

CONTROLLERS_PB_UP = CONTROLLERS + (("Pitchbend UP", 127),)

CONTROLLERS_PB_DOWN = CONTROLLERS + (("Pitchbend DOWN", 127),)

PROFILE_DEFAULT = {
    NRPN.BREATH_GAIN: 64,
    NRPN.BITE_GAIN: 64,
    NRPN.BITE_AC_GAIN: 64,
    NRPN.PB_GAIN: 64,
    NRPN.KEY_DELAY: 7,
    NRPN.MIDI_CHANNEL: 0,
    NRPN.FINGERING: Fingering.EWI.value,
    NRPN.TRANSPOSITION: 64,
    NRPN.VELOCITY: 120,
    NRPN.BREATH_CC_1: BREATH_CONTROLLER,
    NRPN.BREATH_CC_2: 127,
    NRPN.BITE_CC_1: 127,
    NRPN.BITE_CC_2: OFF,
    NRPN.PB_UP_CC: 127,
    NRPN.PB_DOWN_CC: 127,
}

PROFILE_FAVOURITE = PROFILE_DEFAULT.update(
    {
        NRPN.BITE_GAIN: 20,
        NRPN.KEY_DELAY: 10,
        NRPN.BREATH_CC_1: BREATH_CONTROLLER,
        NRPN.BREATH_CC_2: OFF,
        NRPN.BITE_CC_1: OFF,
        NRPN.BITE_CC_2: MODULATION,
    }
)
