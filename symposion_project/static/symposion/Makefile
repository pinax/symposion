BOOTSTRAP_LESS = ./less/symposion.less
CSS_OUTPUT_FILENAME = symposion.css
LESS_COMPRESSOR ?= `which lessc`

#
# BUILD SITE MEDIA
# lessc & uglifyjs are required
#

build:
	mkdir -p css
	lessc --compress ${BOOTSTRAP_LESS} > css/${CSS_OUTPUT_FILENAME}
