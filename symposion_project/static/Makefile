SYMPOSION_LESS = ./symposion/less/site.less
CSS_OUTPUT_FILENAME = symposion.css
LESS_COMPRESSOR ?= `which lessc`

#
# BUILD SITE MEDIA
# lessc & uglifyjs are required
#

build:
	mkdir -p symposion/css
	lessc --yui-compress ${SYMPOSION_LESS} > symposion/css/${CSS_OUTPUT_FILENAME}
