# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 17:32
from __future__ import unicode_literals

from importlib import import_module
from django.db import migrations, models
from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname


def get_add_field_for_langs(name, **kwargs):
    ret = []

    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        trans_field = build_localized_fieldname(name, lang_code)
        ret.append(migrations.AddField(name=trans_field, **kwargs))

    return ret


class Migration(migrations.Migration):
    def __init__(self, name, app_label):
        # by changing app_label here to 'wagtailcore' we trick Django migrations system 
        # to think that this migration belongs to wagtailcore app
        # this is necessary to make model name resolution work
        app_label = 'wagtailcore'
        super(Migration, self).__init__(name, app_label)

        # import operations from wagtail migration we are replacing
        # and prepend them to operations of this migration
        mod_path = 'wagtail.{}.migrations.{}'.format(*self.replaces[0])
        orig_migration = import_module(mod_path).Migration
        self.operations[:0] = orig_migration.operations
        self.dependencies = orig_migration.dependencies

    # By using `replaces` we make sure that this migration doesn't have ambiguous `app_label`.
    # When this migration is applied Django writes only replaced migration
    # to django_migrations table in DB. Otherwise migration would have
    # 'wagtail_translation' as app_label in django_migrations table and
    # `migrate` command would consider this migration as unapplied due 
    # to app_label mismatch.
    replaces = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    # Dynamically define AddField operations for all Page field translations.
    # This always uses current AVAILABLE_LANGUAGES setting.
    # In case languages are changed after running this migration, `makemigrations`
    # command would do nothing for Page model. One would have to run `sync_translation_fields` 
    # command from modeltranslation to get DB schema in sync.
    _search_description = get_add_field_for_langs(
        'search_description',
        model_name='page',
        field=models.TextField(blank=True, null=True, verbose_name='search description'))
    _seo_title = get_add_field_for_langs(
        'seo_title',
        model_name='page',
        field=models.CharField(blank=True, help_text="Optional. 'Search Engine Friendly' title. This will appear at the top of the browser window.", max_length=255, null=True, verbose_name='page title'))
    _slug = get_add_field_for_langs(
        'slug',
        model_name='page',
        field=models.SlugField(allow_unicode=True, help_text='The name of the page as it will appear in URLs e.g http://domain.com/blog/[my-slug]/', max_length=255, null=True, verbose_name='slug'))
    _title = get_add_field_for_langs(
        'title',
        model_name='page',
        field=models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='title'))
    _url_path = get_add_field_for_langs(
        'url_path',
        model_name='page',
        field=models.TextField(blank=True, editable=False, null=True, verbose_name='URL path'))

    operations = _search_description + _seo_title + _slug + _title + _url_path