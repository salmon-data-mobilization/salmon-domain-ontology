ROBOT_VERSION := 1.9.8
ROBOT_JAR := tools/robot.jar
ROBOT_URL := https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar
WIDOCO_VERSION := 1.4.25
WIDOCO_JAR := tools/widoco.jar
WIDOCO_URL := https://github.com/dgarijo/Widoco/releases/download/v$(WIDOCO_VERSION)/widoco-$(WIDOCO_VERSION)-jar-with-dependencies_JDK-17.jar
ONTOLOGY_TTL := ontology/salmon-domain-ontology.ttl

.PHONY: help install-robot install-widoco check-robot check-widoco docs-widoco docs-serializations docs-postprocess docs-refresh release-snapshot

help:
	@echo "🧭 Salmon Domain Ontology build targets"
	@echo "  install-robot    Download ROBOT JAR into tools/"
	@echo "  install-widoco   Download WIDOCO JAR into tools/"
	@echo "  docs-widoco      Regenerate WIDOCO HTML docs into docs/"
	@echo "  docs-serializations Regenerate docs/smn.{ttl,owl,jsonld}"
	@echo "  docs-postprocess Apply project-specific WIDOCO HTML cleanup"
	@echo "  docs-refresh     Run full docs refresh pipeline"
	@echo "  release-snapshot VERSION=X.Y.Z   Write immutable docs/releases/X.Y.Z/ assets"

install-robot:
	@echo "📥 Downloading ROBOT..."
	@mkdir -p tools
	@if command -v curl >/dev/null 2>&1; then \
		curl -fL --retry 3 --retry-delay 2 $(ROBOT_URL) -o $(ROBOT_JAR); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -O $(ROBOT_JAR) $(ROBOT_URL); \
	else \
		echo "Neither curl nor wget is available; please install one to fetch ROBOT."; \
		exit 1; \
	fi
	@echo "✅ ROBOT installed at $(ROBOT_JAR)"

install-widoco:
	@echo "📥 Downloading WIDOCO..."
	@mkdir -p tools
	@if command -v curl >/dev/null 2>&1; then \
		curl -fL --retry 3 --retry-delay 2 $(WIDOCO_URL) -o $(WIDOCO_JAR); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -O $(WIDOCO_JAR) $(WIDOCO_URL); \
	else \
		echo "Neither curl nor wget is available; please install one to fetch WIDOCO."; \
		exit 1; \
	fi
	@echo "✅ WIDOCO installed at $(WIDOCO_JAR)"

check-robot:
	@if [ ! -f "$(ROBOT_JAR)" ]; then \
		echo "❌ ROBOT not found at $(ROBOT_JAR). Run 'make install-robot' first."; \
		exit 1; \
	fi
	@if ! command -v java >/dev/null 2>&1; then \
		echo "❌ Java runtime not found. Install Java 17+ to run ROBOT."; \
		exit 1; \
	fi

check-widoco:
	@if [ ! -f "$(WIDOCO_JAR)" ]; then \
		echo "❌ WIDOCO not found at $(WIDOCO_JAR). Run 'make install-widoco' first."; \
		exit 1; \
	fi
	@if ! command -v java >/dev/null 2>&1; then \
		echo "❌ Java runtime not found. Install Java 17+ to run WIDOCO."; \
		exit 1; \
	fi

docs-widoco: check-widoco
	@echo "🧙 Regenerating WIDOCO docs..."
	@OUT="release/tmp/widoco"; \
	rm -rf "$$OUT"; \
	mkdir -p "$$OUT"; \
	java -jar $(WIDOCO_JAR) \
		-ontFile $(ONTOLOGY_TTL) \
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
	rm -rf "$$OUT"; \
	echo "✅ WIDOCO regenerated into docs/"

docs-serializations: check-robot
	@echo "🔄 Regenerating docs/ downloadable serializations..."
	@mkdir -p docs
	@java -jar $(ROBOT_JAR) convert --input $(ONTOLOGY_TTL) --output docs/smn.ttl
	@java -jar $(ROBOT_JAR) convert --input $(ONTOLOGY_TTL) --output docs/smn.owl
	@python3 scripts/convert_ttl_to_jsonld.py $(ONTOLOGY_TTL) docs/smn.jsonld
	@echo "✅ Wrote docs/smn.ttl, docs/smn.owl, docs/smn.jsonld"

docs-postprocess:
	@echo "🧩 Applying project-specific WIDOCO post-processing..."
	@python3 scripts/postprocess_widoco_html.py
	@echo "✅ WIDOCO post-processing complete."

docs-refresh: docs-widoco docs-serializations docs-postprocess
	@echo "✅ Docs refresh complete."

release-snapshot: docs-refresh
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ VERSION is required (e.g., make release-snapshot VERSION=0.0.0)"; \
		exit 1; \
	fi
	@DEST="docs/releases/$(VERSION)"; \
	if [ -d "$$DEST" ] && [ "$(FORCE)" != "1" ]; then \
		echo "❌ Snapshot already exists: $$DEST (set FORCE=1 to overwrite)"; \
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
		'  <title>Salmon Domain Ontology — Version $(VERSION)</title>' \
		'</head>' \
		'<body>' \
		'  <main>' \
		'    <h1>Salmon Domain Ontology — Version $(VERSION)</h1>' \
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
	@echo "✅ Wrote snapshot: docs/releases/$(VERSION)/ (index.html + smn.{ttl,owl,jsonld})"
