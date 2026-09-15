ROBOT_VERSION := 1.9.8
ROBOT_JAR := tools/robot.jar
ROBOT_URL := https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar
WIDOCO_VERSION := 1.4.25
WIDOCO_JAR := tools/widoco.jar
WIDOCO_URL := https://github.com/dgarijo/Widoco/releases/download/v$(WIDOCO_VERSION)/widoco-$(WIDOCO_VERSION)-jar-with-dependencies_JDK-17.jar
ONTOLOGY_TTL := ontology/salmon-domain-ontology.ttl
FLAT_TTL := salmon-domain-ontology.ttl
COMPOSE_FLAT_TTL := $(FLAT_TTL)
WIDOCO_INPUT := release/tmp/widoco-input.ttl

.PHONY: help install-robot install-widoco check-robot check-widoco compose-case-study-modules compose-flat-ttl docs-widoco-input verify-ontology-parse verify-year-age-semantic-contract verify-flat-ttl verify-doc-term-anchors verify-doc-version-metadata verify-superclass-declarations verify-superclass-declarations-staged test ci verify-generated-artifacts docs-widoco docs-serializations docs-postprocess docs-refresh snapshot-release release-snapshot release

help:
	@echo "Salmon Domain Ontology build targets"
	@echo "  install-robot    Download ROBOT JAR into tools/"
	@echo "  install-widoco   Download WIDOCO JAR into tools/"
	@echo "  compose-case-study-modules  Recompose split case-study profile modules"
	@echo "  compose-flat-ttl  Build flattened read-only root TTL from source imports"
	@echo "  docs-widoco-input Build the root-ontology-only input used by WIDOCO"
	@echo "  verify-ontology-parse  Parse all ontology Turtle files with rdflib"
	@echo "  verify-year-age-semantic-contract  Verify year, age, abundance, and example semantics"
	@echo "  verify-flat-ttl  Verify committed flat TTL is in sync with source"
	@echo "  verify-doc-term-anchors  Verify WIDOCO HTML exposes stable #/Term anchors"
	@echo "  verify-doc-version-metadata  Verify WIDOCO HTML exposes ontology version metadata"
	@echo "  verify-superclass-declarations  Fail on any undeclared asserted superclass IRI (not yet in 'test'; see B-143)"
	@echo "  verify-superclass-declarations-staged  Same check, reporting the recorded B-143 backlog without failing"
	@echo "  test            Run the fast validation bundle"
	@echo "  ci              Run the full local CI bundle (docs refresh + validation)"
	@echo "  verify-generated-artifacts  Rebuild publication artifacts and fail if git shows drift"
	@echo "  docs-widoco      Regenerate WIDOCO HTML docs into docs/"
	@echo "  docs-serializations Regenerate docs/smn.{ttl,owl,jsonld}"
	@echo "  docs-postprocess Apply project-specific WIDOCO HTML cleanup"
	@echo "  docs-refresh     Run full docs refresh pipeline"
	@echo "  snapshot-release VERSION=X.Y.Z   Write immutable docs/releases/X.Y.Z/ assets from current docs/"
	@echo "  release-snapshot VERSION=X.Y.Z   Refresh docs and write immutable docs/releases/X.Y.Z/ assets"
	@echo "  release VERSION=X.Y.Z [PRIOR_VERSION=A.B.C]  Update release metadata, rebuild, validate, and write the immutable snapshot"

install-robot:
	@echo "Downloading ROBOT..."
	@mkdir -p tools
	@if command -v curl >/dev/null 2>&1; then \
		curl -fL --retry 3 --retry-delay 2 $(ROBOT_URL) -o $(ROBOT_JAR); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -O $(ROBOT_JAR) $(ROBOT_URL); \
	else \
		echo "Neither curl nor wget is available; please install one to fetch ROBOT."; \
		exit 1; \
	fi
	@echo "ROBOT installed at $(ROBOT_JAR)"

install-widoco:
	@echo "Downloading WIDOCO..."
	@mkdir -p tools
	@if command -v curl >/dev/null 2>&1; then \
		curl -fL --retry 3 --retry-delay 2 $(WIDOCO_URL) -o $(WIDOCO_JAR); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -O $(WIDOCO_JAR) $(WIDOCO_URL); \
	else \
		echo "Neither curl nor wget is available; please install one to fetch WIDOCO."; \
		exit 1; \
	fi
	@echo "WIDOCO installed at $(WIDOCO_JAR)"

check-robot:
	@if [ ! -f "$(ROBOT_JAR)" ]; then \
		echo "ROBOT not found at $(ROBOT_JAR). Run 'make install-robot' first."; \
		exit 1; \
	fi
	@if ! command -v java >/dev/null 2>&1; then \
		echo "Java runtime not found. Install Java 17+ to run ROBOT."; \
		exit 1; \
	fi

check-widoco:
	@if [ ! -f "$(WIDOCO_JAR)" ]; then \
		echo "WIDOCO not found at $(WIDOCO_JAR). Run 'make install-widoco' first."; \
		exit 1; \
	fi
	@if ! command -v java >/dev/null 2>&1; then \
		echo "Java runtime not found. Install Java 17+ to run WIDOCO."; \
		exit 1; \
	fi

compose-case-study-modules:
	@echo "Rebuilding split case-study module 09 from fragments..."
	@python3 scripts/build_rda_case_study_modules.py

compose-flat-ttl:
	@echo "Building flattened root TTL: $(COMPOSE_FLAT_TTL)"
	@python3 scripts/build_flat_smn_ttl.py --source $(ONTOLOGY_TTL) --output $(COMPOSE_FLAT_TTL)

docs-widoco-input: compose-flat-ttl
	@echo "Building WIDOCO input: $(WIDOCO_INPUT)"
	@python3 scripts/build_widoco_input.py --input $(COMPOSE_FLAT_TTL) --output $(WIDOCO_INPUT)

verify-ontology-parse:
	@python3 scripts/verify_ontology_parse.py

verify-year-age-semantic-contract:
	@python3 scripts/verify_year_age_semantic_contract.py

verify-case-study-modules:
	@python3 scripts/build_rda_case_study_modules.py --check

verify-mapping-policy:
	@python3 scripts/verify_mapping_policy.py

verify-method-shapes:
	@python3 scripts/verify_method_shapes.py

verify-reasoner: check-robot
	@echo "Running ELK reasoner over the modular build (catalog-resolved imports)..."
	@tmp=$$(mktemp -u).ttl; \
	java -jar $(ROBOT_JAR) merge --catalog ontology/catalog-v001.xml --input $(ONTOLOGY_TTL) \
	  reason --reasoner ELK --output $$tmp && rm -f $$tmp
	@echo "Reasoner gate passed: consistent, no unsatisfiable classes."

verify-flat-ttl:
	@tmp=$$(mktemp); \
	python3 scripts/build_flat_smn_ttl.py --source $(ONTOLOGY_TTL) --output $$tmp; \
	if ! cmp -s $(COMPOSE_FLAT_TTL) $$tmp; then \
		echo "Flat TTL is out of sync. Run 'make compose-flat-ttl' and commit the generated file."; \
		rm -f $$tmp; \
		exit 1; \
	fi; \
	rm -f $$tmp
	@echo "Flat TTL is up-to-date."

verify-doc-term-anchors:
	@python3 scripts/verify_widoco_term_anchors.py

verify-doc-version-metadata:
	@python3 scripts/verify_widoco_version_metadata.py

# The real gate: fails on any superclass IRI asserted in ontology/modules/ that
# neither those modules nor a vendored import declares. It is RED over the
# modules as they stand (9 IRIs, hub item B-143), so it is deliberately NOT a
# prerequisite of `test` yet -- a check that arrives red teaches its first
# reader to weaken it.
#
# SWITCH-ON CONDITION (2026-09-15): when scripts/verify_superclass_declarations.py
# has an empty KNOWN_UNDECLARED, replace `verify-superclass-declarations-staged`
# in the `test` prerequisites below with `verify-superclass-declarations` and
# delete the staged target. The last baseline entry to clear is sosa:Property,
# which is hub item B-107, itself blocked on smn pull request #27. The script's
# staged mode fails on a stale baseline entry, so that swap cannot be forgotten:
# landing B-107 turns CI red until it is done.
verify-superclass-declarations:
	@python3 scripts/verify_superclass_declarations.py

# The staged half, and the one `test` runs today. It is fatal on the
# two-direction fixture, on any undeclared superclass IRI outside the recorded
# B-143 backlog, and on any backlog entry that has since been declared. It is
# silent-but-reporting only on the 9 already known. The fixture is enforced from
# day one on purpose: a staged check whose own demonstration is also staged rots
# before it ever guards anything.
verify-superclass-declarations-staged:
	@python3 scripts/verify_superclass_declarations.py --staged

test: verify-ontology-parse verify-case-study-modules verify-year-age-semantic-contract verify-mapping-policy verify-method-shapes verify-superclass-declarations-staged verify-flat-ttl verify-doc-term-anchors verify-doc-version-metadata
	@echo "Validation bundle completed."

ci: docs-refresh test
	@echo "CI bundle completed."

verify-generated-artifacts: ci
	@if ! git diff --quiet -- docs/ $(COMPOSE_FLAT_TTL); then \
		echo "Generated publication artifacts are out of date."; \
		echo "Run: make ci"; \
		echo "and commit the regenerated docs/ files."; \
		git --no-pager diff -- docs/ $(COMPOSE_FLAT_TTL); \
		exit 1; \
	fi
	@echo "Generated publication artifacts are synchronized."

docs-widoco: compose-case-study-modules docs-widoco-input check-widoco
	@echo "Regenerating WIDOCO docs..."
	@OUT="release/tmp/widoco"; \
	rm -rf "$$OUT"; \
	mkdir -p "$$OUT"; \
	java -jar $(WIDOCO_JAR) \
		-ontFile $(WIDOCO_INPUT) \
		-outFolder "$$OUT" \
		-uniteSections \
		-rewriteAll \
		-noPlaceHolderText; \
	if [ -f "$$OUT/index-en.html" ] && [ ! -f "$$OUT/index.html" ]; then \
		cp "$$OUT/index-en.html" "$$OUT/index.html"; \
	fi; \
	mkdir -p docs; \
	rsync -a --exclude "/ontology.*" "$$OUT/" docs/; \
	rm -f docs/ontology.jsonld docs/ontology.nt docs/ontology.owl docs/ontology.ttl; \
	rm -rf "$$OUT"
	@echo "WIDOCO regenerated into docs/"

docs-serializations: compose-case-study-modules compose-flat-ttl check-robot
	@echo "Regenerating docs/ downloadable serializations..."
	@mkdir -p docs
	@java -jar $(ROBOT_JAR) convert --input $(COMPOSE_FLAT_TTL) --output docs/smn.ttl
	@java -jar $(ROBOT_JAR) convert --input $(COMPOSE_FLAT_TTL) --output docs/smn.owl
	@python3 scripts/convert_ttl_to_jsonld.py $(COMPOSE_FLAT_TTL) docs/smn.jsonld
	@echo "Wrote docs/smn.ttl, docs/smn.owl, docs/smn.jsonld"

docs-postprocess:
	@echo "Applying project-specific WIDOCO post-processing..."
	@python3 scripts/postprocess_widoco_html.py
	@echo "WIDOCO post-processing complete."

docs-refresh: compose-flat-ttl docs-widoco docs-serializations docs-postprocess
	@echo "Docs refresh complete."

snapshot-release:
	@if [ -z "$(VERSION)" ]; then \
		echo "VERSION is required (e.g., make snapshot-release VERSION=0.0.1)"; \
		exit 1; \
	fi
	@DEST="docs/releases/$(VERSION)"; \
	if [ -d "$$DEST" ] && [ "$(FORCE)" != "1" ]; then \
		echo "Snapshot already exists: $$DEST (set FORCE=1 to overwrite)"; \
		exit 1; \
	fi; \
	mkdir -p "$$DEST"; \
	cp docs/smn.ttl "$$DEST/smn.ttl"; \
	cp docs/smn.owl "$$DEST/smn.owl"; \
	cp docs/smn.jsonld "$$DEST/smn.jsonld"; \
	printf '%s\n' \
		'<!DOCTYPE html>' \
		'<html lang="en">' \
		'<head>' \
		'  <meta charset="UTF-8" />' \
		'  <meta name="viewport" content="width=device-width, initial-scale=1" />' \
		'  <link rel="canonical" href="https://w3id.org/smn/$(VERSION)" />' \
		'  <title>Salmon Domain Ontology - Version $(VERSION)</title>' \
		'</head>' \
		'<body>' \
		'  <main>' \
		'    <h1>Salmon Domain Ontology - Version $(VERSION)</h1>' \
		'    <p>This is an immutable release snapshot hosted from GitHub Pages.</p>' \
		'    <h2>Download</h2>' \
		'    <ul>' \
		'      <li><a href="smn.ttl">Turtle (TTL)</a></li>' \
		'      <li><a href="smn.owl">RDF/XML (OWL)</a></li>' \
		'      <li><a href="smn.jsonld">JSON-LD</a></li>' \
		'    </ul>' \
		'    <h2>Links</h2>' \
		'    <ul>' \
		'      <li>Latest documentation: <a href="https://w3id.org/smn">https://w3id.org/smn</a></li>' \
		'      <li>Repository: <a href="https://github.com/salmon-data-mobilization/salmon-domain-ontology">https://github.com/salmon-data-mobilization/salmon-domain-ontology</a></li>' \
		'    </ul>' \
		'  </main>' \
		'</body>' \
		'</html>' \
		> "$$DEST/index.html"
	@echo "Wrote snapshot: docs/releases/$(VERSION)/ (index.html + smn.{ttl,owl,jsonld})"

release-snapshot: docs-refresh snapshot-release

release:
	@if [ -z "$(VERSION)" ]; then \
		echo "VERSION is required (e.g., make release VERSION=0.0.1)"; \
		exit 1; \
	fi
	@args="--version $(VERSION)"; \
	if [ -n "$(PRIOR_VERSION)" ]; then args="$$args --prior-version $(PRIOR_VERSION)"; fi; \
	python3 scripts/update_root_release_metadata.py $$args
	@$(MAKE) ci
	@$(MAKE) snapshot-release VERSION=$(VERSION) FORCE=$(FORCE)
	@echo "Release $(VERSION) prepared."
