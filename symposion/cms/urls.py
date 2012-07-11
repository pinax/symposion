from django.conf.urls.defaults import url, patterns

PAGE_RE = r"(([\w-]{1,})(/[\w-]{1,})*)/"

urlpatterns = patterns("symposion.cms.views",
    url(r"^(?P<path>%s)_edit/$" % PAGE_RE, "page_edit", name="cms_page_edit"),
    url(r"^(?P<path>%s)$" % PAGE_RE, "page", name="cms_page"),
)
