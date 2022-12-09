"""Weave the content of the meta file(s) of metadata.tex.in into the output metadata.tex."""
import datetime as dti
import os
import pathlib
from typing import no_type_check

import yaml

import liitos.gather as gat
import liitos.template_loader as template
from liitos import ENCODING, log

METADATA_TEMPLATE = os.getenv('LIITOS_METADATA_TEMPLATE', '')
METADATA_TEMPLATE_IS_EXTERNAL = bool(METADATA_TEMPLATE)
if not METADATA_TEMPLATE:
    METADATA_TEMPLATE = 'templates/metadata.tex.in'

METADATA_PATH = pathlib.Path('metadata.tex')

SETUP_TEMPLATE = os.getenv('LIITOS_SETUP_TEMPLATE', '')
SETUP_TEMPLATE_IS_EXTERNAL = bool(SETUP_TEMPLATE)
if not SETUP_TEMPLATE:
    SETUP_TEMPLATE = 'templates/setup.tex.in'

SETUP_PATH = pathlib.Path('setup.tex')

DRIVER_TEMPLATE = os.getenv('LIITOS_DRIVER_TEMPLATE', '')
DRIVER_TEMPLATE_IS_EXTERNAL = bool(DRIVER_TEMPLATE)
if not DRIVER_TEMPLATE:
    DRIVER_TEMPLATE = 'templates/driver.tex.in'

DRIVER_PATH = pathlib.Path('driver.tex')

VALUE_SLOT = 'VALUE.SLOT'
DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
MAGIC_OF_TODAY = 'PUBLICATIONDATE'

WEAVE_DEFAULTS = {
    'font_path': '/opt/fonts/',
    'font_suffix': '.otf',
    'bold_font': 'ITCFranklinGothicStd-Demi',
    'italic_font': 'ITCFranklinGothicStd-BookIt',
    'bold_italic_font': 'ITCFranklinGothicStd-DemiIt',
    'main_font': 'ITCFranklinGothicStd-Book',
    'fixed_font_package': 'sourcecodepro',
    'code_fontsize': r'\scriptsize',
    'chosen_logo': '/opt/logo/liitos-logo.png',
}
ACROSS = {
    'eff_font_folder': '',
    'eff_font_suffix': '',
}


@no_type_check
def process_meta(aspects: str) -> gat.Meta | int:
    """TODO."""
    meta_path = DOC_BASE / aspects[gat.KEY_META]
    if not meta_path.is_file() or not meta_path.stat().st_size:
        log.error(f'destructure failed to find non-empty meta file at {meta_path}')
        return 1
    if meta_path.suffix.lower() not in ('.yaml', '.yml'):
        log.error(f'meta file format per suffix ({meta_path.suffix}) not supported')
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
        log.warning(
            f'code_fontsize value missing ... setting default ({defaults["code_fontsize"]})'
            f' - in config that would be {defaults["code_fontsize"]}'
        )
        return text.replace(VALUE_SLOT, defaults['code_fontsize'])


@no_type_check
def weave_setup_chosen_logo(
    mapper: dict[str, str | int | bool | None],
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
        log.warning(f'chosen_logo value missing ... setting default ({defaults["chosen_logo"]})')
        return text.replace(VALUE_SLOT, defaults['chosen_logo'])


@no_type_check
def dispatch_setup_weaver(
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
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
        log.warning(f'toc_level value missing ... setting default ({toc_level})')
    return text.replace(VALUE_SLOT, str(toc_level))


@no_type_check
def weave_driver_list_of_figures(
    mapper: dict[str, str | int | bool | None],
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
                f" - resorting to default ({lof}) i.e. commenting out the list of figures"
            )
    else:
        log.warning('list_of_figures value missing ... setting default (comment out the lof per %)')

    return text.replace(VALUE_SLOT, '%')


@no_type_check
def weave_driver_list_of_tables(
    mapper: dict[str, str | int | bool | None],
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
                f" - resorting to default ({lof}) i.e. commenting out the list of tables"
            )
    else:
        log.warning('list_of_tables value missing ... setting default (comment out the lot per %)')

    return text.replace(VALUE_SLOT, '%')


@no_type_check
def dispatch_driver_weaver(
    mapper: dict[str, str | int | bool | None],
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
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the header_title from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_HEADER_%_TITLE_%%')
    """
    if mapper.get('header_title'):
        return text.replace(VALUE_SLOT, mapper['header_title'])
    else:
        log.warning('header_title value missing ... setting default (the title value)')
        return text.replace(VALUE_SLOT, mapper['title'])


@no_type_check
def weave_meta_part_title(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the title from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_MAIN_%_TITLE_%%')
    """
    return text.replace(VALUE_SLOT, mapper['title'])


@no_type_check
def weave_meta_part_sub_title(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the sub_title from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_SUB_%_TITLE_%%')
    """
    if mapper.get('sub_title'):
        return text.replace(VALUE_SLOT, mapper['sub_title'])
    else:
        log.warning('sub_title value missing ... setting default (single space)')
        return text.replace(VALUE_SLOT, ' ')


@no_type_check
def weave_meta_part_header_type(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the header_type from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_TYPE_%%')
    """
    if mapper.get('header_type'):
        return text.replace(VALUE_SLOT, mapper['header_type'])
    else:
        log.warning('header_type value missing ... setting default (Engineering Document)')
        return text.replace(VALUE_SLOT, 'Engineering Document')


@no_type_check
def weave_meta_part_header_id(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the header_id from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ID_%%')
    """
    if mapper.get('header_id'):
        return text.replace(VALUE_SLOT, mapper['header_id'])
    else:
        log.warning('header_id value missing ... setting default (P99999)')
        return text.replace(VALUE_SLOT, 'P99999')


@no_type_check
def weave_meta_part_issue(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the issue from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ISSUE_%%')
    """
    if mapper.get('issue'):
        return text.replace(VALUE_SLOT, mapper['issue'])
    else:
        log.warning('issue value missing ... setting default (01)')
        return text.replace(VALUE_SLOT, '01')


@no_type_check
def weave_meta_part_revision(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the revision from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_REVISION_%%')
    """
    if mapper.get('revision'):
        return text.replace(VALUE_SLOT, mapper['revision'])
    else:
        log.warning('revision value missing ... setting default (00)')
        return text.replace(VALUE_SLOT, '00')


@no_type_check
def weave_meta_part_header_date(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the header_date from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_DATE_%%')
    """
    today = dti.datetime.today()
    pub_date_today = today.strftime('%d %b %Y').upper()
    if mapper.get('header_date'):
        pub_date = mapper['header_date'].strip()
        if pub_date == MAGIC_OF_TODAY:
            pub_date = pub_date_today
        return text.replace(VALUE_SLOT, pub_date)
    else:
        log.warning(f'header_date value missing ... setting default as today({pub_date_today})')
        return text.replace(VALUE_SLOT, pub_date_today)


@no_type_check
def weave_meta_part_footer_frame_note(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the footer_frame_note from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FRAME_%_NOTE_%%')
    """
    if mapper.get('footer_frame_note'):
        return text.replace(VALUE_SLOT, mapper['footer_frame_note'])
    else:
        log.warning('footer_frame_note value missing ... setting default (VERY CONSEQUENTIAL)')
        return text.replace(VALUE_SLOT, 'VERY CONSEQUENTIAL')


@no_type_check
def weave_meta_part_footer_page_number_prefix(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the footer_page_number_prefix from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%')
    """
    if mapper.get('footer_page_number_prefix'):
        return text.replace(VALUE_SLOT, mapper['footer_page_number_prefix'])
    else:
        log.warning('footer_page_number_prefix value missing ... setting default (Page)')
        return text.replace(VALUE_SLOT, 'Page')


@no_type_check
def weave_meta_part_change_log_issue_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the change_log_issue_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%')
    """
    if mapper.get('change_log_issue_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_issue_label'])
    else:
        log.warning('change_log_issue_label value missing ... setting default (Iss.)')
        return text.replace(VALUE_SLOT, 'Iss.')


@no_type_check
def weave_meta_part_change_log_revision_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the change_log_revision_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%')
    """
    if mapper.get('change_log_revision_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_revision_label'])
    else:
        log.warning('change_log_revision_label value missing ... setting default (Rev.)')
        return text.replace(VALUE_SLOT, 'Rev.')


@no_type_check
def weave_meta_part_change_log_date_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the change_log_date_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%')
    """
    if mapper.get('change_log_date_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_date_label'])
    else:
        log.warning('change_log_date_label value missing ... setting default (Date)')
        return text.replace(VALUE_SLOT, 'Date')


@no_type_check
def weave_meta_part_change_log_author_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the change_log_author_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%')
    """
    if mapper.get('change_log_author_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_author_label'])
    else:
        log.warning('change_log_author_label value missing ... setting default (Author)')
        return text.replace(VALUE_SLOT, 'Author')


@no_type_check
def weave_meta_part_change_log_description_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the change_log_description_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%')
    """
    if mapper.get('change_log_description_label'):
        return text.replace(VALUE_SLOT, mapper['change_log_description_label'])
    else:
        log.warning('change_log_description_label value missing ... setting default (Description)')
        return text.replace(VALUE_SLOT, 'Description')


@no_type_check
def weave_meta_part_approvals_role_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the approvals_role_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%')
    """
    if mapper.get('approvals_role_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_role_label'])
    else:
        log.warning('approvals_role_label value missing ... setting default (Approvals)')
        return text.replace(VALUE_SLOT, 'Approvals')


@no_type_check
def weave_meta_part_approvals_name_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the approvals_name_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%')
    """
    if mapper.get('approvals_name_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_name_label'])
    else:
        log.warning('approvals_name_label value missing ... setting default (Name)')
        return text.replace(VALUE_SLOT, 'Name')


@no_type_check
def weave_meta_part_approvals_date_and_signature_label(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the approvals_date_and_signature_label from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%')
    """
    if mapper.get('approvals_date_and_signature_label'):
        return text.replace(VALUE_SLOT, mapper['approvals_date_and_signature_label'])
    else:
        log.warning('approvals_date_and_signature_label value missing ... setting default (Date and Signature)')
        return text.replace(VALUE_SLOT, 'Date and Signature')


@no_type_check
def weave_meta_part_header_issue_revision_combined(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Weave in the header_issue_revision_combined from mapper or default.

    Trigger is text.rstrip().endswith('%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%')
    """
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
    mapper: dict[str, str | int | bool | None],
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
        log.warning('proprietary_information value missing ... setting default (Proprietary Information MISSING)')
        return text.replace(VALUE_SLOT, 'Proprietary Information MISSING')


@no_type_check
def dispatch_meta_weaver(
    mapper: dict[str, str | int | bool | None],
    text: str,
) -> str:
    """Dispatch the meta weaver by mapping to handled groups per source marker."""
    dispatch = {
        '%%_PATCH_%_HEADER_%_TITLE_%%': weave_meta_part_header_title,
        '%%_PATCH_%_MAIN_%_TITLE_%%': weave_meta_part_title,
        '%%_PATCH_%_SUB_%_TITLE_%%': weave_meta_part_sub_title,
        '%%_PATCH_%_TYPE_%%': weave_meta_part_header_type,
        '%%_PATCH_%_ID_%%': weave_meta_part_header_id,
        '%%_PATCH_%_ISSUE_%%': weave_meta_part_issue,
        '%%_PATCH_%_REVISION_%%': weave_meta_part_revision,
        '%%_PATCH_%_DATE_%%': weave_meta_part_header_date,
        '%%_PATCH_%_FRAME_%_NOTE_%%': weave_meta_part_footer_frame_note,
        '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': weave_meta_part_footer_page_number_prefix,
        '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': weave_meta_part_change_log_issue_label,
        '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': weave_meta_part_change_log_revision_label,
        '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': weave_meta_part_change_log_date_label,
        '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': weave_meta_part_change_log_author_label,
        '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': weave_meta_part_change_log_description_label,
        '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': weave_meta_part_approvals_role_label,
        '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': weave_meta_part_approvals_name_label,
        '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': weave_meta_part_approvals_date_and_signature_label,
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': weave_meta_part_header_issue_revision_combined,
        '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': weave_meta_part_proprietary_information,
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
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
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
    rel_concat_folder_path = pathlib.Path("render/pdf/")
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)
    os.chdir(rel_concat_folder_path)
    log.info(f'meta (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    if not STRUCTURE_PATH.is_file() or not STRUCTURE_PATH.stat().st_size:
        log.error(f'meta failed to find non-empty structure file at {STRUCTURE_PATH}')
        return 1

    with open(STRUCTURE_PATH, 'rt', encoding=ENCODING) as handle:
        structure = yaml.safe_load(handle)

    targets = sorted(structure.keys())

    if not targets:
        log.error(f'structure at ({STRUCTURE_PATH}) does not provide any targets')
        return 1

    if target_code not in targets:
        log.error(f'structure does not provide ({target_code})')
        return 1

    if len(targets) == 1:
        target = targets[0]
        facets = sorted(list(facet.keys())[0] for facet in structure[target])
        log.info(f'found single target ({target}) with facets ({facets})')

        if facet_code not in facets:
            log.error(f'structure does not provide facet ({facet_code}) for target ({target_code})')
            return 1

        aspect_map = {}
        for data in structure[target]:
            if facet_code in data:
                aspect_map = data[facet_code]
                break
        missing_keys = [key for key in gat.KEYS_REQUIRED if key not in aspect_map]
        if missing_keys:
            log.error(
                f'structure does not provide all expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.error(f'- the found aspects: {sorted(aspect_map.keys())}')
            log.error(f'- missing aspects:   {sorted(missing_keys)}')
            return 1
        if sorted(aspect_map.keys()) != sorted(gat.KEYS_REQUIRED):
            log.warning(
                f'structure does not strictly provide the expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.warning(f'- found the following aspects instead:                   {sorted(aspect_map.keys())} instead')

        metadata = process_meta(aspect_map)
        if isinstance(metadata, int):
            return 1

    metadata_template = template.load_resource(METADATA_TEMPLATE, METADATA_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in metadata_template.split('\n')]
    lines = weave_meta_meta(metadata, lines)
    with open(METADATA_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    driver_template = template.load_resource(DRIVER_TEMPLATE, DRIVER_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in driver_template.split('\n')]
    lines = weave_meta_driver(metadata, lines)
    with open(DRIVER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    setup_template = template.load_resource(SETUP_TEMPLATE, SETUP_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in setup_template.split('\n')]
    lines = weave_meta_setup(metadata, lines)
    with open(SETUP_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    return 0
