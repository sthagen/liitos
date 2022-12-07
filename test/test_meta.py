import os
import pathlib

import liitos.meta as meta

EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')


def test_weave_meta_part_proprietary_information_on_empty_ok():
    assert meta.weave_meta_part_proprietary_information({}, '') == ''


def test_weave_meta_part_proprietary_information_on_value_slot_ok():
    assert meta.weave_meta_part_proprietary_information({}, '-VALUE.SLOT+') == '-Proprietary Information MISSING+'


def test_meta_dispatch_no_match_let_pass_empty():
    assert meta.weave_meta_meta({'document': {'common': {}}}, []) == []


def test_meta_dispatch_no_match_let_pass():
    assert meta.weave_meta_meta({'document': {'common': {}}}, ['no-match']) == ['no-match', '\n']


def test_meta_dispatch():
    dispatch = {
        '%%_PATCH_%_HEADER_%_TITLE_%%': meta.weave_meta_part_header_title,
        '%%_PATCH_%_MAIN_%_TITLE_%%': meta.weave_meta_part_title,
        '%%_PATCH_%_SUB_%_TITLE_%%': meta.weave_meta_part_sub_title,
        '%%_PATCH_%_TYPE_%%': meta.weave_meta_part_header_type,
        '%%_PATCH_%_ID_%%': meta.weave_meta_part_header_id,
        '%%_PATCH_%_ISSUE_%%': meta.weave_meta_part_issue,
        '%%_PATCH_%_REVISION_%%': meta.weave_meta_part_revision,
        '%%_PATCH_%_DATE_%%': meta.weave_meta_part_header_date,
        '%%_PATCH_%_FRAME_%_NOTE_%%': meta.weave_meta_part_footer_frame_note,
        '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': meta.weave_meta_part_footer_page_number_prefix,
        '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': meta.weave_meta_part_change_log_issue_label,
        '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': meta.weave_meta_part_change_log_revision_label,
        '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': meta.weave_meta_part_change_log_date_label,
        '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': meta.weave_meta_part_change_log_author_label,
        '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': meta.weave_meta_part_change_log_description_label,
        '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': meta.weave_meta_part_approvals_role_label,
        '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': meta.weave_meta_part_approvals_name_label,
        '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': meta.weave_meta_part_approvals_date_and_signature_label,
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': meta.weave_meta_part_header_issue_revision_combined,
        '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': meta.weave_meta_part_proprietary_information,
    }
    expected = {
        '%%_PATCH_%_HEADER_%_TITLE_%%': '',
        '%%_PATCH_%_MAIN_%_TITLE_%%': '',
        '%%_PATCH_%_SUB_%_TITLE_%%': ' ',
        '%%_PATCH_%_TYPE_%%': 'Engineering Document',
        '%%_PATCH_%_ID_%%': 'P99999',
        '%%_PATCH_%_ISSUE_%%': '01',
        '%%_PATCH_%_REVISION_%%': '00',
        '%%_PATCH_%_DATE_%%': '01 FEB 2345',
        '%%_PATCH_%_FRAME_%_NOTE_%%': 'VERY CONSEQUENTIAL',
        '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': 'Page',
        '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': 'Iss.',
        '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': 'Rev.',
        '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': 'Date',
        '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': 'Author',
        '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': 'Description',
        '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': 'Approvals',
        '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': 'Name',
        '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': 'Date and Signature',
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': r'Iss \theMetaIssCode, Rev \theMetaRevCode',
        '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': 'Proprietary Information MISSING',
    }
    mapper = {'title': '', 'header_date': '01 FEB 2345'}
    value_slot_container = '-VALUE.SLOT+'
    wrapper = {'document': {'common': {**mapper}}}
    for trigger, weaver in dispatch.items():
        assert weaver(mapper, value_slot_container) == f'-{expected[trigger]}+'
        value_wrapper = f'-VALUE.SLOT+{trigger}'
        assert meta.weave_meta_meta(wrapper, [value_wrapper]) == [f'-{expected[trigger]}+{trigger}', '\n']


def test_meta_dispatch_explicit():
    dispatch = {
        '%%_PATCH_%_HEADER_%_TITLE_%%': meta.weave_meta_part_header_title,
        '%%_PATCH_%_MAIN_%_TITLE_%%': meta.weave_meta_part_title,
        '%%_PATCH_%_SUB_%_TITLE_%%': meta.weave_meta_part_sub_title,
        '%%_PATCH_%_TYPE_%%': meta.weave_meta_part_header_type,
        '%%_PATCH_%_ID_%%': meta.weave_meta_part_header_id,
        '%%_PATCH_%_ISSUE_%%': meta.weave_meta_part_issue,
        '%%_PATCH_%_REVISION_%%': meta.weave_meta_part_revision,
        '%%_PATCH_%_DATE_%%': meta.weave_meta_part_header_date,
        '%%_PATCH_%_FRAME_%_NOTE_%%': meta.weave_meta_part_footer_frame_note,
        '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': meta.weave_meta_part_footer_page_number_prefix,
        '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': meta.weave_meta_part_change_log_issue_label,
        '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': meta.weave_meta_part_change_log_revision_label,
        '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': meta.weave_meta_part_change_log_date_label,
        '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': meta.weave_meta_part_change_log_author_label,
        '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': meta.weave_meta_part_change_log_description_label,
        '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': meta.weave_meta_part_approvals_role_label,
        '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': meta.weave_meta_part_approvals_name_label,
        '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': meta.weave_meta_part_approvals_date_and_signature_label,
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': meta.weave_meta_part_header_issue_revision_combined,
        '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': meta.weave_meta_part_proprietary_information,
    }
    mapper = {
        'header_title': 'Ttt Tt',
        'title': 'Ttt Tt Tt',
        'sub_title': 'The Deep Spec',
        'header_type': 'Engineering Document',
        'header_id': 'MMI',
        'issue': '01',
        'revision': '00',
        'header_date': '01 FEB 2345',
        'footer_frame_note': 'VERY CONSEQUENTIAL',
        'footer_page_number_prefix': 'Page',
        'change_log_issue_label': 'Iss.',
        'change_log_revision_label': 'Rev.',
        'change_log_date_label': 'Date',
        'change_log_author_label': 'Author',
        'change_log_description_label': 'Description',
        'approvals_role_label': 'Approvals',
        'approvals_name_label': 'Name',
        'approvals_date_and_signature_label': 'Date and Signature',
        'header_issue_revision_combined': 'combined',
        'proprietary_information': 'test',
    }
    expected = {
        '%%_PATCH_%_HEADER_%_TITLE_%%': mapper['header_title'],
        '%%_PATCH_%_MAIN_%_TITLE_%%': mapper['title'],
        '%%_PATCH_%_SUB_%_TITLE_%%': mapper['sub_title'],
        '%%_PATCH_%_TYPE_%%': mapper['header_type'],
        '%%_PATCH_%_ID_%%': mapper['header_id'],
        '%%_PATCH_%_ISSUE_%%': mapper['issue'],
        '%%_PATCH_%_REVISION_%%': mapper['revision'],
        '%%_PATCH_%_DATE_%%': mapper['header_date'],
        '%%_PATCH_%_FRAME_%_NOTE_%%': mapper['footer_frame_note'],
        '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': mapper['footer_page_number_prefix'],
        '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': mapper['change_log_issue_label'],
        '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': mapper['change_log_revision_label'],
        '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': mapper['change_log_date_label'],
        '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': mapper['change_log_author_label'],
        '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': mapper['change_log_description_label'],
        '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': mapper['approvals_role_label'],
        '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': mapper['approvals_name_label'],
        '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': mapper['approvals_date_and_signature_label'],
        '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': mapper['header_issue_revision_combined'],
        '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': mapper['proprietary_information'],
    }

    value_slot_container = '-VALUE.SLOT+'
    wrapper = {'document': {'common': {**mapper}}}
    for trigger, weaver in dispatch.items():
        assert weaver(mapper, value_slot_container) == f'-{expected[trigger]}+'
        value_wrapper = f'-VALUE.SLOT+{trigger}'
        assert meta.weave_meta_meta(wrapper, [value_wrapper]) == [f'-{expected[trigger]}+{trigger}', '\n']


def test_driver_dispatch_no_match_let_pass():
    assert meta.weave_meta_driver({'document': {'common': {}}}, ['no-match']) == ['no-match', '\n']


def test_driver_dispatch_no_match_let_pass_empty():
    assert meta.weave_meta_driver({'document': {'common': {}}}, []) == []


def test_driver_dispatch():
    dispatch = {
        '%%_PATCH_%_TOC_%_LEVEL_%%': meta.weave_driver_toc_level,
        '%%_PATCH_%_LOF_%%': meta.weave_driver_list_of_figures,
        '%%_PATCH_%_LOT_%%': meta.weave_driver_list_of_tables,
    }
    expected = {
        '%%_PATCH_%_TOC_%_LEVEL_%%': '2',
        '%%_PATCH_%_LOF_%%': '%',
        '%%_PATCH_%_LOT_%%': '%',
    }
    mapper = {'title': '', 'header_date': '01 FEB 2345'}
    value_slot_container = '-VALUE.SLOT+'
    wrapper = {'document': {'common': {**mapper}}}
    for trigger, weaver in dispatch.items():
        assert weaver(mapper, value_slot_container) == f'-{expected[trigger]}+'
        value_wrapper = f'-VALUE.SLOT+{trigger}'
        assert meta.weave_meta_driver(wrapper, [value_wrapper]) == [f'-{expected[trigger]}+{trigger}', '\n']


def test_driver_dispatch_explicit():
    dispatch = {
        '%%_PATCH_%_TOC_%_LEVEL_%%': meta.weave_driver_toc_level,
        '%%_PATCH_%_LOF_%%': meta.weave_driver_list_of_figures,
        '%%_PATCH_%_LOT_%%': meta.weave_driver_list_of_tables,
    }
    expected = {
        # WARNING ignored toc level (5) set to default (2) - expected value 0 < toc_level < 5:
        '%%_PATCH_%_TOC_%_LEVEL_%%': '2',
        '%%_PATCH_%_LOF_%%': '',
        '%%_PATCH_%_LOT_%%': '%',
    }
    mapper = {'toc_level': 5, 'list_of_figures': '', 'list_of_tables': '%'}
    value_slot_container = '-VALUE.SLOT+'
    wrapper = {'document': {'common': {**mapper}}}
    for trigger, weaver in dispatch.items():
        assert weaver(mapper, value_slot_container) == f'-{expected[trigger]}+'
        value_wrapper = f'-VALUE.SLOT+{trigger}'
        assert meta.weave_meta_driver(wrapper, [value_wrapper]) == [f'-{expected[trigger]}+{trigger}', '\n']
    # Parked here for now: Not a number for toc level
    assert (
        meta.weave_driver_toc_level({'toc_level': 'x'}, '-VALUE.SLOT+%%_PATCH_%_TOC_%_LEVEL_%%')
        == '-2+%%_PATCH_%_TOC_%_LEVEL_%%'
    )
    # Parked here for now: Unaccepted value for switching of list of figures and tables
    assert (
        meta.weave_driver_list_of_figures({'list_of_figures': 'x'}, '-VALUE.SLOT+%%_PATCH_%_LOF_%%')
        == '-%+%%_PATCH_%_LOF_%%'
    )
    assert (
        meta.weave_driver_list_of_tables({'list_of_tables': 'x'}, '-VALUE.SLOT+%%_PATCH_%_LOT_%%')
        == '-%+%%_PATCH_%_LOT_%%'
    )


def test_setup_dispatch_no_match_let_pass_empty():
    assert meta.weave_meta_setup({'document': {'common': {}}}, []) == []


def test_setup_dispatch_no_match_let_pass():
    assert meta.weave_meta_setup({'document': {'common': {}}}, ['no-match']) == ['no-match', '\n']


def test_setup_dispatch():
    dispatch = {
        '%%_PATCH_%_FONT_%_PATH_%%': meta.weave_setup_font_path,
        '%%_PATCH_%_FONT_%_SUFFIX_%%': meta.weave_setup_font_suffix,
        '%%_PATCH_%_BOLD_%_FONT_%%': meta.weave_setup_bold_font,
        '%%_PATCH_%_ITALIC_%_FONT_%%': meta.weave_setup_italic_font,
        '%%_PATCH_%_BOLDITALIC_%_FONT_%%': meta.weave_setup_bold_italic_font,
        '%%_PATCH_%_MAIN_%_FONT_%%': meta.weave_setup_main_font,
        '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': meta.weave_setup_fixed_font_package,
        '%%_PATCH_%_CODE_%_FONTSIZE_%%': meta.weave_setup_code_fontsize,
        '%%_PATCH_%_CHOSEN_%_LOGO_%%': meta.weave_setup_chosen_logo,
    }
    d = {**meta.WEAVE_DEFAULTS}
    expected = {
        '%%_PATCH_%_FONT_%_PATH_%%': d['font_path'],
        '%%_PATCH_%_FONT_%_SUFFIX_%%': d['font_suffix'],
        '%%_PATCH_%_BOLD_%_FONT_%%': d['bold_font'],
        '%%_PATCH_%_ITALIC_%_FONT_%%': d['italic_font'],
        '%%_PATCH_%_BOLDITALIC_%_FONT_%%': d['bold_italic_font'],
        '%%_PATCH_%_MAIN_%_FONT_%%': d['main_font'],
        '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': d['fixed_font_package'],
        '%%_PATCH_%_CODE_%_FONTSIZE_%%': d['code_fontsize'],
        '%%_PATCH_%_CHOSEN_%_LOGO_%%': d['chosen_logo'],
    }
    mapper = {'title': '', 'header_date': '01 FEB 2345'}
    value_slot_container = '-VALUE.SLOT+'
    wrapper = {'document': {'common': {**mapper}}}
    for trigger, weaver in dispatch.items():
        assert weaver(mapper, value_slot_container) == f'-{expected[trigger]}+'
        value_wrapper = f'-VALUE.SLOT+{trigger}'
        assert meta.weave_meta_setup(wrapper, [value_wrapper]) == [f'-{expected[trigger]}+{trigger}', '\n']


def test_setup_dispatch_explicit():
    dispatch = {
        '%%_PATCH_%_FONT_%_PATH_%%': meta.weave_setup_font_path,
        '%%_PATCH_%_FONT_%_SUFFIX_%%': meta.weave_setup_font_suffix,
        '%%_PATCH_%_BOLD_%_FONT_%%': meta.weave_setup_bold_font,
        '%%_PATCH_%_ITALIC_%_FONT_%%': meta.weave_setup_italic_font,
        '%%_PATCH_%_BOLDITALIC_%_FONT_%%': meta.weave_setup_bold_italic_font,
        '%%_PATCH_%_MAIN_%_FONT_%%': meta.weave_setup_main_font,
        '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': meta.weave_setup_fixed_font_package,
        '%%_PATCH_%_CODE_%_FONTSIZE_%%': meta.weave_setup_code_fontsize,
        '%%_PATCH_%_CHOSEN_%_LOGO_%%': meta.weave_setup_chosen_logo,
    }
    d = {**meta.WEAVE_DEFAULTS}
    expected = {
        '%%_PATCH_%_FONT_%_PATH_%%': d['font_path'],
        '%%_PATCH_%_FONT_%_SUFFIX_%%': d['font_suffix'],
        '%%_PATCH_%_BOLD_%_FONT_%%': d['bold_font'],
        '%%_PATCH_%_ITALIC_%_FONT_%%': d['italic_font'],
        '%%_PATCH_%_BOLDITALIC_%_FONT_%%': d['bold_italic_font'],
        '%%_PATCH_%_MAIN_%_FONT_%%': d['main_font'],
        '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': d['fixed_font_package'],
        '%%_PATCH_%_CODE_%_FONTSIZE_%%': d['code_fontsize'],
        '%%_PATCH_%_CHOSEN_%_LOGO_%%': d['chosen_logo'],
    }
    mapper = {**d}
    value_slot_container = '-VALUE.SLOT+'
    wrapper = {'document': {'common': {**mapper}}}
    for trigger, weaver in dispatch.items():
        assert weaver(mapper, value_slot_container) == f'-{expected[trigger]}+'
        value_wrapper = f'-VALUE.SLOT+{trigger}'
        assert meta.weave_meta_setup(wrapper, [value_wrapper]) == [f'-{expected[trigger]}+{trigger}', '\n']


def test_ren_der():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
    }
    restore = os.getcwd()
    assert meta.weave(**parameters) == 0
    os.chdir(restore)
