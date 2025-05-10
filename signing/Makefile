# use VERBOSE=-v for verbose output
#VERBOSE=-v
SRC=signing.py

all:  output1.json output2.json output3.json 

output%.json: input%.json $(SRC)
	@echo "Generating $@ from $<"
	@echo "Using the following command:"
	@echo "python3 $(SRC) --input $< --output $@ $(VERBOSE)"
	@python3 $(SRC) --input $< --output $@ $(VERBOSE)
	@echo "Done generating $@"
	
