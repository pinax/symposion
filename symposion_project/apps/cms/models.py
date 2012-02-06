from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from markitup.fields import MarkupField

from taggit.managers import TaggableManager

from mptt.models import MPTTModel, TreeForeignKey
from mptt.utils import drilldown_tree_for_node


class ContentBase(models.Model):
    
    STATUS_CHOICES = (
        (1, _("Draft")),
        (2, _("Public")),
    )

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True, null=True)
    body = MarkupField()

    tags = TaggableManager(blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    published = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(editable=False, default=datetime.now)
    updated = models.DateTimeField(editable=False, default=datetime.now)

    class Meta:
        abstract = True


class Page(MPTTModel, ContentBase):

    parent = TreeForeignKey("self", null=True, blank=True, related_name="children")
    ordering = models.PositiveIntegerField(default=1)
    path = models.TextField(blank=True, editable=False)

    def __unicode__(self):
        return self.title

    def save(self, calculate_path=True, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        if calculate_path:
            self.calculate_path()
    
    def calculate_path(self):
        self.path = ""
        for page in drilldown_tree_for_node(self):
            if page == self:
                self.path += page.slug
                break
            else:
                self.path += "%s/" % page.slug
        self.save(calculate_path=False)

    class MPTTMeta:
        order_insertion_by = ["ordering", "title"]


class MenuItem(MPTTModel):
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children")

    url = models.CharField(max_length=200)

    published = models.BooleanField(default=True)
    login_required = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.name


    class MPTTMeta:
        order_insertion_by = ["ordering", "name"]
