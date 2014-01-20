# (C) Michael DeHaan, 2014.
#
# This file is part of Slide The Relevator
#
# Slide The Revelator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Slide The Relevator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

__version__ = '0.1'
__author__ = 'Michael DeHaan'

import yaml
import StringIO


REVEAL_HEADER = """
<!doctype html>
<html lang="en">

        <head>
                <meta charset="utf-8">

                <title>reveal.js - The HTML Presentation Framework</title>

                <meta name="description" content="A framework for easily creating beautiful presentations using HTML">
                <meta name="author" content="Hakim El Hattab">

                <meta name="apple-mobile-web-app-capable" content="yes" />
                <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

                <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

                <link rel="stylesheet" href="css/reveal.min.css">
                <link rel="stylesheet" href="css/theme/default.css" id="theme">

                <!-- For syntax highlighting -->
                <link rel="stylesheet" href="lib/css/zenburn.css">

                <!-- If the query includes 'print-pdf', use the PDF print sheet -->
                <script>
                        document.write( '<link rel="stylesheet" href="css/print/' + ( window.location.search.match( /print-pdf/gi ) ? 'pdf' : 'paper' ) + '.css" type="text/css" media="print">' );
                </script>

                <!--[if lt IE 9]>
                <script src="lib/js/html5shiv.js"></script>
                <![endif]-->
        </head>

        <body>

     <div class="reveal">

                        <!-- Any section element inside of this container is displayed as a slide -->
                        <div class="slides">

"""

REVEAL_FOOTER = """

                       </div>

                </div>

                <script src="lib/js/head.min.js"></script>
                <script src="js/reveal.min.js"></script>

                <script>

                        // Full list of configuration options available here:
                        // https://github.com/hakimel/reveal.js#configuration
                        Reveal.initialize({
                                controls: true,
                                progress: true,
                                history: true,
                                center: true,

                                theme: Reveal.getQueryHash().theme, // available themes are in /css/theme
                                transition: Reveal.getQueryHash().transition || 'default', // default/cube/page/concave/zoom/linear/fade/none

                                // Parallax scrolling
                                // parallaxBackgroundImage: 'https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg',
                                // parallaxBackgroundSize: '2100px 900px',

                                // Optional libraries used to extend on reveal.js
                                dependencies: [
                                        { src: 'lib/js/classList.js', condition: function() { return !document.body.classList; } },
                                        { src: 'plugin/markdown/marked.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                                        { src: 'plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                                        { src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
                                        { src: 'plugin/zoom-js/zoom.js', async: true, condition: function() { return !!document.body.classList; } },
                                        { src: 'plugin/notes/notes.js', async: true, condition: function() { return !!document.body.classList; } }
                                ]
                        });

                </script>

        </body>
</html>


"""

class Deck(object):

   def __init__(self, filename):
       self.filename = filename
       fh = open(self.filename, 'r')
       self.data = yaml.load(fh.read())
       self.io = StringIO.StringIO()
       fh.close()       
 
   def run(self):
       self.write_header(self.data.get('header',{}))
       self.write_slides(self.data['slides'])
       self.write_footer(self.data.get('footer',{}))
       return self.io.getvalue()

   def write_slides(self, data):
       for x in data:
           self.write_slide(x)

   def write_header(self, data):
       self.io.write(REVEAL_HEADER)

   def write_footer(self, data):
       self.io.write(REVEAL_FOOTER)

   def write_slide(self, slide_data):
       self.io.write("<section>\n")
       for elem in slide_data:
           if type(elem) != dict:
               raise Exception("expected a list of dicts")           
           for (k,v) in elem.iteritems():
               self.io.write("<%s>%s</%s>" % (k,v,k))
       self.io.write("</section>")
       

                       
