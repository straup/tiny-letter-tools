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
    parser.add_option('--html', dest='html', action='store_true', default=False, help='')
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

        newsletter = os.path.basename(url)

        root = os.path.join(dest, newsletter)

        if not os.path.exists(root):
            os.makedirs(root)

        tl = tinyletter.TinyLetter(url)

        for item in tl.as_list(**kwargs):

            link = item.get('link')

            if not link:
                logging.warning("bogus link, skipping")
                continue

            base = os.path.basename(link)
            
            ymd = item['date'].strftime("%Y%m%d")
            fname = "%s-%s.md" % (ymd, base)

            if options.html:
                fname = "%s-%s.html" % (ymd, base)

            path = os.path.join(root, fname)
            logging.debug("write %s" % path)

            try:
                fh = open(path, 'w')

                if options.html:
                    tl.as_html_item(item, fh)
                else:
                    tl.as_markdown_item(item, fh)

                fh.close()
            except Exception, e:
                logging.error("failed to write %s, because %s" % (path, e))
