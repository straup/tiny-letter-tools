#!/usr/bin/env python

import sys
import logging
import tinyletter

if __name__ == '__main__':

    import optparse
    parser = optparse.OptionParser()

    parser.add_option('--items', dest='items', default=15, help='')
    parser.add_option('--verbose', dest='verbose', help='Be chatty', action='store_true', default=False)

    options, args = parser.parse_args()
    
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    kwargs = { 'max_items': options.items }

    fh = sys.stdout

    for url in args:

        tl = tinyletter.TinyLetter(url)
        tl.as_markdown(fh, **kwargs)
