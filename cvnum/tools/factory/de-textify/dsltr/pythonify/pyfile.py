#!/usr/bin/env python3

from collections import defaultdict
from pprint      import pformat
from re          import compile
from textwrap    import wrap

import black

from ..rules import *

# ! -- DEBUGGING -- ! #
from pprint import pprint
# ! -- DEBUGGING -- ! #


# ----------- #
# -- TOOLS -- #
# ----------- #

def addnewlines(n):
    return ['']*n


def taglang(lang):
    for old in '-[]':
        lang = lang.replace(old, "_")

    if lang[-1] == "_":
        lang = lang[:-1]

    return lang


def commentit(text):
    comment = []

    lines = wrap(text, width = 70)

    for oneline in lines:
        oneline = oneline.strip()

        comment.append(f'# {oneline}')

    return "\n".join(comment)


# ------------------------------------- #
# -- BUILD OF THE CONGIG PYTHON FILE -- #
# ------------------------------------- #

def pycode_spevars(spevars_used):
    spevars_code = []
    spevars_vals = {}
    spevars_nb   = -1

    for spekind in sorted(spevars_used.keys()):
        spevars = spevars_used[spekind]

        deco = '-'*(len(spekind) + 6)
        deco = f'# {deco} #'

        spevars_code.append(f"""
{deco}
# -- {spekind} -- #
{deco}
        """.strip())

        spevars_code += addnewlines(1)

        kind_spevars_code = []
        last_subkind      = ""

        for name in sorted(spevars.keys()):
            if name.startswith('DSL_TAG_'):
                subkind = name.split('_')[2]

                if subkind != last_subkind:
                    if last_subkind:
                        kind_spevars_code.append('')

                    last_subkind = subkind

            fulltxt = spevars[name]

            spevars_nb += 1
            kind_spevars_code.append(f"{name} = {spevars_nb}  # --> '{fulltxt}'")

            spevars_vals[name] = spevars_nb

        for spechar in '=#':
            imax = - 1

            for line in kind_spevars_code:
                if not line:
                    continue

                ichar = line.index(spechar)

                if ichar > imax:
                    imax = ichar

            for cursor, line in enumerate(kind_spevars_code):
                if not line:
                    continue

                ichar = line.index(spechar)
                line  = line[:ichar] + ' '*(imax - ichar) + line[ichar:]

                kind_spevars_code[cursor] = line


        spevars_code += kind_spevars_code
        spevars_code += addnewlines(2)

    spevars_code = '\n'.join(spevars_code[:-2])

    return spevars_code, spevars_vals


def pycode_naming(debug_coding, alltrans):
# Use of ``re.compile``.
    for lang, specs in alltrans.items():
        for length, matchrules in specs[DSL_SPECS_SMALL][DSL_ACTION_MATCHING].items():
            newspecs_small_matching = OrderedDict()

            for p, r in matchrules.items():
                newspecs_small_matching[compile(p)] = r

            specs[DSL_SPECS_SMALL][DSL_ACTION_MATCHING][length] = newspecs_small_matching

        if specs[DSL_SPECS_GENE][DSL_TAG_GENE_BIG]:
            specs[DSL_SPECS_GENE][DSL_TAG_GENE_BIG] = (
                compile(specs[DSL_SPECS_GENE][DSL_TAG_GENE_BIG][0]),
                specs[DSL_SPECS_GENE][DSL_TAG_GENE_BIG][1]
            )


# Translations code.
    code   = []

    for lang in sorted(alltrans.keys()):
        stdspecs = {
            k: alltrans[lang][k]
            for k in sorted(alltrans[lang].keys())
        }

        code.append(
            f'''
INT_2_NAME[{taglang(lang)}] = {stdspecs}
            '''
        )

    code = '\n'.join(code)

# Names of DSL actions
    spevars_used = defaultdict(dict)

    for name, fulltxt in globals().items():
        quotedtxt = f"'{fulltxt}'"

# We always need all the the comparator speecial variables!
        if name.startswith('DSL_'):
            spekind = name.split('_')[1]

            if quotedtxt in code:
                spevars_used[spekind][name] = fulltxt

                code = code.replace(quotedtxt, name)

            elif name.startswith('DSL_COMPOPE_'):
                spevars_used[spekind][name] = fulltxt

    code = code.replace(
        're.compile',
        '__re_compile'
    )

    for sep in ":,":
        for unwanted, wanted in [
            ("DSL_TAG_GENE_BIG"  , DSL_TAG_GENE_BIG),
            ("DSL_TAG_SIGN_MINUS", DSL_TAG_SIGN_MINUS),
            ("DSL_TAG_SIGN_PLUS" , DSL_TAG_SIGN_PLUS),
        ]:
            code = code.replace(
                f'{unwanted}{sep} {unwanted}',
                f'{unwanted}{sep} "{wanted}"'
            )
            code = code.replace(
                f'DSL_ACTION_VERBATIM{sep} {unwanted}',
                f'DSL_ACTION_VERBATIM{sep} "{wanted}"'
            )

    if debug_coding:
        code = black.format_file_contents(
            code,
            fast = False,
            mode = black.FileMode()
        )

    code = code.strip()

# Code for the special variables
    spevars_code, spevars_vals = pycode_spevars(spevars_used)

# Hard coding
    if not debug_coding:
        for name, hardcode in spevars_vals.items():
            for sep in ":,":
                code = code.replace(
                    f"{name}{sep}",
                    f"{hardcode}{sep}",
                )

            code = code.replace(
                f", {name}",
                f", {hardcode}",
            )

# Final code
    code = f'''
{spevars_code}


# ---------------------- #
# -- INTEGER --> NAME -- #
# ---------------------- #

INT_2_NAME = {{}}


{code}


# --------------------------------- #
# -- LIST OF ALL LANGS SUPPORTED -- #
# --------------------------------- #

ALL_LANGS = list(INT_2_NAME)
        '''.strip()



    return code


def tags_for_langs(all_langs, alldescs):
    tags_langs = {}

    for onelang in sorted(all_langs.keys()):
        tags_langs[taglang(onelang)] = onelang
        # print(all_langs[onelang])
        # BUG

    code = []

    for onetag, onelang in tags_langs.items():
        onedesc = commentit(alldescs[onelang])
        code += [
            f'{onedesc}',
            f'{onetag} = "{onetag}"',
            '',
        ]

    return "\n".join(code[:-1])



def pycode(debug_coding, alltrans, alldescs):
    code_tags_langs = tags_for_langs(alltrans, alldescs)
    code_naming     = pycode_naming(debug_coding, alltrans)

    return f'''
# -------------------- #
# -- TAGS FOR LANGS -- #
# -------------------- #

{code_tags_langs}


# ------------- #
# -- PATTERN -- #
# ------------- #

DSL_PATTERN_ELLIPSIS = __re_compile("(?P<bname>\.\.\.)")


{code_naming}
        '''.strip() + '\n'
