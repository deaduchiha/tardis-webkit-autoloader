#!/usr/bin/env python3
"""Apply Tardis-specific Windows console and network diagnostics to host.py.

The remote-loader is a pinned upstream submodule. Keeping these small host
customizations here makes release builds reproducible without committing local
changes inside that submodule or depending on an upstream-only commit.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


WINDOWS_COLOR = '''COLOR = sys.stdout.isatty()
if COLOR and os.name == "nt":
    # Some Windows console hosts report isatty() == True but do not interpret
    # ANSI escapes. Enable virtual-terminal output where supported; otherwise
    # use plain text instead of leaking escape sequences into the console.
    try:
        import ctypes

        _kernel32 = ctypes.windll.kernel32
        _std_output_handle = -11
        _enable_virtual_terminal_processing = 0x0004
        _handle = _kernel32.GetStdHandle(_std_output_handle)
        _mode = ctypes.c_uint32()
        if not _kernel32.GetConsoleMode(_handle, ctypes.byref(_mode)):
            raise OSError("GetConsoleMode failed")
        if not _kernel32.SetConsoleMode(
            _handle, _mode.value | _enable_virtual_terminal_processing
        ):
            raise OSError("SetConsoleMode failed")
    except Exception:
        COLOR = False
'''

LOCAL_IP_HELPER = '''def list_local_ips():
    """Best-effort list of non-loopback IPv4 addresses on this computer."""
    ips = set()
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except OSError:
        pass
    return sorted(ips)


'''

IP_DIAGNOSTICS = '''    other_ips = [address for address in list_local_ips() if address != ip]
    if other_ips and args.ip is None:
        note(f"Other local IPv4 addresses: {', '.join(other_ips)}")
        note("If the PS5 cannot reach the selected address, it may be on")
        note("another network. Restart with --ip <address> to select one.")
    note("The PS5 must use this computer's address as DNS; this host cannot")
    note("change the PS5 network settings for you.")
'''


def patch(source: str) -> str:
    if "# TARDIS_WINDOWS_CONSOLE" not in source:
        anchor = "COLOR = sys.stdout.isatty()\n"
        if source.count(anchor) != 1:
            raise ValueError("Could not find the upstream console-color setting")
        marker = "# TARDIS_WINDOWS_CONSOLE\n"
        if 'if COLOR and os.name == "nt":' in source:
            # This checkout already contains the developer's local version of
            # the patch; mark it so subsequent builds stay idempotent.
            source = source.replace(anchor, marker + anchor, 1)
        else:
            block = WINDOWS_COLOR.replace(anchor, marker + anchor, 1)
            source = source.replace(anchor, block, 1)

    if "def list_local_ips():" not in source:
        anchor = "def validate_ip(value):\n"
        if source.count(anchor) != 1:
            raise ValueError("Could not find the upstream IP validation function")
        source = source.replace(anchor, LOCAL_IP_HELPER + anchor, 1)

    if "Other local IPv4 addresses:" not in source:
        local_diagnostic = "other_ips = [i for i in list_local_ips() if i != ip]"
        if local_diagnostic in source:
            anchor = '        note("networks instead -- pass --ip <address> to pick it explicitly.")\n'
            if source.count(anchor) != 1:
                raise ValueError("Could not find the existing alternate-IP diagnostic")
            source = source.replace(
                anchor,
                anchor + '        note("The PS5 must use this computer\'s address as DNS.")\n',
                1,
            )
            return source
        anchor = '    good(f"Spoofing {style(args.target, 1)} -> {style(ip, 1, 33)}")\n'
        if source.count(anchor) != 1:
            raise ValueError("Could not find the upstream host startup message")
        source = source.replace(anchor, anchor + IP_DIAGNOSTICS, 1)

    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    try:
        result = patch(source)
        compile(result, str(args.output), "exec")
    except (ValueError, SyntaxError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(f"Prepared Tardis host source: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
