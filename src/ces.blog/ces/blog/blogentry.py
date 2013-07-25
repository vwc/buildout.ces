from five import grok
from plone.directives import dexterity, form
from zope import schema
from plone.indexer import indexer

from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText
try:
    from plone.app.discussion.interfaces import IConversation
    USE_PAD = True
except ImportError:
    USE_PAD = False
from ces.blog import MessageFactory as _


class IBlogEntry(form.Schema, IImageScaleTraversable):
    """
    A single blogentry that can contain images
    """
    text = RichText(
        title=_(u"Blog Entry"),
        description=_(u"Please enter main body text for this blog entry"),
        required=False,
    )
    pressitem = schema.Bool(
        title=_(u"Mark this entry as pressrelease?"),
        default=False,
    )


@indexer(IBlogEntry)
def pressitemIndexer(obj):
    return obj.pressitem
grok.global_adapter(pressitemIndexer, name="pressitem")


class BlogEntry(dexterity.Container):
    grok.implements(IBlogEntry)


class View(grok.View):
    grok.context(IBlogEntry)
    grok.require('zope2.View')
    grok.name('view')

    def commentsEnabled(self, ob):
        if USE_PAD:
            conversation = IConversation(ob)
            return conversation.enabled()
        else:
            return self.portal_discussion.isDiscussionAllowedFor(ob)

    def commentCount(self, ob):
        if USE_PAD:
            conversation = IConversation(ob)
            return len(conversation)
        else:
            discussion = self.portal_discussion.getDiscussionFor(ob)
            return discussion.replyCount(ob)
