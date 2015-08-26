#!/usr/bin/env python

import sys
import os.path
import logging
import tinyletter

if __name__ == '__main__':

    import optparse
    parser = optparse.OptionParser()

    parser.add_option('--items', dest='items', default=15, help='')
    parser.add_option('--dest', dest='dest', default=None, help='')
    parser.add_option('--verbose', dest='verbose', help='Be chatty', action='store_true', default=False)

    options, args = parser.parse_args()
    
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    kwargs = { 'max_items': options.items, 'entextify': True }

    dest = os.path.abspath(options.dest)

    if not os.path.exists(dest):
        logging.error("%s does not exist" % dest)
        sys.exit()

    for url in args:

        tl = tinyletter.TinyLetter(url)

        for item in tl.as_list(**kwargs):

            link = item.get('link')
            base = os.path.basename(link)
            
            ymd = item['date'].strftime("%Y%m%d")
            fname = "%s-%s.md" % (ymd, base)

            path = os.path.join(dest, fname)
            logging.debug("write %s" % path)

            try:
                fh = open(path, 'w')
                tl.as_markdown_item(item, fh)
                fh.close()
            except Exception, e:
                logging.error("failed to write %s, because %s" % (path, e)
