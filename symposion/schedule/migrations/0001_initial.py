# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schedule'
        db.create_table('schedule_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conference.Section'], unique=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('schedule', ['Schedule'])

        # Adding model 'Day'
        db.create_table('schedule_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Schedule'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('schedule', ['Day'])

        # Adding unique constraint on 'Day', fields ['schedule', 'date']
        db.create_unique('schedule_day', ['schedule_id', 'date'])

        # Adding model 'Room'
        db.create_table('schedule_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Schedule'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('schedule', ['Room'])

        # Adding model 'SlotKind'
        db.create_table('schedule_slotkind', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Schedule'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('schedule', ['SlotKind'])

        # Adding model 'Slot'
        db.create_table('schedule_slot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Day'])),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.SlotKind'])),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('content_override', self.gf('markitup.fields.MarkupField')(no_rendered_field=True, blank=True)),
            ('_content_override_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('schedule', ['Slot'])

        # Adding model 'SlotRoom'
        db.create_table('schedule_slotroom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Slot'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Room'])),
        ))
        db.send_create_signal('schedule', ['SlotRoom'])

        # Adding unique constraint on 'SlotRoom', fields ['slot', 'room']
        db.create_unique('schedule_slotroom', ['slot_id', 'room_id'])

        # Adding model 'Presentation'
        db.create_table('schedule_presentation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='content_ptr', unique=True, null=True, to=orm['schedule.Slot'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('abstract', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presentations', to=orm['speakers.Speaker'])),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('proposal_base', self.gf('django.db.models.fields.related.OneToOneField')(related_name='presentation', unique=True, to=orm['proposals.ProposalBase'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presentations', to=orm['conference.Section'])),
            ('_description_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_abstract_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('schedule', ['Presentation'])

        # Adding M2M table for field additional_speakers on 'Presentation'
        m2m_table_name = db.shorten_name('schedule_presentation_additional_speakers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('presentation', models.ForeignKey(orm['schedule.presentation'], null=False)),
            ('speaker', models.ForeignKey(orm['speakers.speaker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['presentation_id', 'speaker_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SlotRoom', fields ['slot', 'room']
        db.delete_unique('schedule_slotroom', ['slot_id', 'room_id'])

        # Removing unique constraint on 'Day', fields ['schedule', 'date']
        db.delete_unique('schedule_day', ['schedule_id', 'date'])

        # Deleting model 'Schedule'
        db.delete_table('schedule_schedule')

        # Deleting model 'Day'
        db.delete_table('schedule_day')

        # Deleting model 'Room'
        db.delete_table('schedule_room')

        # Deleting model 'SlotKind'
        db.delete_table('schedule_slotkind')

        # Deleting model 'Slot'
        db.delete_table('schedule_slot')

        # Deleting model 'SlotRoom'
        db.delete_table('schedule_slotroom')

        # Deleting model 'Presentation'
        db.delete_table('schedule_presentation')

        # Removing M2M table for field additional_speakers on 'Presentation'
        db.delete_table(db.shorten_name('schedule_presentation_additional_speakers'))


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
        'schedule.day': {
            'Meta': {'ordering': "['date']", 'unique_together': "[('schedule', 'date')]", 'object_name': 'Day'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Schedule']"})
        },
        'schedule.presentation': {
            'Meta': {'ordering': "['slot']", 'object_name': 'Presentation'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_description_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'copresentations'", 'blank': 'True', 'to': "orm['speakers.Speaker']"}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal_base': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'presentation'", 'unique': 'True', 'to': "orm['proposals.ProposalBase']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presentations'", 'to': "orm['conference.Section']"}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'content_ptr'", 'unique': 'True', 'null': 'True', 'to': "orm['schedule.Slot']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presentations'", 'to': "orm['speakers.Speaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schedule.room': {
            'Meta': {'object_name': 'Room'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Schedule']"})
        },
        'schedule.schedule': {
            'Meta': {'ordering': "['section']", 'object_name': 'Schedule'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'section': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['conference.Section']", 'unique': 'True'})
        },
        'schedule.slot': {
            'Meta': {'ordering': "['day', 'start', 'end']", 'object_name': 'Slot'},
            '_content_override_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_override': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.SlotKind']"}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'schedule.slotkind': {
            'Meta': {'object_name': 'SlotKind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Schedule']"})
        },
        'schedule.slotroom': {
            'Meta': {'ordering': "['slot', 'room__order']", 'unique_together': "[('slot', 'room')]", 'object_name': 'SlotRoom'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Room']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Slot']"})
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

    complete_apps = ['schedule']