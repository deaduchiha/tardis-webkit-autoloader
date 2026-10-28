#!/bin/zsh

# Finder double-click launcher for the embedded PS5 setup host.
# The host needs privileged DNS/HTTPS ports 53 and 443.

set -eu

PROJECT_DIR="${0:A:h}"
HOST_SCRIPT="$PROJECT_DIR/webkit-autoloader-host.py"
PYTHON_BIN="$(command -v python3 || true)"

if [[ ! -f "$HOST_SCRIPT" ]]; then
  print "Tardis setup host was not found:"
  print "  $HOST_SCRIPT"
  print "Build it first with: make host HOST_PAYLOAD=<installer.elf>"
  print ""
  read "?Press Return to close..."
  exit 1
fi

if [[ -z "$PYTHON_BIN" ]]; then
  print "Python 3 was not found. Install Python 3, then open this launcher again."
  print ""
  read "?Press Return to close..."
  exit 1
fi

cd "$PROJECT_DIR"
print "Starting the Tardis PS5 setup host. macOS will ask for your administrator password."
print "Leave this Terminal window open while using the PS5. Press Control-C to stop."
print ""
exec sudo "$PYTHON_BIN" "$HOST_SCRIPT" --verbose
