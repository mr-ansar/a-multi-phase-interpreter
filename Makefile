BIN=dist


all: $(BIN)/parser $(BIN)/codegen $(BIN)/vm $(BIN)/calc

$(BIN)/parser: parser.py
	pyinstaller --onefile -p . parser.py

clean::
	-@rm -f $(BIN)/parser
	-@rm -rf build/parser

$(BIN)/codegen: codegen.py
	pyinstaller --onefile -p . codegen.py

clean::
	-@rm -f $(BIN)/codegen
	-@rm -rf build/codegen

$(BIN)/vm: vm.py
	pyinstaller --onefile -p . vm.py

clean::
	-@rm -f $(BIN)/vm
	-@rm -rf build/vm

$(BIN)/calc: calc.py
	pyinstaller --onefile -p . calc.py

clean::
	-@rm -f $(BIN)/calc
	-@rm -rf build/calc

clean::
	-@rm -rf *.spec __pycache__
	-@rm -rf lib/__pycache__
