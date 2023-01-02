DEFAULT_FLAT_MAP = {
    'SITE_NAME': '',
    'SITE_DESCRIPTION': '',
    'SOURCE_PATH': 'docs',
    'DIST_PATH': 'site',
    'THEME_LOGO_REL_PATH': 'assets/logo.png',
    'THEME_FAVICON_REL_PATH': 'images/favicon.svg',
    'THEME_FONT': False,
    'EXTRA_GENERATOR_SHOW': False,
    'EXTRA_HOMEPAGE_URL': '../',
    'EXTRA_SOCIAL_ICON_REL_PATH': 'fontawesome/brands/bitbucket',
    'EXTRA_SOCIAL_LINK_URL': '',
    'EXTRA_CSS_STYLESHEET_PATH': 'stylesheets/extra.css',
    'COPYRIGHT_TEXT': 'Copyright &copy; 2022 Organization - All rights reserved.',
    'REPO_NAME': '',
    'REPO_URL': '',
    'EDIT_URI': '',
    'PLUGINS_EXCLUDE_GLOB_LIST': [
        'attic/*',
        'render/*',
        '*.tex',
        '*.pdf',
        '*.json',
    ],
    'NAV_TREE': [
        {'Document': 'document.md'},
    ],
    'MARKDOWN_EXTENSIONS_TOC_PERMALINK_TEXT': '∞',
    'MARKDOWN_EXTENSIONS_PYMDOWNX_X_MERMAID_FORMAT': '!!python/name:pymdownx.superfences.fence_code_format',
}

DEFAULT_EXTRA_CSS = """\
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
