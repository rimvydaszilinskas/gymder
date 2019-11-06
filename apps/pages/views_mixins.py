from django.shortcuts import render
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

import json


class PageViewMixin(View):
    """
    Helper for writing Webpack based views

    Override `create_js_context` to set data to be used in JS
    
    Create `modify_context(request, context, *args, **kwargs)` to edit pre-send context

    `get` is handled by default
    """
    TITLE = None
    BUNDLE_NAME = None
    TEMPLATE_NAME = 'base.html'

    def create_js_context(self, request, *args, **kwargs):
        return None

    def get_context(self, request, *args, **kwargs):
        """ Setup the full context for rendering """
        context = {
            'bundle_name': self.BUNDLE_NAME
        }

        if hasattr(self, 'create_js_context'):
            js_context = self.create_js_context(request, *args, **kwargs)
            
            if js_context is not None:
                context['context'] = json.dumps(js_context, cls=DjangoJSONEncoder)
        
        if hasattr(self, 'TITLE') and self.TITLE:
            context['title'] = self.TITLE

        if hasattr(self, 'modify_context'):
            context = self.modify_context(request, context, *args, **kwargs)

        if hasattr(self, 'BUNDLE_NAME') and self.BUNDLE_NAME is not None:
            context['bundle_name'] = self.BUNDLE_NAME

        return context

    def get(self, request, *args, **kwargs):
        """ Package all the data and render response view """
        if self.TEMPLATE_NAME is None:
            raise Exception('TEMPLATE_NAME has to be defined')

        context = self.get_context(request, *args, **kwargs)

        return render(request, self.TEMPLATE_NAME, context)
