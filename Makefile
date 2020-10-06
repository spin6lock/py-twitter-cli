update:
	proxychains4 python3 main.py
d: #display
	cat timeline.json|jq -r '["----------------------------------------"], (. | ["@\(.user.screen_name):", .full_text, .url]) | @tsv '|less
all: update d
