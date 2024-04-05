# Akai EWI USB MIDI Wind Controller Notes

## MIDI implementation

### Reset

If you press the "RESET" button on the lower backside, the EWI will sent the
following MIDI messages on its configured MIDI channel:

* Pitch bend. value 0
* Control change #121, value 0
* Control change #7, value 100
* Control change #11, value 127
* Channel aftertouch, value 0
* Note Off for all notes 0-127
