SRC_SCHEMA=x590schema.json
EX_SRC=example-instance.json
EX_SCH=example-subschema.json
TEST=test/test.json
TOOL=/usr/bin/jsonschema
SUBDIRS= signing
#VERBOSE=-v

all:	test validate signing
	@echo "All tasks completed."

test:	$(SRC_SCHEMA) $(TEST)
	$(TOOL) test $(TEST)  $(VERBOSE) --resolve $(SRC_SCHEMA) 

validate: $(SRC) $(EX_SRC) $(EX_SCH)
	$(TOOL) validate $(EX_SCH) $(EX_SRC) --resolve $(SRC_SCHEMA) $(VERBOSE)
	
signing: 
	@echo "Descending into signing directory..."
	@cd signing && $(MAKE) all

.PHONY: $(SUBDIRS)
