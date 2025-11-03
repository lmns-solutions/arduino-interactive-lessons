default: run


run:
	@bundle exec jekyll serve --livereload

install:
	@bundle install

build:
	@bundle exec jekyll build

clean:
	@bundle exec jekyll clean
	@rm -rf _site
	@rm -rf .jekyll-cache
