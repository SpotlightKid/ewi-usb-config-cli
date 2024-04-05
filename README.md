# ewi-usb-config-cli

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Configure an Akai EWI USB MIDI wind controller via MIDI from the command line
on Linux, macOS or Windows.


### Installation

Via [pip](https://github.com/pypa/pip):

```con
pip install ewi-usb-config-cli
```

Via [pipx](https://github.com/pypa/pipx):

```con
pipx install ewi-usb-config-cli
```


## Usage

```
usage: ewi-usb-config [-h] [-d DEVICE_ID] [-a] [-f] [-r PATH] [--all-banks]
                      [-s PATH] [-p PORT] [-t TIMEOUT] [-v] [--version]
                      [setting ...]

Configure an Akai EWI USB MIDI wind controller via MIDI.

positional arguments:
  setting               Setting to send to EWI in the form name=value (can be
                        given more than once)

options:
  -h, --help            show this help message and exit
  -d DEVICE_ID, --device-id DEVICE_ID
                        SysEx Device ID (default: 0x7F)
  -a, --ascii           Set SysEx dump output format to ASCII hexadecimal
                        values
  -f, --force           Allow overwriting existing file when writing received
                        SysEx dump
  -r PATH, --receive PATH
                        Receive SysEx dump from EWI and save in file PATH (use
                        '-' to write to standard output)
  --all-banks           Request all settings banks (0-3) (the purpose of banks
                        1 and 3 is unclear)
  -s PATH, --send PATH  Send SysEx dump file PATH to EWI (use '-' to read from
                        standard input)
  -p PORT, --port PORT  Number or (part of) name of MIDI input/output port to
                        open (default: 'EWI-USB')
  -t TIMEOUT, --timeout TIMEOUT
                        SysEx dump reception timeout (default: 5)
  -v, --verbose         Output verbose messages of program operation to stderr
  --version             show program's version number and exit

Settings:
   breath-gain, bite-gain, bite-ac-gain, pb-gain, key-delay, unknown-1,
   midi-channel, fingering, transposition, velocity, breath-cc-1, breath-cc-2,
   unknown-2, bite-cc-1, bite-cc-2, pb-up-cc, pb-down-cc
```


## Examples

Connect your Akai EWI USB wind controller via USB and use your system's MIDI
tools to check that it shows up as MIDI input and output ports having names
with "EWI-USB" in them.

Then use the terminal to send commands to your EWI using the `ewi-usb-config`
program.

For example, to set the key delay to 10 (the factory default value is 7):

```con
ewi-usb-config key-delay=10
```

Configure the MIDI control change type, which is sent when biting on the mouth
piece to only *Modulation* (CC #1) an disable it sending *Pitch Bend" as well.
Also set the bite gain a rather low value 20 (the factory default value is 64):

```con
ewi-usb-config bite-cc-1=0 bite-cc-2=1 bite-gain=20
```

Configure the MIDI messages types, which are sent in response to breath input,
to *Breath Controller* (CC #2) and *Channel Aftertouch*, which is the factory
default behaviour:

```con
ewi-usb-config breath-cc-1=2 breath-cc-2=127
```

Retrieve all current settings from the device as a MIDI System Exclusive (SysEx)
dump and write it to the file `ewi-usb.syx` using the `-r|--receive` option:

```con
ewi-usb-config -r ewi-usb.syx
```

Send a SysEx dump to the device to restore all settings saved in the dump using
the `-s|--send` option:

```con
ewi-usb-config -s ewi-usb.syx
```

Retrieve a settings dump but output the SysEx data as hexadecimal numbers in
ASCII to the standard output by adding the `-a|--ascii` option and using `-` as
the output filename to indicate standard output:

```con
ewi-usb-config --ascii r -
```

This produces output like this:

```
F0 47 7F 6D 00 00 06 40 40 40 40 07 7F F7
F0 47 7F 6D 02 00 0B 00 00 40 78 02 7F 00 7F 00 7F 7F F7
```

Note that this format can not be loaded back into the EWI USB. It is meant
mainly as a debugging tool for developers.


## Controller Settings Values

| Value | Breath CC 1   | Breath CC 2   | Bite CC 1         | Bite CC 2     | Pitch Plate Up | Pitch Plate Down |
| ----- | ------------- | ------------- | ----------------- | ------------- | -------------- | ---------------- |
| 0     | OFF           | OFF           | OFF               | OFF           | OFF            | OFF              |
| 1-119 | MIDI CC 1-119 | MIDI CC 1-119 | MIDI CC 1-119     | MIDI CC 1-119 | MIDI CC 1-119  | MIDI CC 1-119    |
| 124   | -             | -             | Pitchbend UP      | -             | -              | -                |
| 125   | -             | -             | Pitchbend DOWN    | -             | -              | -                |
| 126   | -             | -             | Pitchbend up-down | -             | -              | -                |
| 127   | Aftertouch    | Aftertouch    | Pitchbend down-up | Aftertouch    | Pitchbend UP   | Pitchbend DOWN   |


*Aftertouch* is always *Channel Pressure*, aka *Mono Aftertouch*.
*Note Pressure*, aka *Poly Aftertouch*, is not supported.


## Development

Using the [poetry](https://python-poetry.org/) tool:

- `poetry config virtualenvs.in-project true`
- `poetry install`
- `poetry run ewi-usb-config --version`
- `poetry run ewi-usb-config --help`
- `poetry run ewi-usb-config`
- `poetry check`


## Deployment

- `poetry version minor` or `poetry version patch`
- `poetry build`
