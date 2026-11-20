#!/bin/bash
cd "$HOME"
echo "Installing PostureCoach..."

PYBIN=""
# shortcut: hardcoded python@3.14 preference list; once Homebrew moves past 3.14
# this won't match anymore -- update the list or resolve dynamically via `brew list`.
for candidate in \
  "/opt/homebrew/opt/python@3.14/bin/python3.14" \
  "/opt/homebrew/bin/python3.14" \
  "$(command -v python3.14 2>/dev/null)" \
  "/opt/homebrew/bin/python3" \
  "$(command -v python3 2>/dev/null)"
do
  if [ -n "$candidate" ] && [ -x "$candidate" ]; then
    PYBIN="$candidate"
    break
  fi
done

if [ -z "$PYBIN" ]; then
  echo "Could not find any python3 on this Mac. Install Xcode Command Line Tools"
  echo "(run: xcode-select --install) or Homebrew's python, then re-run this installer."
  read -p "Press enter to close..."
  exit 1
fi

echo "Using interpreter: $PYBIN"

echo "1) Making sure the rumps menu bar library is installed for that interpreter..."
"$PYBIN" -m pip install --user --break-system-packages --upgrade rumps
if [ $? -ne 0 ]; then
  echo "First attempt failed, trying to bootstrap pip first..."
  "$PYBIN" -m ensurepip --upgrade 2>/dev/null
  "$PYBIN" -m pip install --user --break-system-packages --upgrade rumps
  if [ $? -ne 0 ]; then
    echo ""
    echo "rumps install failed for $PYBIN. Check your internet connection and re-run this installer."
    read -p "Press enter to close..."
    exit 1
  fi
fi

SCRIPT_PATH="/Applications/PostureCoach.app/Contents/Resources/posture_coach.py"
PLIST="$HOME/Library/LaunchAgents/com.jessica.posturecoach.plist"
LOG="$HOME/Library/Application Support/PostureCoach/run.log"

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Application Support/PostureCoach"

echo "2) Removing any old Login Item, if present..."
osascript -e 'tell application "System Events" to delete (every login item whose name is "PostureCoach")' 2>/dev/null

echo "3) Installing PostureCoach as a login agent, pinned to $PYBIN ..."
pkill -f posture_coach.py 2>/dev/null
launchctl bootout "gui/$(id -u)/com.jessica.posturecoach" 2>/dev/null

cat > "$PLIST" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jessica.posturecoach</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYBIN</string>
        <string>$SCRIPT_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOG</string>
    <key>StandardErrorPath</key>
    <string>$LOG</string>
    <key>ProcessType</key>
    <string>Interactive</string>
</dict>
</plist>
PLISTEOF

launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/com.jessica.posturecoach"

LAUNCHER="/Applications/PostureCoach.app/Contents/MacOS/PostureCoach"
cat > "$LAUNCHER" << LAUNCHEREOF
#!/bin/bash
LOG="\$HOME/Library/Application Support/PostureCoach/run.log"
mkdir -p "\$HOME/Library/Application Support/PostureCoach"
exec "$PYBIN" "$SCRIPT_PATH" >> "\$LOG" 2>&1
LAUNCHEREOF
chmod +x "$LAUNCHER"

echo ""
sleep 1
echo "4) Checking status..."
launchctl print "gui/$(id -u)/com.jessica.posturecoach" | grep -E "state|pid" || echo "(agent not showing yet, check the log)"

echo ""
echo "All done! Look for the sitting/standing icon in your menu bar."
echo "It will now start automatically every time you log in, using $PYBIN."
echo "You can delete this installer file now if you like."
read -p "Press enter to close this window..."
