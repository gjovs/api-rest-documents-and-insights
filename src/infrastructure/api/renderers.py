from rest_framework.renderers import BaseRenderer


class ServerSentEventRenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'sse'
    charset = None  # SSE doesn't use charset

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Data should be a generator that yields SSE-formatted strings.
        """
        return data  # data must already be a generator yielding bytes or strings
