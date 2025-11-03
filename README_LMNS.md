# README LMNS


## Local setup

* [Install ruby macos](https://jekyllrb.com/docs/installation/macos/)


## Local run

* It is important due to Ruby SSL issue to set - export RUBYOPT="-r$HOME/.ruby-no-crl"
* The content of the `.ruby-no-crl` file is in ./misc/ruby-no-crl

* Makefile
  * make clean - cleans the build
  * make build - builds the website
  * make run - runs it locally

## Scripts

### Setup

* `python3 -m venv .venv`
* `touch .envrc`
* `echo source .venv/bin/activate >> .envrc`
* `direnv allow`
* `which python3` - inspect whether virtualenv loaded properly
* `pip3 install -r requirements.txt`

### Purpose and usage

#### Jekyll utilities

* `add_frontmatter.py` - adds unique page_id for each page so the jekyll polygloth plugin can detect language change
* `link-rewrite.py` - not used, but the idea is to replace plain markdown links with Liquid to fix relative/absolute links issues with routing within the page (needed in case you introduce permalinks with add_frontmatter.py)

#### Translations

* (deprecated) `translate.py` - translates html pages using Google Translate API
* (deprecated) `translate-v2.py` - translates html pages using Google Translate API
* (deprecated) `translate-html.py` - translates html pages using Google Translate API
* (latest) `translate-v3.py` - translates html pages using Google Translate API

## Processing from original fork

1. After the repo was forked the `_config.yml` was changed:
    * Change baseurl and other configuration related to deployment with Github Pages
    * `polygloth` plugin was added to support `en` and `bg` versions of the website
2. Added Github Actions in `.github` directory to deploy the website
3. Introduce `_includes/header_custom.html` partial so we can show users simple language switcher
4. `add_frontmatter.py` was ran over the pages to produce unique page_id for each page
5. `_includes/nav_footer_custom.html` and `_includes/footer_custom.html` were changed with LMNS logo


## Deployment

* Via Github Actions and Github Pages

