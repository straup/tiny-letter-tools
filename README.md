# tiny-letter-tools

Miscellaneous tools for doing things with Tiny Letter mailing lists.

## mk-rss-feed.py

### For example (abstract)

	url = sys.argv[1]
	rss = sys.stdout

	tl = TinyLetter(url)
	tl.as_rss(rss)

### For example (concrete)

	$> python ./mk-rss-feed.py https://tinyletter.com/danhon/ > danhon.rss
	$> xmllint --format danhon.rss

	<?xml version="1.0" encoding="iso-8859-1"?>
	<rss version="2.0">
	  <channel>
	    <title> Things That Have Caught My Attention by danhon </title>
	    <link>https://tinyletter.com/danhon/</link>
	    <description> by danhon </description>
	    <lastBuildDate>Sat, 07 Jun 2014 12:50:04 GMT</lastBuildDate>
	    <item>
	      <title>Episode Ninety Seven: That Most Killer Of Deals; Need To Know</title>
	      <link>https://tinyletter.com/danhon/letters/</link>
	      <description>I got a bunch of notes back about what I wrote the other day about my depression. I don't really mind writing about it, and I think it's a tragedy that more people don't understand how someone can loo</description>
	      <guid>a3f6a69df8a62e61951f25f3dc1d06f6</guid>
	      <pubDate>Sat, 07 Jun 2014 00:00:00 GMT</pubDate>
	    </item>
	    <item>
	      <title>Episode Ninety Six: And Then It Came Back; Meek, Meeker, Meekest</title>
	      <link>https://tinyletter.com/danhon/letters/episode-ninety-six-and-then-it-came-back-meek-meeker-meekest</link>
	      <description>A difficult day, as you'll see below. And the baby monitor app isn't working, so I'm upstairs, typing quietly and quickly whilst watching my son sleep. But, tomorrow's Friday, and my one meeting is ab</description>
	      <guid>b22f44bd1ff7fcb4bb0a1aa5ab98c61a</guid>
	      <pubDate>Fri, 06 Jun 2014 00:00:00 GMT</pubDate>
	    </item>
	
	<-- and so on... -->

### Dependencies

* https://pypi.python.org/pypi/BeautifulSoup/
* https://pypi.python.org/pypi/PyRSS2Gen/

## See also

* http://tinyletter.com
