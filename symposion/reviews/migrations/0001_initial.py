# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReviewAssignment'
        db.create_table('reviews_reviewassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['proposals.ProposalBase'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('origin', self.gf('django.db.models.fields.IntegerField')()),
            ('assigned_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('opted_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('reviews', ['ReviewAssignment'])

        # Adding model 'ProposalMessage'
        db.create_table('reviews_proposalmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['proposals.ProposalBase'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('message', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('submitted_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('_message_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('reviews', ['ProposalMessage'])

        # Adding model 'Review'
        db.create_table('reviews_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['proposals.ProposalBase'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vote', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('comment', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('submitted_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('_comment_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('reviews', ['Review'])

        # Adding model 'LatestVote'
        db.create_table('reviews_latestvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['proposals.ProposalBase'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vote', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('submitted_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('reviews', ['LatestVote'])

        # Adding unique constraint on 'LatestVote', fields ['proposal', 'user']
        db.create_unique('reviews_latestvote', ['proposal_id', 'user_id'])

        # Adding model 'ProposalResult'
        db.create_table('reviews_proposalresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.OneToOneField')(related_name='result', unique=True, to=orm['proposals.ProposalBase'])),
            ('score', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=5, decimal_places=2)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('vote_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('plus_one', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('plus_zero', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minus_zero', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minus_one', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('accepted', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='undecided', max_length=20)),
        ))
        db.send_create_signal('reviews', ['ProposalResult'])

        # Adding model 'Comment'
        db.create_table('reviews_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['proposals.ProposalBase'])),
            ('commenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('commented_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('_text_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('reviews', ['Comment'])

        # Adding model 'NotificationTemplate'
        db.create_table('reviews_notificationtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reviews', ['NotificationTemplate'])

        # Adding model 'ResultNotification'
        db.create_table('reviews_resultnotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['proposals.ProposalBase'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.NotificationTemplate'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('to_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reviews', ['ResultNotification'])


    def backwards(self, orm):
        # Removing unique constraint on 'LatestVote', fields ['proposal', 'user']
        db.delete_unique('reviews_latestvote', ['proposal_id', 'user_id'])

        # Deleting model 'ReviewAssignment'
        db.delete_table('reviews_reviewassignment')

        # Deleting model 'ProposalMessage'
        db.delete_table('reviews_proposalmessage')

        # Deleting model 'Review'
        db.delete_table('reviews_review')

        # Deleting model 'LatestVote'
        db.delete_table('reviews_latestvote')

        # Deleting model 'ProposalResult'
        db.delete_table('reviews_proposalresult')

        # Deleting model 'Comment'
        db.delete_table('reviews_comment')

        # Deleting model 'NotificationTemplate'
        db.delete_table('reviews_notificationtemplate')

        # Deleting model 'ResultNotification'
        db.delete_table('reviews_resultnotification')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'conference.conference': {
            'Meta': {'object_name': 'Conference'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('timezones.fields.TimeZoneField', [], {'default': "'US/Eastern'", 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'conference.section': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'Section'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Conference']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposals.additionalspeaker': {
            'Meta': {'unique_together': "(('speaker', 'proposalbase'),)", 'object_name': 'AdditionalSpeaker', 'db_table': "'proposals_proposalbase_additional_speakers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposalbase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposals.ProposalBase']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['speakers.Speaker']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'proposals.proposalbase': {
            'Meta': {'object_name': 'ProposalBase'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_additional_notes_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_notes': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['speakers.Speaker']", 'symmetrical': 'False', 'through': "orm['proposals.AdditionalSpeaker']", 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposals.ProposalKind']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': "orm['speakers.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposals.proposalkind': {
            'Meta': {'object_name': 'ProposalKind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposal_kinds'", 'to': "orm['conference.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'reviews.comment': {
            'Meta': {'object_name': 'Comment'},
            '_text_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'commented_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['proposals.ProposalBase']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'})
        },
        'reviews.latestvote': {
            'Meta': {'unique_together': "[('proposal', 'user')]", 'object_name': 'LatestVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['proposals.ProposalBase']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'reviews.notificationtemplate': {
            'Meta': {'object_name': 'NotificationTemplate'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reviews.proposalmessage': {
            'Meta': {'ordering': "['submitted_at']", 'object_name': 'ProposalMessage'},
            '_message_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['proposals.ProposalBase']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'reviews.proposalresult': {
            'Meta': {'object_name': 'ProposalResult'},
            'accepted': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minus_one': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minus_zero': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'plus_one': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'plus_zero': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'proposal': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'result'", 'unique': 'True', 'to': "orm['proposals.ProposalBase']"}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '5', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'undecided'", 'max_length': '20'}),
            'vote_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'reviews.resultnotification': {
            'Meta': {'object_name': 'ResultNotification'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['proposals.ProposalBase']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.NotificationTemplate']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'to_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        'reviews.review': {
            'Meta': {'object_name': 'Review'},
            '_comment_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': "orm['proposals.ProposalBase']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        'reviews.reviewassignment': {
            'Meta': {'object_name': 'ReviewAssignment'},
            'assigned_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opted_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin': ('django.db.models.fields.IntegerField', [], {}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposals.ProposalBase']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'speakers.speaker': {
            'Meta': {'ordering': "['name']", 'object_name': 'Speaker'},
            '_biography_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'biography': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'invite_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'speaker_profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['reviews']