import liitos.meta as meta


def test_weave_meta_part_proprietary_information_on_empty_ok():
    assert meta.weave_meta_part_proprietary_information({}, '') == ''


def test_weave_meta_part_proprietary_information_on_value_slot_ok():
    assert meta.weave_meta_part_proprietary_information({}, '-VALUE.SLOT+') == '-Proprietary Information MISSING+'


def test_dispatch():
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
