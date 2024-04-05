#!/usr/bin/env python3
"""Configure an Akai EWI USB MIDI wind controller via MIDI.

Supported NRPNs:

    0/0 Breath gain (default: 64)
    0/1 Bite gain (default: 64)
    0/2 Bite AC gain (default: 64)
    0/3 Pitch bend gain (default: 64)
    0/4 Key delay (default: 7)
    2/0 MIDI channel (default: 0)
    2/1 Fingering mode (default: 0)
    2/2 Transpose (52 - 76, default: 64 = +/-0 (C))
    2/3 Velocity (default: 0 (Dynamic))
    2/4 Breath CC 1 (0 = OFF, default: 2 = CC #2 (Breath))
    2/5 Breath CC 2 (0 = OFF, default: 127 = Aftertouch)
    2/7 Bite CC 1 (0 = OFF, default: 127 = Pitchbend down-up)
    2/8 Bite CC 2 (default: 0 = OFF)
    2/9 Pitchbend UP (0 = OFF, default: 127 = Pitchbend UP)
    2/10 Pitchbend DOWN (0 = OFF, default: 127 = Pitchbend DOWN)

Fingering modes:

    0 - EWI standard
    1 - Saxophone
    2 - Flute
    3 - Oboe
    4 - EVI valve 1
    5 - EVI valve 2 (reversed PB pads)

"""

import argparse
import logging
import sys
from datetime import datetime
from os.path import exists
from time import sleep, time

from rtmidi import midiutil

from .ewidata import *
from .version import version as __version__


PROG = "ewi-usb-config"

log = logging.getLogger(PROG)


class SysexMessage(object):
    @classmethod
    def fromdata(cls, data):
        self = cls()
        if data[0] != SYSTEM_EXCLUSIVE:
            raise ValueError("Message does not start with 0xF0", data)
        if data[-1] != END_OF_EXCLUSIVE:
            raise ValueError("Message does not end with 0xF7", data)
        if len(data) < 5:
            raise ValueError("Message too short", data)
        if data[1] == 0:
            self.manufacturer_id = (data[1], data[2], data[3])
            self.model_id = data[5]
            self.device_id = data[6]
        else:
            self.manufacturer_id = data[1]
            self.model_id = data[3]
            self.device_id = data[2]

        self._data = data
        return self

    def __getitem__(self, i):
        return self._data[i]

    def __getslice(self, i, j):
        return self._data[i:j]

    def __repr__(self):
        return " ".join(["%02X" % b for b in self._data])

    def as_bytes(self):
        return bytes(self._data)


class AkaiEWIUSB:
    def __init__(self, midiout, midiin=None, ch=1, device_id=0x7F):
        self.channel = ch
        self._midiout = midiout
        self._midiin = midiin
        self.device_id = device_id
        self._received_dumps = []

        if self._midiin:
            log.debug("Attaching MIDI input callback handler.")
            self._midiin.set_callback(self)
            log.debug("Enabling reception of sysex messages.")
            self._midiin.ignore_types(sysex=False)

    def close(self):
        if self._midiout:
            self._midiout.close_port()
            del self._midiout
        if self._midiin:
            self._midiin.close_port()
            del self._midiin

    def send_channel_message(self, status, data1=None, data2=None, ch=None):
        """Send a MIDI channel mode message."""
        msg = [(status & 0xF0) | ((ch if ch else self.channel) - 1 & 0xF)]

        if data1 is not None:
            msg.append(data1 & 0x7F)

            if data2 is not None:
                msg.append(data2 & 0x7F)

        self._midiout.send_message(msg)

    def send_control_change(self, cc=0, value=0, ch=None):
        """Send a 'Control Change' message."""
        self.send_channel_message(CONTROL_CHANGE, cc, value, ch=ch)

    def send_nrpn(self, param=0, value=0, ch=None):
        """Send a Non-Registered Parameter Number (NRPN) Change via a series of CC messages."""
        if isinstance(param, int):
            param_msb = param >> 7
            param_lsb = param
        else:
            param_msb, param_lsb = param

        if param_msb is not None:
            self.send_control_change(NRPN_MSB, param_msb, ch=ch)

        if param_lsb is not None:
            self.send_control_change(NRPN_LSB, param_lsb, ch=ch)

        if isinstance(value, int):
            value_msb = value >> 7
            value_lsb = value
        else:
            value_msb, value_lsb = value

        if value_msb is not None:
            self.send_control_change(DATA_ENTRY_MSB, value_msb, ch=ch)

        if value_lsb is not None:
            self.send_control_change(DATA_ENTRY_LSB, value_lsb, ch=ch)

    def send_system_exclusive(self, msg=""):
        """Send a MIDI system exclusive (SysEx) message."""
        if (
            msg
            and msg.startswith(b"\xF0")
            and msg.endswith(b"\xF7")
            and all((val <= 0x7F for val in msg[1:-1]))
        ):
            self._midiout.send_message(msg)
        else:
            raise ValueError("Invalid sysex string: %s", msg)

    def __call__(self, event, data=None):
        try:
            message, deltatime = event
            if message[:1] != [SYSTEM_EXCLUSIVE]:
                return

            dt = datetime.now()
            log.debug(
                "[%s: %s] Received sysex msg of %i bytes."
                % ("EWI USB", dt.strftime("%x %X"), len(message))
            )
            sysex = SysexMessage.fromdata(message)

            if (
                sysex.manufacturer_id == MANUFACTURER_ID_AKAI
                and sysex.model_id == MODEL_ID_EWI_USB
            ):
                self._received_dumps.append(sysex)
        except Exception as exc:
            msg = "Error handling MIDI message: %s" % exc.args[0]
            if self.debug:
                log.debug(msg)
                if len(exc.args) >= 2:
                    log.debug("Message data: %r", exc.args[1])
            else:
                log.error(msg)

    def set(self, setting: NRPN, value):
        self.send_nrpn(setting, (int(value), None))


def do_request_dump(args):
    mo, mo_name = midiutil.open_midioutput(args.port, client_name=PROG)
    mi, mi_name = midiutil.open_midiinput(args.port, client_name=PROG)
    akai = AkaiEWIUSB(mo, mi, device_id=args.device_id)
    sysex = []

    akai.send_nrpn((1, 4), (0x20, None))

    log.info("Requesting dumps. Waiting to receive... Press Control-C to cancel.")
    try:
        for bank in range(4) if args.all_banks else (0, 2):
            akai.send_system_exclusive(
                bytes(
                    [
                        SYSTEM_EXCLUSIVE,
                        MANUFACTURER_ID_AKAI,
                        akai.device_id,
                        MODEL_ID_EWI_USB,
                        MSG_ID_DUMP_REQUEST + bank,
                        0,
                        0,
                        END_OF_EXCLUSIVE,
                    ]
                )
            )
            start = time()
            while True:
                if akai._received_dumps:
                    sysex.append(akai._received_dumps.pop(0))
                    break
                if time() - start > args.timeout:
                    log.error("Timeout exceeded.")
                    break

                sleep(0.05)
    except KeyboardInterrupt:
        print("")
    finally:
        akai.send_nrpn((1, 4), (0x10, None))
        log.debug("Exit.")
        akai.close()

    if sysex:
        mode = "w" if args.ascii else "wb"

        with open(args.receive, mode) if args.receive != "-" else sys.stdout as fp:
            for msg in sysex:
                if args.ascii:
                    fp.write(repr(msg) + "\n")
                else:
                    fp.write(msg.as_bytes())


def read_sysex(fp, manufacturer_id=None, model_id=None, max_size=1024):
    sysex = []
    msg = None
    bytes_read = 0

    while bytes_read <= max_size and (byte := fp.read(1)):
        bytes_read += 1

        if byte[0] == SYSTEM_EXCLUSIVE:
            msg = byte
        elif msg is not None:
            msg += byte

        if byte[0] == END_OF_EXCLUSIVE:
            if (manufacturer_id is not None and msg[1] != manufacturer_id) or (
                model_id is not None and msg[3] != model_id
            ):
                log.debug(f"Read unsupported SysEx message: {msg!r}")
            else:
                sysex.append(msg)
            msg = None

    return sysex


def do_send_dump(args):
    with open(args.send, "rb") if args.send != "-" else sys.stdin.buffer as fp:
        sysex = read_sysex(fp, MANUFACTURER_ID_AKAI, MODEL_ID_EWI_USB)

    if sysex:
        mo, _ = midiutil.open_midioutput(args.port, client_name=PROG)
        akai = AkaiEWIUSB(mo, device_id=args.device_id)

        akai.send_nrpn((1, 4), (0x20, None))

        for i, msg in enumerate(sysex):
            log.info(f"Sending SysEx message with {len(msg)} bytes.")
            akai.send_system_exclusive(msg)

        akai.send_nrpn((1, 4), (0x10, None))

        akai.close()
    else:
        log.error(
            f"No supported SysEx message found in '{args.send}'. Nothing was sent."
        )


def main(args=None):
    params = [e.name.lower().replace("_", "-") for e in NRPN]
    ap = argparse.ArgumentParser(
        prog=PROG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__.splitlines()[0],
        epilog=f"Settings:\n   {', '.join(params)}",
        fromfile_prefix_chars="@",
    )
    ap.add_argument(
        "-d",
        "--device-id",
        type=int,
        default=0x7F,
        help="SysEx Device ID (default: 0x%(default)02X)",
    )
    ap.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="Set SysEx dump output format to ASCII hexadecimal values",
    )
    ap.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Allow overwriting existing file when writing received SysEx dump",
    )
    ap.add_argument(
        "-r",
        "--receive",
        metavar="PATH",
        help=(
            "Receive SysEx dump from EWI and save in file PATH "
            "(use '-' to write to standard output)"
        ),
    )
    ap.add_argument(
        "--all-banks",
        action="store_true",
        help="Request all settings banks (0-3) (the purpose of banks 1 and 3 is unclear)",
    )
    ap.add_argument(
        "-s",
        "--send",
        metavar="PATH",
        help="Send SysEx dump file PATH to EWI (use '-' to read from standard input)",
    )
    ap.add_argument(
        "-p",
        "--port",
        default="EWI-USB",
        help="Number or (part of) name of MIDI input/output port to open (default: %(default)r)",
    )
    ap.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=5,
        help="SysEx dump reception timeout (default: %(default)i)",
    )
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Output verbose messages of program operation to stderr",
    )
    ap.add_argument(
        "setting",
        nargs="*",
        help="Setting to send to EWI in the form name=value (can be given more than once)",
    )
    ap.add_argument("--version", action="version", version="%(prog)s " + __version__)

    args = ap.parse_args(args)

    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.INFO if args.verbose else logging.WARNING,
    )
    midiutil.log = log

    if not any([args.send, args.receive, args.setting]):
        ap.print_usage()
        return

    if args.receive:
        if args.receive != "-" and exists(args.receive):
            if args.force:
                log.warning(f"Overwriting exiting file '{args.receive}'.")
            else:
                log.error(
                    f"File '{args.receive}' exist. Use option -f to overwrite. Aborting."
                )
                return

        try:
            do_request_dump(args)
        except (KeyboardInterrupt, EOFError):
            return 1

    if args.send:
        if args.send != "-" and not exists(args.send):
            log.error(f"File not found: '{args.send}'. Aborting.")
            return

        try:
            do_send_dump(args)
        except (KeyboardInterrupt, EOFError):
            return 1

    if args.setting:
        try:
            mo, name = midiutil.open_midioutput(args.port)
        except (KeyboardInterrupt, EOFError):
            return

        akai = AkaiEWIUSB(mo)

        for setting in args.setting:
            try:
                name, value = setting.split("=")
            except ValueError:
                log.error("Skipping mal-formed setting (use: name=value).")

            try:
                if not 0 < (value := int(value)) < 128:
                    raise ValueError("Out of range")
            except ValueError:
                log.error(f"Value for setting '{name}' must be an integer 0..127.")
                continue

            name = name.upper().replace("-", "_")

            if name in NRPN.__members__:
                log.info(f"Sending NRPN {NRPN[name].value} ({name}) value={value}")
                akai.set(NRPN[name].value, value)
            else:
                ap.print_help()
                return "Setting '{name}' not supported."

        akai.close()


if __name__ == "__main__":
    sys.exit(main() or 0)
