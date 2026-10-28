#!/usr/bin/env python3
"""Apply Tardis-specific Windows console, network and firewall fixes to host.py.

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

FIREWALL_HELPER = '''def ensure_windows_firewall_rule(name, protocol, port):
    """Best-effort inbound-allow rule on Windows Defender Firewall.

    A blocked bind raises OSError and is already reported via bind_hint(),
    but a firewall drop is silent: the socket binds fine, the console looks
    healthy, and the PS5's packets simply never arrive. No-op on non-Windows.
    Both the .ps1 launcher and the --uac-admin PyInstaller build already run
    elevated by the time this runs, which `netsh advfirewall` requires.
    """
    if os.name != "nt":
        return True
    try:
        subprocess.run(
            [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={name}", "dir=in", "action=allow",
                f"protocol={protocol}", f"localport={port}",
                "remoteip=localsubnet",
            ],
            check=True, capture_output=True,
        )
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


'''

FIREWALL_DNS_CALL = '''        if os.name == "nt":
            if not ensure_windows_firewall_rule(
                "Tardis WebKit Autoloader (DNS)", "UDP", args.dns_port
            ):
                note("Could not add a Windows Firewall rule for this port.")
                note("If the PS5 never shows up below, allow it manually: Windows")
                note("Defender Firewall -> Advanced settings -> Inbound Rules ->")
                note(f"New Rule -> Port -> UDP -> {args.dns_port} -> Allow.")
            else:
                good(f"Windows Firewall allows local-network DNS on UDP {args.dns_port}.")
'''

FIREWALL_HTTPS_CALL = '''        if os.name == "nt":
            if not ensure_windows_firewall_rule(
                "Tardis WebKit Autoloader (HTTPS)", "TCP", args.https_port
            ):
                note("Could not add a Windows Firewall rule for this port.")
                note("If the PS5 never shows up below, allow it manually: Windows")
                note("Defender Firewall -> Advanced settings -> Inbound Rules ->")
                note(f"New Rule -> Port -> TCP -> {args.https_port} -> Allow.")
            else:
                good(f"Windows Firewall allows local-network HTTPS on TCP {args.https_port}.")
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

    if (
        "Other local IPv4 addresses:" not in source
        and "The PS5 must use this computer's address as DNS." not in source
    ):
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
        else:
            anchor = '    good(f"Spoofing {style(args.target, 1)} -> {style(ip, 1, 33)}")\n'
            if source.count(anchor) != 1:
                raise ValueError("Could not find the upstream host startup message")
            source = source.replace(anchor, anchor + IP_DIAGNOSTICS, 1)

    if "def ensure_windows_firewall_rule" not in source:
        anchor = "def validate_ip(value):\n"
        if source.count(anchor) != 1:
            raise ValueError("Could not find the upstream IP validation function")
        source = source.replace(anchor, FIREWALL_HELPER + anchor, 1)

    # Migrate hosts generated by earlier Tardis builds, whose firewall helper
    # existed but was not restricted to the local subnet.
    if "remoteip=localsubnet" not in source:
        anchor = '                f"protocol={protocol}", f"localport={port}",\n'
        if source.count(anchor) != 1:
            raise ValueError("Could not find the existing firewall rule arguments")
        source = source.replace(
            anchor,
            anchor + '                "remoteip=localsubnet",\n',
            1,
        )

    if "Tardis WebKit Autoloader (DNS)" not in source:
        anchor = '        good(f"DNS on UDP {args.dns_port}")\n'
        if source.count(anchor) != 1:
            raise ValueError("Could not find the upstream DNS startup message")
        source = source.replace(anchor, anchor + FIREWALL_DNS_CALL, 1)

    if "Tardis WebKit Autoloader (HTTPS)" not in source:
        anchor = '        good(f"HTTPS on TCP {args.https_port} (self-signed)")\n'
        if source.count(anchor) != 1:
            raise ValueError("Could not find the upstream HTTPS startup message")
        source = source.replace(anchor, anchor + FIREWALL_HTTPS_CALL, 1)

    # Upgrade older generated hosts too, not just builds made from the clean
    # upstream submodule. Their calls were unconditional and reported a
    # Windows Firewall success on macOS/Linux, where this feature is a no-op.
    for service, server_name in (("DNS", "dns"), ("HTTPS", "httpsd")):
        old_start = (
            f'        if not ensure_windows_firewall_rule(\n'
            f'            "Tardis WebKit Autoloader ({service})"'
        )
        start = source.find(old_start)
        while start != -1 and start > 0 and source[start - 1] != "\n":
            start = source.find(old_start, start + len(old_start))
        if start != -1:
            end_anchor = f"\n        servers.append({server_name})"
            end = source.find(end_anchor, start)
            if end == -1:
                raise ValueError(f"Could not find the end of the legacy {service} firewall call")
            legacy_call = source[start:end]
            indented_call = "\n".join("    " + line for line in legacy_call.splitlines())
            source = (
                source[:start]
                + '        if os.name == "nt":\n'
                + indented_call
                + source[end:]
            )

    required = (
        "def ensure_windows_firewall_rule",
        "Tardis WebKit Autoloader (DNS)",
        "Tardis WebKit Autoloader (HTTPS)",
        "remoteip=localsubnet",
        "Waiting for the PS5. Open Settings -> User's Guide when ready.",
    )
    missing = [marker for marker in required if marker not in source]
    if missing:
        raise ValueError(
            "Prepared host is missing required Windows/startup logic: "
            + ", ".join(missing)
        )

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
