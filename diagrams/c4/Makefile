
PLANTUML_VERSION=1.2022.6

plantuml.jar:
	curl -L https://github.com/plantuml/plantuml/releases/download/v$(PLANTUML_VERSION)/plantuml-$(PLANTUML_VERSION).jar \
		-o $@

dist:
	mkdir -pv $@

dist/%.png: src/%.puml dist plantuml.jar
	java -DPLANTUML_LIMIT_SIZE=8192 -jar plantuml.jar -v -tpng -r -o output $<
	mv -v src/output/$$(basename $@) $@

dist/%.svg: src/%.puml dist plantuml.jar
	java -DPLANTUML_LIMIT_SIZE=8192 -jar plantuml.jar -v -tsvg -r -o output $<
	mv -v src/output/$$(basename $@) $@

dist_all:
	for src_file in $$(find src -iname '*.puml' -not -path 'src/icons/*') ; do \
		file=$$(basename $$src_file) ; \
		name=$$(echo "$$file" | sed 's/\.puml$$//') ; \
		make "dist/$${name}.png" ; \
		make "dist/$${name}.svg" ; \
	done

src/output:
	mkdir -pv $@

src/output/%.png: src/%.puml src/output plantuml.jar
	echo $< | entr java -DPLANTUML_LIMIT_SIZE=8192 -jar plantuml.jar -v -tpng -r -o output $<

src/output/%.svg: src/%.puml src/output plantuml.jar
	echo $< | entr java -DPLANTUML_LIMIT_SIZE=8192 -jar plantuml.jar -v -tsvg -r -o output $<
