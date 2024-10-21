#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Toggle Yabai & SKHD
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🌅

# Documentation:
# @raycast.author minis
# @raycast.authorURL https://raycast.com/minis

# Sprawdzam czy serwis yabai jest uruchomiony
if pgrep yabai; then
    echo "Zatrzymuję serwis yabai..."
    yabai --stop-service
else
    echo "Uruchamiam serwis yabai..."
    yabai --start-service
fi

# Sprawdzanie czy serwis skhd jest uruchomiony
if pgrep skhd; then
    echo "Zatrzymuję serwis skhd..."
    skhd --stop-service
else
    echo "Uruchamiam serwis skhd..."
    skhd --start-service
fi
