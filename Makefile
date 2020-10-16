.PHONY : all
all: update
update:
	proxychains4 python3 main.py |less
d: #display
	./display.sh
