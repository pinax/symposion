from django.db import models
from django.db.models.query import QuerySet


class CachingM2MQuerySet(QuerySet):
    
    def __init__(self, *args, **kwargs):
        super(CachingM2MQuerySet, self).__init__(*args, **kwargs)
        self.cached_m2m_field = kwargs["m2m_field"]
    
    def iterator(self):
        parent_iter = super(CachingM2MQuerySet, self).iterator()
        m2m_model = getattr(self.model, self.cached_m2m_field).through
        
        for obj in parent_iter:
            if obj.id in cached_objects:
                setattr(obj, "_cached_m2m_%s" % self.cached_m2m_field)
            yield obj


class ProposalManager(models.Manager):
    def cache_m2m(self, m2m_field):
        return CachingM2MQuerySet(self.model, using=self._db, m2m_field=m2m_field)
        AdditionalSpeaker = queryset.model.additional_speakers.through
        additional_speakers = collections.defaultdict(set)
        for additional_speaker in AdditionalSpeaker._default_manager.filter(proposal__in=queryset).select_related("speaker__user"):
            additional_speakers[additional_speaker.proposal_id].add(additional_speaker.speaker)