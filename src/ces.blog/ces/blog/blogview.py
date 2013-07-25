import calendar
from Acquisition import aq_inner
from DateTime import DateTime
from five import grok
from plone import api

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

from plone.app.discussion.interfaces import IConversation
from plone.app.contentlisting.interfaces import IContentListing

from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces import IFolderish

from ces.blog.blogentry import IBlogEntry


class BlogView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('blog-view')

    def blogitems(self):
        """List all blog items as brains"""
        year = int(self.request.form.get('year', 0))
        month = int(self.request.form.get('month', 0))
        subject = self.request.form.get('category', None)
        return self.get_entries(year=year, month=month, subject=subject)

    def batch(self):
        b_size = 5
        b_start = self.request.form.get('b_start', 0)
        return Batch(self.blogitems(), b_size, b_start, orphan=1)

    def commentsEnabled(self, ob):
        conversation = IConversation(ob)
        return conversation.enabled()

    def commentCount(self, ob):
        conversation = IConversation(ob)
        return len(conversation)

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = IBlogEntry.__identifier__
        path = '/'.join(context.getPhysicalPath())
        return dict(path={'query': path, 'depth': 2},
                    object_provides=obj_provides,
                    sort_on='effective', sort_order='reverse')

    def get_entries(self, year=None, month=None, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = self._base_query()
        if subject:
            query['Subject'] = subject
        if year:
            if month:
                lastday = calendar.monthrange(year, month)[1]
                startdate = DateTime(year, month, 1, 0, 0)
                enddate = DateTime(year, month, lastday, 23, 59, 59)
            else:
                startdate = DateTime(year, 1, 1, 0, 0)
                enddate = DateTime(year, 12, 31, 0, 0)
            query['effective'] = dict(query=(startdate, enddate),
                                      range='minmax')
        results = catalog.searchResults(**query)[:5]
        return IContentListing(results)


class BlogCategoryView(grok.View):
    grok.context(IFolderish)
    grok.require('zope2.View')
    grok.name('blog-category-view')

    def blogitems(self):
        """List all blog items as brains"""
        year = int(self.request.form.get('year', 0))
        month = int(self.request.form.get('month', 0))
        subject = self.request.form.get('category', None)
        return self.get_entries(year=year, month=month, subject=subject)

    def batch(self):
        b_size = 5
        b_start = self.request.form.get('b_start', 0)
        return Batch(self.blogitems(), b_size, b_start, orphan=1)

    def commentsEnabled(self, ob):
        conversation = IConversation(ob)
        return conversation.enabled()

    def commentCount(self, ob):
        conversation = IConversation(ob)
        return len(conversation)

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = IBlogEntry.__identifier__
        path = '/'.join(context.getPhysicalPath())
        return dict(path={'query': path, 'depth': 2},
                    object_provides=obj_provides,
                    sort_on='effective', sort_order='reverse')

    def get_entries(self, year=None, month=None, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = self._base_query()
        if subject:
            query['Subject'] = subject
        if year:
            if month:
                lastday = calendar.monthrange(year, month)[1]
                startdate = DateTime(year, month, 1, 0, 0)
                enddate = DateTime(year, month, lastday, 23, 59, 59)
            else:
                startdate = DateTime(year, 1, 1, 0, 0)
                enddate = DateTime(year, 12, 31, 0, 0)
            query['effective'] = dict(query=(startdate, enddate),
                                      range='minmax')
        results = catalog.searchResults(**query)[:5]
        return IContentListing(results)


class PressView(grok.View):
    grok.context(IFolderish)
    grok.require('zope2.View')
    grok.name('press-view')

    def update(self):
        self.has_pressitem = len(self.pressitems()) > 0

    def pressitems(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        results = catalog(object_provides=IBlogEntry.__identifier__,
                          review_state="published",
                          pressitem=True,
                          sort_on="effective",
                          sort_order="reverse")
        return IContentListing(results)
