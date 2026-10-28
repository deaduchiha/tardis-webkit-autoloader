# PC setup host

The setup host is built by remote-loader's `tools/build_host.py`; this
repository does not maintain a separate DNS/HTTPS implementation. The generated
`webkit-autoloader-host_v<version>.py` embeds standalone HTML pages for both chains
(Relapse and Poops) carrying the installer ELF and a TLS certificate. At runtime, it
automatically routes firmwares where Relapse is unsupported (9.05) to Poops.
It needs only Python's standard library.

Run the generated script, set the PS5's DNS to your PC's IP, then open Settings →
User's Guide. The page runs the exploit and installer; reboot after installation.
On systems requiring elevated privileges for ports 53/443, run the host with sudo.
The host selects its default-route IPv4 address when it starts and reports other
local addresses when it detects multiple adapters. The PS5 must be on a network
that can reach the selected address; restart the host after changing networks,
or pass `--ip <address>` to select another address on the PC. On Windows, it
also adds inbound-allow rules on Windows Defender Firewall for the DNS and
HTTPS ports, since a silently blocked port otherwise looks identical to a
healthy "waiting for the PS5" state; if that fails (e.g. not elevated), it
prints the exact manual steps to allow the port yourself.

For a local HTTP check without DNS or HTTPS:

```sh
python3 webkit-autoloader-host_v<version>.py --no-dns --no-https --http-port 8123
```

Use `--help` for upstream host options. `--extract <directory>` extracts the
embedded page. Build both versioned artifacts with `./build_release.sh`, or build
only the host from an existing installer with:

```sh
make host HOST_PAYLOAD=webkit-autoloader-installer_v<version>.elf
```
