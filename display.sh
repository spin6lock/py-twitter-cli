#!/bin/sh
cat timeline.json | \
    jq -r '["----------------------------------------"], (. | ["@\(.user.screen_name):\(.full_text) via: https://twitter.com/\(.user.screen_name)/status/\(.id_str)"]) | @tsv ' -C | \
    less -R
