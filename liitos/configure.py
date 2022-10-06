import yaml

DEFAULT_YAML = """
site_name: $SITE_NAME$
site_description: $SITE_DESCRIPTION$

docs_dir: $DOC_BASE$
site_dir: $TARGET_BASE$

theme:
  name: 'material'
  logo: $ASSETS_SLASH_LOGO_PATH$
  favicon: $IMAGES_SLASH_FAVICON_PATH$
  font:
    text: $PUBLIC_TEXT_FONT$
    code: $PUBLIC_CODE_FONT$
  features:
    - navigation.expand
    - toc.integrate
  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue grey
      accent: indigo
      toggle:
        icon: material/toggle-switch-off-outline
        name: Switch to dark mode

    # Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: indigo
      toggle:
        icon: material/toggle-switch
        name: Switch to light mode

extra:
  generator: false
  homepage: $HOMEPAGE_URL$
  social:
    - icon: $SOCIAL_ICON_PATH$
      link: $SOCIAL_LINK$

extra_css:
  - $STYLESHEETS_SLASH_EXTRA_CSS_PATH$
copyright: $COPYRIGHT_TEXT_WITH_ENTITIES$

repo_name: $REPO_LINK_TEXT$
repo_url: $REPO_LINK$
edit_uri: ""

plugins:
  - search
  - mkdocstrings
  - exclude:
      glob:
        - attic/*
        - render/*
        - "*.tex"
        - "*.pdf"
        - "*.json"
  - enumerate-headings

nav:
  - $LEVEL_WUN_NAV$:
    - $LEVEL_TWO_NAV_1$: $WHERE_1$
    - $LEVEL_TWO_NAV_2$: $WHERE_2$

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - meta
  - md_in_html
  - tables
  - toc:
      permalink: '∞'
  - mkautodoc
  - pymdownx.highlight
  - pymdownx.superfences

extra_javascript:
"""

DEFAULT_EXTRA_CSS = """
@font-face {
    font-family: $LOCAL_FONT$;
    src: url("$LOCAL_FONT_PATH$") format("$LOCAL_FONT_TYPE$");
}

.md-grid {
  max-width: 1440px;
}
th, td { border: .05rem solid; }
th { font-weight: bold; }

[data-md-color-scheme="default"] {
  --md-default-fg-color:        #FFF;
  --md-default-bg-color:        #3D3D3D;
  --md-primary-fg-color:        #26AAE1;
  --md-primary-bg-color:        #000000;
  --md-default-fg-color--light: #FFF;
  --md-primary-fg-color--light: #F0F;
  --md-primary-fg-color--dark:  #00F;
  --md-primary-bg-color--light: #999999;
  --md-primary-bg-color--dark:  #3D3D3D;
  --md-typeset-a-color:         #8C8C8C;
}
"""

DEFAULT_CONFIG = yaml.safe_load(DEFAULT_YAML)
