import liitos.captions as captions


def test_weave_on_empty_ok():
    assert captions.weave([]) == []


def test_weave_no_match_passes_through_ok():
    pass_me_through = ['a', 'b', 'caption', 'figure', 'table', 'label']
    assert captions.weave(pass_me_through) == pass_me_through


def test_weave_start_trigger():
    missing_end = ['a', '', r'\begin{longtable}', '', 'label']
    lost_most = ['a', '']
    assert captions.weave(missing_end) == lost_most


def test_weave_complete():
    complete = [
        'a',
        '',
        r'\begin{longtable}[]{@{}lcr@{}}',
        r'\caption{A caption for a table',
        r'\label{table:left-middle-right}}\tabularnewline',
        r'\toprule()\noalign{}',
        r'Left & Middle & Right \\',
        r'\midrule()\noalign{}',
        r'\endfirsthead',
        r'\toprule()\noalign{}',
        r'Left & Middle & Right \\',
        r'\midrule()\noalign{}',
        r'\endhead',
        r'\endlastfoot',
        r'L1 & M2 & R3 \\',
        r'\bottomrule()\noalign{}',
        r'\end{longtable}',
        '',
        'z',
    ]
    woven = [
        'a',
        '',
        r'\begin{longtable}[]{@{}lcr@{}}',
        r'\toprule()\noalign{}',
        r'Left & Middle & Right \\',
        r'\midrule()\noalign{}',
        r'\endfirsthead',
        r'\toprule()\noalign{}',
        r'Left & Middle & Right \\',
        r'\midrule()\noalign{}',
        r'\endhead',
        r'\caption{A caption for a table',
        r'\label{table:left-middle-right}}\tabularnewline',
        r'\endlastfoot',
        r'L1 & M2 & R3 \\',
        r'\bottomrule()\noalign{}',
        r'\end{longtable}',
        '',
        'z',
    ]
    assert captions.weave(complete) == woven
