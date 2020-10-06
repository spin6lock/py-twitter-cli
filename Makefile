.PHONY : all
all: update d
update:
	proxychains4 python3 main.py
d: #display
	./display.sh
