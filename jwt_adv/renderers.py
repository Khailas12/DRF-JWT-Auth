# Renderer classes allows you to return responses with various media types. There is also support for defining your own custom renderers, which gives you the flexibility to design your own media types.


import json
from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """        
        If we receive a `token` key as part of the response, it will be a
        byte object. Byte objects don't serialize well, so we need to
        decode it before rendering the User object.
        """
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            # Also as mentioned above, it'll decode `token` if it is of type
            # bytes
            data['token'] = token.decode('utf-8')

        return json.dumps({
            'user': data
        })
