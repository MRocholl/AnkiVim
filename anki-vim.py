#!/usr/bin/env python3

""" Using VIM to generate textfiles which are directly anki-importable.  """

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import argparse
from os import getenv
from os.path import abspath, join as path_join

from ankivim.cards import create_card


def main():
    parser = argparse.ArgumentParser(
        description="Use VIM (or the editor of your choice) "
                    "to comfortably and quickly write textfiles "
                    "which are directly anki-importable. "
    )

    parser.add_argument(
        "deck", help='Name of the deck to write cards for.'
    )

    parser.add_argument(
        "-e", "--editor",
        help="Force using EDITOR, overwriting default behaviours.\n"
             "If set to anything else but vim(1), '--editor-args' must "
             "also be specified.\n"
             "Default behaviour for editor choices:\n"
             "1. read environment variable $EDITOR \n"
             "2. fall back to vim(1) if $EDITOR is not set.",
        action="store", dest="editor", default=None
    )

    parser.add_argument(
        "--editor-args",
        help="Arguments to pass to the editor upon calling. "
             "Must be specified (simplest case: empty string) when '--editor' "
             "is set.\n"
             'Expected format:"--arg1 VALUE1 --arg2 VALUE2 ..."\t\n'
             "(mind the quotes!)",
        action="store", dest="editor_args", default=None
    )

    args = parser.parse_args()

    if args.editor is not None and args.editor_args is None:
        raise ValueError()

    if args.editor is None:
        editor = getenv("EDITOR", "vim")
    else:
        editor = args.editor

    if args.editor_args is None:
        # editor args below target vim 7.4, overwrite for other editor choices.
        editor_args = (
            # set cursor below headers
            "-c {}".format(r'/\v\%\n\zs(^$|^[^\%]{1}.*$)'),
            # use anki_vim snippets
            "-c set filetype=anki_vim",
            # latex syntax highlighting
            "-c set syntax=tex"
        )
    else:
        if args.editor_args == "":
            editor_args = ()
        else:
            editor_args = args.editor_args.split(",")

    deckpath = path_join(abspath("./decks"), args.deck)

    content_added = True
    while content_added:
        # If a card is closed without content or changes, stop
        content_added = create_card(
            deckpath=deckpath, editor=editor, editor_args=editor_args
        )


if __name__ == '__main__':
    main()
