default: run


run:
	@bundle exec jekyll serve --livereload

install:
	@bundle install

build:
	@bundle exec jekyll build

clean:
	@rm -rf _site
	@rm -rf .jekyll-cache
