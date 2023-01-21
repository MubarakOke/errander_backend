from rest_framework.renderers import JSONRenderer

class DefaultRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response= ""
        if 'Error' in str(data):
            response= {"error" : data}
        else:
            response= {"data": data}
        data= response
        return super().render(data, accepted_media_type, renderer_context)