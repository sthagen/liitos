#! /usr/bin/env python
"""Weave the content of the meta file(s) into the output metadata.tex.

in:

---
document:
  common:
    title: Long Title
    abbrv_title: Short Title
    sub_title: null
    type: Engineering Document
    id: 123-444-jaja
    issue: '01'
    revision: '00'
    head_iss_rev: Iss @issue, Rev @revision
    date: 04 NOV 2022
    blurb_header: Or Maybe Footer
    page_count_prefix: Page
    toc: true
    lof: false
    lot: false

out:

cf. MF below
"""
import pathlib

from liitos import log

MF = r"""% Variables from METADATA:
\newcommand{\theMetaTitle}{Short Title}
\newcommand{\theBoxedTitle}{\textbf{\textsf{\mbox{Long}\nolinebreak\ \mbox{Title}}}}
\newcommand{\theBoxedSubTitle}{ }%Document Sub Title
\newcommand{\theMetaType}{Engineering Document}%Document Type
\newcommand{\theMetaDocId}{123-444-jaja}
\newcommand{\theMetaIssCode}{01}
\newcommand{\theMetaRevCode}{00}
\newcommand{\theMetaIssRev}{Iss \theMetaIssCode, Rev \theMetaRevCode}
\newcommand{\theMetaDate}{04 NOV 2022}
\newcommand{\theMetaPropInfo}{Or Maybe Footer}
\newcommand{\theMetaPageNumPrefix}{Page}

\newcommand{\theChangeLogNameIss}{Iss.}
\newcommand{\theChangeLogNameRev}{Rev.}
\newcommand{\theChangeLogNameDate}{Date}
\newcommand{\theChangeLogNameDesc}{Change Description}
"""

APPROVALS_PATH = pathlib.Path('approvals.json')
BOOKMATTER_TEMPLATE_PATH = pathlib.Path('bookmatter.tex.in')
BOOKMATTER_PATH = pathlib.Path('bookmatter.tex')
ENCODING = 'utf-8'
TOKEN = r'\ \mbox{THEROLE} & \mbox{THENAME} & \mbox{} \\[0.5ex]'
ROW_TEMPLATE = r'\ \mbox{role} & \mbox{name} & \mbox{} \\[0.5ex]'
GLUE = '\n\\hline\n'
COLUMNS_EXPECTED = ['Approvals', 'Name']


def weave() -> None:
    """Later alligator."""
    log.info('Would have generated the metadata.tex file from YAML data.')
    with open('metadata.tex', 'wt', encoding=ENCODING) as handle:
        handle.write(MF)
    log.info('Did generate metadata.tex.')
