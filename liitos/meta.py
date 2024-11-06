"""Weave the content of the meta file(s) of metadata.tex.in into the output metadata.tex."""

import datetime as dti
import os
import pathlib
from typing import Union, no_type_check

import yaml

import liitos.gather as gat
import liitos.template as tpl
import liitos.tools as too
from liitos import ENCODING, ExternalsType, KNOWN_APPROVALS_STRATEGIES, LOG_SEPARATOR, log

VALUE_SLOT = 'VALUE.SLOT'
DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
MAGIC_OF_TODAY = 'PUBLICATIONDATE'

WEAVE_DEFAULTS = {
    'approvals_adjustable_vertical_space': '2.5em',
    'approvals_strategy': KNOWN_APPROVALS_STRATEGIES[0],
    'bold_font': 'ITCFranklinGothicStd-Demi',
    'bold_italic_font': 'ITCFranklinGothicStd-DemiIt',
    'bookmatter_path': '',
    'change_log_tune_header_sep': '-0em',
    'chosen_logo': '/opt/logo/liitos-logo.png',
    'chosen_title_page_logo': '/opt/logo/liitos-logo.png',
    'code_fontsize': r'\scriptsize',
    'driver_path': '',
    'fixed_font_package': 'sourcecodepro',
    'font_path': '/opt/fonts/',
    'font_suffix': '.otf',
    'footer_frame_note': os.getenv('LIITOS_FOOTER_FRAME_NOTE', ' '),  # TODO
    'footer_outer_field_normal_pages': r'\theMetaPageNumPrefix { } \thepage { }',
    'italic_font': 'ITCFranklinGothicStd-BookIt',
    'lox_indent': r'\hspace*{0.40\textwidth}',  # old default was '' for left align
    'main_font': 'ITCFranklinGothicStd-Book',
    'metadata_path': '',
    'proprietary_information': '/opt/legal/proprietary-information.txt',
    'proprietary_information_adjustable_vertical_space': '-0em',
    'proprietary_information_tune_header_sep': '-0em',
    'publisher_path': '',
    'setup_path': '',
    'stretch': '1.04',  # old default was 1.2
    'table_captions_below': False,
    'toc_all_dots': '',  # old default was not toc all dots, so '%' would restore
}
ACROSS = {
    'eff_font_folder': '',
    'eff_font_suffix': '',
}


@no_type_check
def process_meta(aspects: dict[str, str]) -> Union[gat.Meta, int]:
    """TODO."""
    meta_path = DOC_BASE / aspects[gat.KEY_META]
    if not meta_path.is_file() or not meta_path.stat().st_size:
        log.error(f'destructure failed to find non-empty meta file at {meta_path}')
        return 1
    if meta_path.suffix.lower() not in ('.yaml', '.yml'):
        return 1
    with open(meta_path, 'rt', encoding=ENCODING) as handle:
        metadata = yaml.safe_load(handle)
    if not metadata:
        log.error(f'empty metadata file? Please add metadata to ({meta_path})')
        return 1
    if 'import' in metadata['document']:
        base_meta_path = DOC_BASE / metadata['document']['import']
        if not base_meta_path.is_file() or not base_meta_path.stat().st_size:
            log.error(
                f'metadata declares import of base data from ({base_meta_path.name})'
                f' but failed to find non-empty base file at {base_meta_path}'
            )
            return 1
        with open(base_meta_path, 'rt', encoding=ENCODING) as handle:
            base_data = yaml.safe_load(handle)
        for key, value in metadata['document']['patch'].items():
            base_data['document']['common'][key] = value
        metadata = base_data
    with open('metadata.yml', 'wt', encoding=ENCODING) as handle:
        yaml.dump(metadata, handle, default_flow_style=False)
    return metadata


@no_type_check
def weave_setup_font_path(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the xxxx from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FONT_%_PATH_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('font_path'):
        font_path = mapper.get('font_path')
        if not pathlib.Path(font_path).is_dir():
            log.warning(f'font_path ({font_path}) is no directory on this system - rendering may not work as intended')
        ACROSS['eff_font_folder'] = font_path
        return text.replace(VALUE_SLOT, font_path)
    else:
        log.warning(f'font_path value missing ... setting default ({defaults["font_path"]})')
        ACROSS['eff_font_folder'] = defaults['font_path']
        return text.replace(VALUE_SLOT, defaults['font_path'])


@no_type_check
def weave_setup_font_suffix(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the font_suffix from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FONT_%_SUFFIX_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('font_suffix'):
        font_suffix = mapper.get('font_suffix')
        if font_suffix not in ('.otf', '.ttf'):
            log.warning(f'font_suffix ({font_suffix}) is unexpected - rendering may not work as intended')
        ACROSS['eff_font_suffix'] = font_suffix
        return text.replace(VALUE_SLOT, font_suffix)
    else:
        log.warning(f'font_suffix value missing ... setting default ({defaults["font_suffix"]})')
        ACROSS['eff_font_suffix'] = defaults['font_suffix']
        return text.replace(VALUE_SLOT, defaults['font_suffix'])


@no_type_check
def weave_setup_bold_font(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the bold_font from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_BOLD_%_FONT_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    eff_font_folder = ACROSS['eff_font_folder']
    eff_font_suffix = ACROSS['eff_font_suffix']
    if mapper.get('bold_font'):
        bold_font = mapper.get('bold_font')
        font_path = pathlib.Path(eff_font_folder) / f'{bold_font}{eff_font_suffix}'
        if not font_path.is_file():
            log.warning(
                f'bold_font ({bold_font}) is not found'
                f' as ({font_path}) on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, bold_font)
    else:
        log.warning(f'bold_font value missing ... setting default ({defaults["bold_font"]})')
        return text.replace(VALUE_SLOT, defaults['bold_font'])


@no_type_check
def weave_setup_italic_font(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the italic_font from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ITALIC_%_FONT_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    eff_font_folder = ACROSS['eff_font_folder']
    eff_font_suffix = ACROSS['eff_font_suffix']
    if mapper.get('italic_font'):
        italic_font = mapper.get('italic_font')
        font_path = pathlib.Path(eff_font_folder) / f'{italic_font}{eff_font_suffix}'
        if not font_path.is_file():
            log.warning(
                f'italic_font ({italic_font}) is not found'
                f' as ({font_path}) on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, italic_font)
    else:
        log.warning(f'italic_font value missing ... setting default ({defaults["italic_font"]})')
        return text.replace(VALUE_SLOT, defaults['italic_font'])


@no_type_check
def weave_setup_bold_italic_font(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the bold_italic_font from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_BOLDITALIC_%_FONT_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    eff_font_folder = ACROSS['eff_font_folder']
    eff_font_suffix = ACROSS['eff_font_suffix']
    if mapper.get('bold_italic_font'):
        bold_italic_font = mapper.get('bold_italic_font')
        font_path = pathlib.Path(eff_font_folder) / f'{bold_italic_font}{eff_font_suffix}'
        if not font_path.is_file():
            log.warning(
                f'bold_italic_font ({bold_italic_font}) is not found'
                f' as ({font_path}) on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, bold_italic_font)
    else:
        log.warning(f'bold_italic_font value missing ... setting default ({defaults["bold_italic_font"]})')
        return text.replace(VALUE_SLOT, defaults['bold_italic_font'])


@no_type_check
def weave_setup_main_font(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the main_font from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_MAIN_%_FONT_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    eff_font_folder = ACROSS['eff_font_folder']
    eff_font_suffix = ACROSS['eff_font_suffix']
    if mapper.get('main_font'):
        main_font = mapper.get('main_font')
        font_path = pathlib.Path(eff_font_folder) / f'{main_font}{eff_font_suffix}'
        if not font_path.is_file():
            log.warning(
                f'main_font ({main_font}) is not found'
                f' as ({font_path}) on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, main_font)
    else:
        log.warning(f'main_font value missing ... setting default ({defaults["main_font"]})')
        return text.replace(VALUE_SLOT, defaults['main_font'])


@no_type_check
def weave_setup_fixed_font_package(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the fixed_font_package from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('fixed_font_package'):
        fixed_font_package = mapper.get('fixed_font_package')
        if fixed_font_package != defaults['fixed_font_package']:
            log.warning(
                f'fixed_font_package ({fixed_font_package}) has not'
                ' been tested on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, fixed_font_package)
    else:
        log.warning(f'fixed_font_package value missing ... setting default ({defaults["fixed_font_package"]})')
        return text.replace(VALUE_SLOT, defaults['fixed_font_package'])


@no_type_check
def weave_setup_code_fontsize(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the code_fontsize from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CODE_%_FONTSIZE_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('code_fontsize'):
        code_fontsize = mapper.get('code_fontsize')
        valid_code_font_sizes = (
            r'\Huge',
            r'\huge',
            r'\LARGE',
            r'\Large',
            r'\large',
            r'\normalsize',
            r'\small',
            r'\footnotesize',
            r'\scriptsize',
            r'\tiny',
        )
        bs = '\\'
        sizes = tuple(size[1:] for size in valid_code_font_sizes)
        if code_fontsize.startswith(r'\\'):
            code_fontsize = code_fontsize[1:]
        if code_fontsize not in valid_code_font_sizes:
            log.error(
                f'code_fontsize ({code_fontsize}) is not a valid font size value'
                ' - rendering would not work as intended'
            )
            log.info(f'valid values for code_fontsize must be in {bs}{(", " + bs).join(sizes)}')
            log.warning(
                f'overriding code font size value with the (working) default of ({defaults["code_fontsize"]})'
                f' - in config that would be {defaults["code_fontsize"]}'
            )
            return text.replace(VALUE_SLOT, defaults['code_fontsize'])
        else:
            return text.replace(VALUE_SLOT, code_fontsize)
    else:
        log.info(
            f'code_fontsize value missing ... setting default ({defaults["code_fontsize"]})'
            f' - in config that would be {defaults["code_fontsize"]}'
        )
        return text.replace(VALUE_SLOT, defaults['code_fontsize'])


@no_type_check
def weave_setup_chosen_logo(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the chosen_logo from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHOSEN_%_LOGO_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('chosen_logo'):
        chosen_logo = mapper.get('chosen_logo')
        logo_path = pathlib.Path(chosen_logo)
        if not logo_path.is_file():
            log.warning(
                f'chosen_logo ({chosen_logo}) is not found'
                f' as ({logo_path}) on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, chosen_logo)
    else:
        log.info(f'chosen_logo value missing ... setting default ({defaults["chosen_logo"]})')
        return text.replace(VALUE_SLOT, defaults['chosen_logo'])


@no_type_check
def weave_setup_chosen_title_page_logo(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the chosen_logo from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHOSEN_%_TITLE_%_PAGE_%_LOGO_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    log.warning(text)
    if mapper.get('chosen_title_page_logo'):
        chosen_title_page_logo = mapper.get('chosen_title_page_logo')
        title_page_logo_path = pathlib.Path(chosen_title_page_logo)
        log.warning(f'found {chosen_title_page_logo}')
        if not title_page_logo_path.is_file():
            log.warning(
                f'chosen_title_page_logo ({chosen_title_page_logo}) is not found'
                f' as ({title_page_logo_path}) on this system - rendering may not work as intended'
            )
        return text.replace(VALUE_SLOT, chosen_title_page_logo)
    else:
        log.warning('default logo')
        log.info(f'chosen_title_page_logo value missing ... setting default ({defaults["chosen_title_page_logo"]})')
        return text.replace(VALUE_SLOT, defaults['chosen_title_page_logo'])


@no_type_check
def weave_setup_footer_outer_field_normal_pages(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the footer_outer_field_normal_pages from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_NORMAL_%_PAGES_%_OUTER_%_FOOT_%_CONTENT_%_VALUE_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('footer_outer_field_normal_pages'):
        footer_outer_field_normal_pages = mapper.get('footer_outer_field_normal_pages')
        return text.replace(VALUE_SLOT, footer_outer_field_normal_pages)
    else:
        log.info(
            'footer_outer_field_normal_pages value missing ...'
            f' setting default ({defaults["footer_outer_field_normal_pages"]})'
        )
        return text.replace(VALUE_SLOT, defaults['footer_outer_field_normal_pages'])


@no_type_check
def weave_setup_toc_all_dots(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the toc_all_dots from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_TOC_ALL_DOTS_%%')
    """
    defaults = {**WEAVE_DEFAULTS}
    if mapper.get('toc_all_dots'):
        toc_all_dots = mapper.get('toc_all_dots')
        return text.replace(VALUE_SLOT, toc_all_dots)
    else:
        log.info('toc_all_dots value missing ...' f' setting default ({defaults["toc_all_dots"]})')
        return text.replace(VALUE_SLOT, defaults['toc_all_dots'])


@no_type_check
def dispatch_setup_weaver(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Dispatch the driver weaver by mapping to handled groups per source marker."""
    dispatch = {
        '%%_PATCH_%_FONT_%_PATH_%%': weave_setup_font_path,
        '%%_PATCH_%_FONT_%_SUFFIX_%%': weave_setup_font_suffix,
        '%%_PATCH_%_BOLD_%_FONT_%%': weave_setup_bold_font,
        '%%_PATCH_%_ITALIC_%_FONT_%%': weave_setup_italic_font,
        '%%_PATCH_%_BOLDITALIC_%_FONT_%%': weave_setup_bold_italic_font,
        '%%_PATCH_%_MAIN_%_FONT_%%': weave_setup_main_font,
        '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': weave_setup_fixed_font_package,
        '%%_PATCH_%_CODE_%_FONTSIZE_%%': weave_setup_code_fontsize,
        '%%_PATCH_%_CHOSEN_%_LOGO_%%': weave_setup_chosen_logo,
        '%%_PATCH_%_CHOSEN_%_TITLE_%_PAGE_%_LOGO_%%': weave_setup_chosen_title_page_logo,
        '%%_PATCH_%_NORMAL_%_PAGES_%_OUTER_%_FOOT_%_CONTENT_%_VALUE_%%': weave_setup_footer_outer_field_normal_pages,
        '%%_PATCH_%_TOC_ALL_DOTS_%%': weave_setup_toc_all_dots,
    }
    for trigger, weaver in dispatch.items():
        if text.rstrip().endswith(trigger):
            return weaver(mapper, text)
    return text


@no_type_check
def weave_meta_setup(meta_map: gat.Meta, latex: list[str]) -> list[str]:
    """TODO."""
    log.info('weaving in the meta data per setup.tex.in into setup.tex ...')
    completed = [dispatch_setup_weaver(meta_map['document']['common'], line) for line in latex]
    if completed and completed[-1]:
        completed.append('\n')
    return completed


@no_type_check
def weave_driver_toc_level(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the toc_level from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_TOC_%_LEVEL_%%')
    """
    toc_level = 2
    if mapper.get('toc_level'):
        try:
            toc_level_read = int(mapper['toc_level'])
            toc_level = toc_level_read if 0 < toc_level_read < 5 else 2
            if toc_level != toc_level_read:
                log.warning(
                    f'ignored toc level ({toc_level_read}) set to default (2) - expected value 0 < toc_level < 5'
                )
        except ValueError as err:
            toc_level = 2
            log.warning(f'toc_level ({mapper["toc_level"]}) not in (1, 2, 3, 4) - resorting to default ({toc_level})')
            log.error(f'error detail: {err}')
    else:
        log.info(f'toc_level value missing ... setting default ({toc_level})')
    return text.replace(VALUE_SLOT, str(toc_level))


@no_type_check
def weave_driver_list_of_figures(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the list_of_figures from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_LOF_%%')
    """
    if mapper.get('list_of_figures', None) is not None:
        lof = mapper['list_of_figures']
        if lof in ('', '%'):
            return text.replace(VALUE_SLOT, str(lof))
        else:
            lof = '%'
            log.warning(
                f"list_of_figures ({mapper['list_of_figures']}) not in ('', '%')"
                f' - resorting to default ({lof}) i.e. commenting out the list of figures'
            )
    else:
        log.info('list_of_figures value missing ... setting default (comment out the lof per %)')

    return text.replace(VALUE_SLOT, '%')


@no_type_check
def weave_driver_list_of_tables(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the list_of_tables from mapper or default for driver.

    Trigger is text.rstrip().endswith('%%_PATCH_%_LOT_%%')
    """
    if mapper.get('list_of_tables', None) is not None:
        lof = mapper['list_of_tables']
        if lof in ('', '%'):
            return text.replace(VALUE_SLOT, str(lof))
        else:
            lof = '%'
            log.warning(
                f"list_of_tables ({mapper['list_of_tables']}) not in ('', '%')"
                f' - resorting to default ({lof}) i.e. commenting out the list of tables'
            )
    else:
        log.info('list_of_tables value missing ... setting default (comment out the lot per %)')

    return text.replace(VALUE_SLOT, '%')


@no_type_check
def dispatch_driver_weaver(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Dispatch the driver weaver by mapping to handled groups per source marker."""
    dispatch = {
        '%%_PATCH_%_TOC_%_LEVEL_%%': weave_driver_toc_level,
        '%%_PATCH_%_LOF_%%': weave_driver_list_of_figures,
        '%%_PATCH_%_LOT_%%': weave_driver_list_of_tables,
    }
    for trigger, weaver in dispatch.items():
        if text.rstrip().endswith(trigger):
            return weaver(mapper, text)
    return text


@no_type_check
def weave_meta_driver(meta_map: gat.Meta, latex: list[str]) -> list[str]:
    """TODO."""
    log.info('weaving in the meta data per driver.tex.in into driver.tex ...')
    completed = [dispatch_driver_weaver(meta_map['document']['common'], line) for line in latex]
    if completed and completed[-1]:
        completed.append('\n')
    return completed


@no_type_check
def weave_meta_part_header_title(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_title from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_HEADER_%_TITLE_%%')
    """
    if mapper.get('header_title'):
        return text.replace(VALUE_SLOT, mapper['header_title'])
    else:
        log.info('header_title value missing ... setting default (the title value)')
        return text.replace(VALUE_SLOT, mapper['title'])


@no_type_check
def weave_meta_part_title_slug(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the title slug deriving from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_MAIN_%_TITLE_%_SLUG_%%')
    """
    if mapper.get('bookmark_title'):
        return text.replace(VALUE_SLOT, mapper['bookmark_title'])
    else:
        log.info('bookmark_title value missing ... setting default (the slugged title value)')
        return text.replace(VALUE_SLOT, mapper['title'].replace('\\\\', '').replace('  ', ' ').title())


@no_type_check
def weave_meta_part_title(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the title from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_MAIN_%_TITLE_%%')
    """
    return text.replace(VALUE_SLOT, mapper['title'])


@no_type_check
def weave_meta_part_sub_title(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the sub_title from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_SUB_%_TITLE_%%')
    """
    if mapper.get('sub_title'):
        return text.replace(VALUE_SLOT, mapper['sub_title'])
    else:
        log.info('sub_title value missing ... setting default (single space)')
        return text.replace(VALUE_SLOT, ' ')


@no_type_check
def weave_meta_part_header_type(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_type from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_TYPE_%%')
    """
    if mapper.get('header_type'):
        return text.replace(VALUE_SLOT, mapper['header_type'])
    else:
        log.info('header_type value missing ... setting default (Engineering Document)')
        return text.replace(VALUE_SLOT, 'Engineering Document')


@no_type_check
def weave_meta_part_header_id_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_id_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ID_%_LABEL_%%')
    """
    if mapper.get('header_id_show', None) is not None and not mapper['header_id_show']:
        log.info('header_id_show set to false - hiding id slot in header by setting label to a single space(" ")')
        return text.replace(VALUE_SLOT, ' ')
    log.info('header_id_show not set - considering header_id_label ...')
    if mapper.get('header_id_label'):
        pub_id_label = mapper['header_id_label'].strip()
        if not pub_id_label:
            pub_id_label = ' '  # single space to please the backend parser
        return text.replace(VALUE_SLOT, pub_id_label)
    else:
        log.info('header_id_label value missing ... setting default(Doc. ID:)')
        return text.replace(VALUE_SLOT, 'Doc. ID:')


@no_type_check
def weave_meta_part_header_id(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_id from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ID_%%')
    """
    if mapper.get('header_id_show', None) is not None and not mapper['header_id_show']:
        log.info('header_id_show set to false - hiding id slot in header by setting value to a single space(" ")')
        return text.replace(VALUE_SLOT, ' ')
    log.info('header_id_show not set - considering header_id ...')
    if mapper.get('header_id'):
        return text.replace(VALUE_SLOT, mapper['header_id'])
    else:
        log.info('header_id value missing ... setting default (N/A)')
        return text.replace(VALUE_SLOT, 'N/A')


@no_type_check
def weave_meta_part_issue(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the issue from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ISSUE_%%')
    """
    if mapper.get('issue'):
        return text.replace(VALUE_SLOT, mapper['issue'])
    else:
        log.info('issue value missing ... setting default (01)')
        return text.replace(VALUE_SLOT, '01')


@no_type_check
def weave_meta_part_revision(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the revision from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_REVISION_%%')
    """
    if mapper.get('revision'):
        return text.replace(VALUE_SLOT, mapper['revision'])
    else:
        log.info('revision value missing ... setting default (00)')
        return text.replace(VALUE_SLOT, '00')


@no_type_check
def weave_meta_part_header_date_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_date_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_DATE_%_LABEL_%%')
    """
    if mapper.get('header_date_show', None) is not None and not mapper['header_date_show']:
        log.info('header_date_show set to false - hiding date slot in header by setting label to a single space(" ")')
        return text.replace(VALUE_SLOT, ' ')
    log.info('header_date_show not set - considering header_date_label ...')
    if mapper.get('header_date_label'):
        pub_date_label = mapper['header_date_label'].strip()
        if not pub_date_label:
            pub_date_label = ' '  # single space to please the backend parser
        return text.replace(VALUE_SLOT, pub_date_label)
    else:
        log.info('header_date_label value missing ... setting default(" ")')
        return text.replace(VALUE_SLOT, ' ')


@no_type_check
def weave_meta_part_header_date(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_date from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_DATE_%%')
    """
    if mapper.get('header_date_show', None) is not None and not mapper['header_date_show']:
        log.info('header_date_show set to false - hiding date slot in header by setting value to a single space(" ")')
        return text.replace(VALUE_SLOT, ' ')
    log.info('header_date_show not set - considering header_date ...')
    if mapper.get('header_date_enable_auto', None) is not None and not mapper['header_date_enable_auto']:
        log.info('header_date_enable_auto set to false - setting that slot value as is (no date semantics enforced)')
        if mapper.get('header_date'):
            pub_date_or_any = mapper['header_date'].strip()
            if not pub_date_or_any:
                pub_date_or_any = ' '  # single space to please the backend parser
            return text.replace(VALUE_SLOT, pub_date_or_any)
        else:
            log.info('header_date value missing and as-is mode ... setting to single space ( ) a.k.a. hiding')
            return text.replace(VALUE_SLOT, ' ')
    else:
        today = dti.datetime.today()
        pub_date_today = today.strftime('%d %b %Y').upper()
        if mapper.get('header_date'):
            pub_date = mapper['header_date'].strip()
            if pub_date == MAGIC_OF_TODAY:
                pub_date = pub_date_today
            return text.replace(VALUE_SLOT, pub_date)
        else:
            log.info('header_date value missing ... setting default as empty(" ")')
            return text.replace(VALUE_SLOT, ' ')


@no_type_check
def weave_meta_part_footer_frame_note(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the footer_frame_note from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FRAME_%_NOTE_%%')
    """
    if mapper.get('footer_frame_note'):
        return text.replace(VALUE_SLOT, mapper['footer_frame_note'])
    else:
        log.info('footer_frame_note value missing ... setting default from module / environment ...')
        return text.replace(VALUE_SLOT, WEAVE_DEFAULTS['footer_frame_note'])


@no_type_check
def weave_meta_part_footer_page_number_prefix(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the footer_page_number_prefix from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%')
    """
    if mapper.get('footer_page_number_prefix'):
        return text.replace(VALUE_SLOT, mapper['footer_page_number_prefix'])
    else:
        log.info('footer_page_number_prefix value missing ... setting default (Page)')
        return text.replace(VALUE_SLOT, 'Page')


@no_type_check
def weave_meta_part_change_log_issue_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the change_log_issue_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%')
    """
    if mapper.get('change_log_issue_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_issue_label'])
    else:
        log.info('change_log_issue_label value missing ... setting default (Iss.)')
        return text.replace(VALUE_SLOT, 'Iss.')


@no_type_check
def weave_meta_part_change_log_revision_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the change_log_revision_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%')
    """
    if mapper.get('change_log_revision_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_revision_label'])
    else:
        log.info('change_log_revision_label value missing ... setting default (Rev.)')
        return text.replace(VALUE_SLOT, 'Rev.')


@no_type_check
def weave_meta_part_change_log_date_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the change_log_date_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%')
    """
    if mapper.get('change_log_date_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_date_label'])
    else:
        log.info('change_log_date_label value missing ... setting default (Date)')
        return text.replace(VALUE_SLOT, 'Date')


@no_type_check
def weave_meta_part_change_log_author_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the change_log_author_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%')
    """
    if mapper.get('change_log_author_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_author_label'])
    else:
        log.info('change_log_author_label value missing ... setting default (Author)')
        return text.replace(VALUE_SLOT, 'Author')


@no_type_check
def weave_meta_part_change_log_description_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the change_log_description_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%')
    """
    if mapper.get('change_log_description_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_description_label'])
    else:
        log.info('change_log_description_label value missing ... setting default (Description)')
        return text.replace(VALUE_SLOT, 'Description')


@no_type_check
def weave_meta_part_with_default_slot(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
    slot: str,
) -> str:
    """Do the conditional weaving of slot if text matches else used default (and log a warning)."""
    if mapper.get(slot):
        return text.replace(VALUE_SLOT, mapper[slot])
    else:
        log.info(f'{slot} value missing ... setting default ({WEAVE_DEFAULTS[slot]})')
        return text.replace(VALUE_SLOT, WEAVE_DEFAULTS[slot])


@no_type_check
def weave_meta_part_approvals_adjustable_vertical_space(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the approvals_adjustable_vertical_space from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_ADJUSTABLE_%_VERTICAL_%_SPACE_%%')
    """
    return weave_meta_part_with_default_slot(mapper, text, 'approvals_adjustable_vertical_space')


@no_type_check
def weave_meta_part_proprietary_information_adjustable_vertical_space(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the proprietary_information_adjustable_vertical_space from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_BLURB_%_ADJUSTABLE_%_VERTICAL_%_SPACE_%%')
    """
    return weave_meta_part_with_default_slot(mapper, text, 'proprietary_information_adjustable_vertical_space')


@no_type_check
def weave_meta_part_proprietary_information_tune_header_sep(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the proprietary_information_tune_header_sep from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_BLURB_%_TUNE_%_HEADER_%_SEP_%%')
    """
    return weave_meta_part_with_default_slot(mapper, text, 'proprietary_information_tune_header_sep')


@no_type_check
def weave_meta_part_change_log_tune_header_sep(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the change_log_tune_header_sep from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGE_%_LOG_%_TUNE_%_HEADER_%_SEP_%%')
    """
    return weave_meta_part_with_default_slot(mapper, text, 'change_log_tune_header_sep')


@no_type_check
def weave_meta_part_approvals_department_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the approvals_department_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_DEPARTMENT_%_LABEL_%%')
    """
    if mapper.get('approvals_department_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_department_label'])
    else:
        log.info('approvals_department_label value missing ... setting default (Department)')
        return text.replace(VALUE_SLOT, 'Department')


@no_type_check
def weave_meta_part_approvals_department_value(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the approvals_department_value from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_DEPARTMENT_%_VALUE_%%')
    """
    if mapper.get('approvals_department_value'):
        return text.replace(VALUE_SLOT, mapper['approvals_department_value'])
    else:
        log.info('approvals_department_value value missing ... setting default ( )')
        return text.replace(VALUE_SLOT, ' ')


@no_type_check
def weave_meta_part_approvals_role_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the approvals_role_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%')
    """
    if mapper.get('approvals_role_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_role_label'])
    else:
        log.info('approvals_role_label value missing ... setting default (Approvals)')
        return text.replace(VALUE_SLOT, 'Approvals')


@no_type_check
def weave_meta_part_approvals_name_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the approvals_name_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%')
    """
    if mapper.get('approvals_name_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_name_label'])
    else:
        log.info('approvals_name_label value missing ... setting default (Name)')
        return text.replace(VALUE_SLOT, 'Name')


@no_type_check
def weave_meta_part_approvals_date_and_signature_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the approvals_date_and_signature_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%')
    """
    if mapper.get('approvals_date_and_signature_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_date_and_signature_label'])
    else:
        log.info('approvals_date_and_signature_label value missing ... setting default (Date and Signature)')
        return text.replace(VALUE_SLOT, 'Date and Signature')


@no_type_check
def weave_meta_part_header_issue_revision_combined_label(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_issue_revision_combined_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%_LABEL_%%')
    """
    do_show_key = 'header_issue_revision_combined_show'
    if mapper.get(do_show_key, None) is not None and not mapper[do_show_key]:
        log.info(f'{do_show_key} set to false' ' - hiding date slot in header by setting label to a single space(" ")')
        return text.replace(VALUE_SLOT, ' ')
    log.info(f'{do_show_key} not set - considering header_issue_revision_combined_label ...')
    if mapper.get('header_issue_revision_combined_label'):
        head_iss_rev_comb_label = mapper['header_issue_revision_combined_label'].strip()
        if not head_iss_rev_comb_label:
            head_iss_rev_comb_label = ' '  # single space to please the backend parser
        return text.replace(VALUE_SLOT, head_iss_rev_comb_label)
    else:
        log.info('header_issue_revision_combined_label value missing ... setting default(Issue, Revision:)')
        return text.replace(VALUE_SLOT, 'Issue, Revision:')


@no_type_check
def weave_meta_part_header_issue_revision_combined(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the header_issue_revision_combined from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%')
    """
    do_show_key = 'header_issue_revision_combined_show'
    if mapper.get(do_show_key, None) is not None and not mapper[do_show_key]:
        log.info(f'{do_show_key} set to false' ' - hiding date slot in header by setting value to a single space(" ")')
        return text.replace(VALUE_SLOT, ' ')
    log.info(f'{do_show_key} not set - considering header_issue_revision_combined ...')
    if mapper.get('header_issue_revision_combined'):
        return text.replace(VALUE_SLOT, mapper['header_issue_revision_combined'])
    else:
        log.info(
            'header_issue_revision_combined value missing ... setting'
            ' default (Iss \\theMetaIssCode, Rev \\theMetaRevCode)'
        )
        return text.replace(VALUE_SLOT, r'Iss \theMetaIssCode, Rev \theMetaRevCode')


@no_type_check
def weave_meta_part_proprietary_information(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the proprietary_information from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%')
    """
    if mapper.get('proprietary_information'):
        prop_info = mapper['proprietary_information']
        if pathlib.Path(prop_info).is_file():
            try:
                prop_info_from_file = pathlib.Path(prop_info).open().read()
                prop_info = prop_info_from_file
            except (OSError, UnicodeDecodeError) as err:
                log.error(f'interpretation of proprietary_information value ({prop_info}) failed with error: {err}')
                log.warning(f'using value ({prop_info}) directly for proprietary_information')
        else:
            log.info(f'using value ({prop_info}) directly for proprietary_information (no file)')
        return text.replace(VALUE_SLOT, prop_info)
    else:
        log.warning('proprietary_information value missing ... setting default from module ...')
        prop_info = WEAVE_DEFAULTS['proprietary_information']
        if pathlib.Path(prop_info).is_file():
            try:
                prop_info_from_file = pathlib.Path(prop_info).open().read()
                prop_info = prop_info_from_file
            except (OSError, UnicodeDecodeError) as err:
                log.error(f'interpretation of proprietary_information value ({prop_info}) failed with error: {err}')
                log.warning(f'using value ({prop_info}) directly for proprietary_information')
        else:
            log.info(f'using value ({prop_info}) directly for proprietary_information (no file)')
        return text.replace(VALUE_SLOT, prop_info)


@no_type_check
def weave_meta_part_stretch(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the stretch from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_STRETCH_%%')
    """
    return weave_meta_part_with_default_slot(mapper, text, 'stretch')


@no_type_check
def weave_meta_part_lox_indent(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Weave in the lox_indent from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_LOX_INDENT_%%')
    """
    return weave_meta_part_with_default_slot(mapper, text, 'lox_indent')


@no_type_check
def dispatch_meta_weaver(
    mapper: dict[str, Union[str, int, bool, None]],
    text: str,
) -> str:
    """Dispatch the meta weaver by mapping to handled groups per source marker."""
    dispatch = {
        '%%_PATCH_%_HEADER_%_TITLE_%%': weave_meta_part_header_title,
        '%%_PATCH_%_TITLE_%_SLUG_%%': weave_meta_part_title_slug,
        '%%_PATCH_%_MAIN_%_TITLE_%%': weave_meta_part_title,
        '%%_PATCH_%_SUB_%_TITLE_%%': weave_meta_part_sub_title,
        '%%_PATCH_%_TYPE_%%': weave_meta_part_header_type,
        '%%_PATCH_%_ID_%_LABEL_%%': weave_meta_part_header_id_label,
        '%%_PATCH_%_ID_%%': weave_meta_part_header_id,
        '%%_PATCH_%_ISSUE_%%': weave_meta_part_issue,
        '%%_PATCH_%_REVISION_%%': weave_meta_part_revision,
        '%%_PATCH_%_DATE_%_LABEL_%%': weave_meta_part_header_date_label,
        '%%_PATCH_%_DATE_%%': weave_meta_part_header_date,
        '%%_PATCH_%_FRAME_%_NOTE_%%': weave_meta_part_footer_frame_note,
        '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': weave_meta_part_footer_page_number_prefix,
        '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': weave_meta_part_change_log_issue_label,
        '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': weave_meta_part_change_log_revision_label,
        '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': weave_meta_part_change_log_date_label,
        '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': weave_meta_part_change_log_author_label,
        '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': weave_meta_part_change_log_description_label,
        '%%_PATCH_%_APPROVALS_%_ADJUSTABLE_%_VERTICAL_%_SPACE_%%': weave_meta_part_approvals_adjustable_vertical_space,
        '%%_PATCH_%_BLURB_%_ADJUSTABLE_%_VERTICAL_%_SPACE_%%': weave_meta_part_proprietary_information_adjustable_vertical_space,  # noqa
        '%%_PATCH_%_BLURB_%_TUNE_%_HEADER_%_SEP_%%': weave_meta_part_proprietary_information_tune_header_sep,
        '%%_PATCH_%_CHANGE_%_LOG_%_TUNE_%_HEADER_%_SEP_%%': weave_meta_part_change_log_tune_header_sep,
        '%%_PATCH_%_APPROVALS_%_DEPARTMENT_%_LABEL_%%': weave_meta_part_approvals_department_label,
        '%%_PATCH_%_APPROVALS_%_DEPARTMENT_%_VALUE_%%': weave_meta_part_approvals_department_value,
        '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': weave_meta_part_approvals_role_label,
        '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': weave_meta_part_approvals_name_label,
        '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': weave_meta_part_approvals_date_and_signature_label,
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%_LABEL_%%': weave_meta_part_header_issue_revision_combined_label,
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': weave_meta_part_header_issue_revision_combined,
        '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': weave_meta_part_proprietary_information,
        '%%_PATCH_%_STRETCH_%%': weave_meta_part_stretch,
        '%%_PATCH_%_LOX_INDENT_%%': weave_meta_part_lox_indent,
    }
    for trigger, weaver in dispatch.items():
        if text.rstrip().endswith(trigger):
            return weaver(mapper, text)
    return text


@no_type_check
def weave_meta_meta(meta_map: gat.Meta, latex: list[str]) -> list[str]:
    """TODO."""
    log.info('weaving in the meta data per metadata.tex.in into metadata.tex ...')
    completed = [dispatch_meta_weaver(meta_map['document']['common'], line) for line in latex]
    if completed and completed[-1]:
        completed.append('\n')
    return completed


@no_type_check
def weave(
    doc_root: Union[str, pathlib.Path],
    structure_name: str,
    target_key: str,
    facet_key: str,
    options: dict[str, bool],
    externals: ExternalsType,
) -> int:
    """Later alligator."""
    log.info(LOG_SEPARATOR)
    log.info('entered meta weave function ...')
    target_code = target_key
    facet_code = facet_key
    if not facet_code.strip() or not target_code.strip():
        log.error(f'meta requires non-empty target ({target_code}) and facet ({facet_code}) codes')
        return 2

    log.info(f'parsed target ({target_code}) and facet ({facet_code}) from request')

    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='meta'
    )
    log.info(f'prelude teleported processor into the document root at ({os.getcwd()}/)')
    rel_concat_folder_path = pathlib.Path('render/pdf/')
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)
    os.chdir(rel_concat_folder_path)
    log.info(f'meta (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    ok, aspect_map = too.load_target(target_code, facet_code)
    if not ok or not aspect_map:
        return 0 if ok else 1

    metadata = process_meta(aspect_map)
    if isinstance(metadata, int):
        return 1

    meta_doc_common = metadata['document']['common']  # noqa
    log.debug(f'in meta.weave {meta_doc_common=}')
    log.debug(f'in meta.weave {externals=}')
    if externals['bookmatter']['is_custom']:
        log.info(
            'per environment variable value request to load external bookmatter layout template'
            f' from {externals["bookmatter"]["id"]} for title page incl. approvals'
        )
    log.debug(f'in meta.weave bookmatter_path is "{meta_doc_common.get("bookmatter_path", "NOT-PRESENT")}"')
    if 'bookmatter_path' in meta_doc_common:
        bookmatter_path_str = meta_doc_common['bookmatter_path']
        if bookmatter_path_str and isinstance(bookmatter_path_str, str):
            externals['bookmatter'] = {'id': bookmatter_path_str.strip(), 'is_custom': True}
            log.info(
                f'per configuration variable value request to load external bookmatter layout template'
                f' from {externals["bookmatter"]["id"]} title page incl. approvals'
            )

    if externals['driver']['is_custom']:
        log.info(
            'per environment variable value request to load external driver layout template'
            f' from {externals["driver"]["id"]} for general document structure'
        )
    log.debug(f'in meta.weave driver_path is "{meta_doc_common.get("driver_path", "NOT-PRESENT")}"')
    if 'driver_path' in meta_doc_common:
        driver_path_str = meta_doc_common['driver_path']
        if driver_path_str and isinstance(driver_path_str, str):
            externals['driver'] = {'id': driver_path_str.strip(), 'is_custom': True}
            log.info(
                f'per configuration variable value request to load external driver layout template'
                f' from {externals["driver"]["id"]} for general document structure'
            )

    if externals['metadata']['is_custom']:
        log.info(
            'per environment variable value request to load external metadata template'
            f' from {externals["metadata"]["id"]} for mapping values to required keys'
        )
    log.debug(f'in meta.weave metadata_path is "{meta_doc_common.get("metadata_path", "NOT-PRESENT")}"')
    if 'metadata_path' in meta_doc_common:
        metadata_path_str = meta_doc_common['metadata_path']
        if metadata_path_str and isinstance(metadata_path_str, str):
            externals['metadata'] = {'id': metadata_path_str.strip(), 'is_custom': True}
            log.info(
                f'per configuration variable value request to load external metadata template'
                f' from {externals["metadata"]["id"]} for mapping values to required keys'
            )

    if externals['publisher']['is_custom']:
        log.info(
            'per environment variable value request to load external publisher layout template'
            f' from {externals["publisher"]["id"]} for changes and notices'
        )
    log.debug(f'in meta.weave publisher_path is "{meta_doc_common.get("publisher_path", "NOT-PRESENT")}"')
    if 'publisher_path' in meta_doc_common:
        publisher_path_str = meta_doc_common['publisher_path']
        if publisher_path_str and isinstance(publisher_path_str, str):
            externals['publisher'] = {'id': publisher_path_str.strip(), 'is_custom': True}
            log.info(
                f'per configuration variable value request to load external publisher layout template'
                f' from {externals["publisher"]["id"]} for changes and notices'
            )

    if externals['setup']['is_custom']:
        log.info(
            'per environment variable value request to load external setup layout template'
            f' from {externals["setup"]["id"]} for general document setup'
        )
    log.debug(f'in meta.weave setup_path is "{meta_doc_common.get("setup_path", "NOT-PRESENT")}"')
    if 'setup_path' in meta_doc_common:
        setup_path_str = meta_doc_common['setup_path']
        if setup_path_str and isinstance(setup_path_str, str):
            externals['setup'] = {'id': setup_path_str.strip(), 'is_custom': True}
            log.info(
                f'per configuration variable value request to load external setup layout template'
                f' from {externals["setup"]["id"]} for general document setup'
            )

    if 'approvals_strategy' in meta_doc_common:
        approvals_strategy_str = meta_doc_common['approvals_strategy']
        if approvals_strategy_str and approvals_strategy_str in KNOWN_APPROVALS_STRATEGIES:
            memo = options.get('approvals_strategy', 'unset')
            options['approvals_strategy'] = approvals_strategy_str
            log.info(
                f'per configuration variable value request for approvals strategy ({approvals_strategy_str})'
                f' was set before to ({memo}) from default or command line'
            )

    if 'table_caption_below' in meta_doc_common:
        table_caption_below = bool(meta_doc_common['table_caption_below'])
        if table_caption_below:
            memo = options.get('table_caption_below', False)
            options['table_caption_below'] = table_caption_below
            tc_strategy = 'below' if table_caption_below else 'above'
            log.info(
                f'per configuration variable value request for table captions ({tc_strategy})'
                f' was set before to ({memo}) from default or command line'
            )

    metadata_template_is_custom = externals['metadata']['is_custom']
    metadata_template = str(externals['metadata']['id'])
    metadata_path = pathlib.Path('metadata.tex')

    metadata_template = tpl.load_resource(metadata_template, metadata_template_is_custom)
    lines = [line.rstrip() for line in metadata_template.split('\n')]
    lines = weave_meta_meta(metadata, lines)
    with open(metadata_path, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    driver_template_is_custom = externals['driver']['is_custom']
    driver_template = str(externals['driver']['id'])
    driver_path = pathlib.Path('driver.tex')

    driver_template = tpl.load_resource(driver_template, driver_template_is_custom)
    lines = [line.rstrip() for line in driver_template.split('\n')]
    lines = weave_meta_driver(metadata, lines)
    with open(driver_path, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    setup_template_is_custom = externals['setup']['is_custom']
    setup_template = str(externals['setup']['id'])
    setup_path = pathlib.Path('setup.tex')

    setup_template = tpl.load_resource(setup_template, setup_template_is_custom)
    lines = [line.rstrip() for line in setup_template.split('\n')]
    lines = weave_meta_setup(metadata, lines)
    with open(setup_path, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    return 0
