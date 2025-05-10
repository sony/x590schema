SRC_SCHEMA=x590signatures.json
SRC_SUBSCHEMA=x590schema.json
EX_SRC=example-instance.json
EX_SCH=example-subschema.json
TEST=test/test.json
TOOL=/usr/bin/jsonschema
SUBDIRS= signing
#VERBOSE=-v

all:	test validate signing
	@echo "All tasks completed."

test:	$(SRC_SCHEMA) $(SRC_SUBSCHEMA) $(TEST)
	$(TOOL) test $(TEST) --resolve $(SRC_SCHEMA) --resolve $(SRC_SUBSCHEMA) $(VERBOSE)

validate: $(SRC) $(EX_SRC) $(EX_SCH)
	$(TOOL) validate $(EX_SCH) $(EX_SRC) --resolve $(SRC_SCHEMA)  --resolve $(SRC_SUBSCHEMA) $(VERBOSE)
	
signing: 
	@echo "Descending into signing directory..."
	@cd signing && $(MAKE) all

.PHONY: $(SUBDIRS)