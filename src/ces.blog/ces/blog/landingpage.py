from five import grok
from plone import api

from plone.dexterity.content import Item
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText
from plone.app.contentlisting.interfaces import IContentListing


from ces.blog.blogentry import IBlogEntry

from ces.blog import MessageFactory as _


# Interface class; used to define content-type schema.

class ILandingPage(form.Schema, IImageScaleTraversable):
    """
    A frontpage type
    """
    text = RichText(
        title=_(u"Body Text"),
        required=False,
    )


class LandingPage(Item):
    grok.implements(ILandingPage)


class View(grok.View):
    grok.context(ILandingPage)
    grok.require('zope2.View')
    grok.name('view')

    def blogitems(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        items = catalog(object_provides=IBlogEntry.__identifier__,
                        review_state='published',
                        sort_on='effective',
                        sort_order='reverse')
        return IContentListing(items)
