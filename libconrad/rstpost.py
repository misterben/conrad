from os import path as op

from docutils import nodes, core
from docutils.writers import html4css1
from docutils.parsers.rst import directives, Directive

from libconrad import models
from libconrad.template.rstextensions import RST_SETTINGS


class libconradWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = libconradTranslator
        self.visitor_attributes += ('libconradmeta',)


class libconradTranslator(html4css1.HTMLTranslator):
    def visit_libconradmeta(self, node):
        self.libconradmeta = '\n'.join(node.rawsource)

    def depart_libconradmeta(self, node):
        pass


class libconradMeta(Directive):
    '''libconrad config catcher for reStructuredText

    Usage::

      .. meta::

        various: configuration
    '''
    class libconradmeta(nodes.Special, nodes.PreBibliographic, nodes.Element):
        pass

    has_content = True

    def run(self):
        self.assert_has_content()
        return [self.libconradmeta(self.content)]

        node = nodes.Element()
        node += nodes.raw(self.content)
        return [nodes.docinfo(self.content)]

directives.register_directive('meta', libconradMeta)


class RstPost(models.Post):

    def __init__(self, *args, **kwargs):
        if not 'source' in kwargs:
            kwargs['source'] = '_post.html'
        super(RstPost, self).__init__(*args, **kwargs)

    @staticmethod
    def check(site, path):
        return models.Post.check(site, path) and path.endswith('.rst')

    def init(self):
        # dumb hack
        self.settings.date = self.date
        self.site.posts.append(self)
        self.site.posts.sort(cmp=models.postcmp, reverse=True)
        self.site.latest_post = self.site.posts[0]

        self._process_tags()

    def collect(self):
        # TODO: need the general solution for Jinja2 and rst to load sources 
        # with path prefixes
        
        source = file(op.join(self.site.env.loader.searchpath[0],
            self.path)).read()
        parts = core.publish_parts(source, writer=libconradWriter(),
                                   settings_overrides=RST_SETTINGS)
        self.settings.read(parts['libconradmeta'])
        self.settings.title = parts['title']
        self.settings.body = parts['body']


models.TYPE_LIST.insert(0, RstPost)
