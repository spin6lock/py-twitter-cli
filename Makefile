.PHONY : all
all: update
update:
	proxychains4 python3 main.py
d: #display
	./display.sh
