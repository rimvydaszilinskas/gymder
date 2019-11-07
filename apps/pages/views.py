from django.shortcuts import render
from django.views import View

from .views_mixins import PageViewMixin


class IndexView(PageViewMixin):
    TITLE = 'Homepage'
    BUNDLE_NAME = 'index'
        