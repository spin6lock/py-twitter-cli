#!/bin/sh

cat timeline.json | \
    sed 's/\\[tn]/ /g'| \
    jq -r '"-----------------------\n\u001b[33m@\(.user.screen_name):\u001b[0m\t\(.text) via: \u001b[34mhttps://twitter.com/\(.user.screen_name)/status/\(.id_str)\u001b[0m"' -C | \
    less -R
