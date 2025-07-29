import redis
import os
import json
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, renderer_classes
from infrastructure.api.renderers import ServerSentEventRenderer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import StreamingHttpResponse, HttpResponseForbidden


@api_view(['GET'])
@renderer_classes([ServerSentEventRenderer])
def document_stream_view(request, document_id):
    token_str = request.GET.get('token')
    if not token_str:
        return HttpResponseForbidden('Token de autenticação não fornecido.')

    try:
        token = AccessToken(token_str)
        token.verify()
    except (InvalidToken, TokenError) as e:
        return HttpResponseForbidden(f'Token inválido ou expirado: {e}')

    redis_instance = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379))
    )
    pubsub = redis_instance.pubsub()
    channel_name = f"doc_stream:{document_id}"
    pubsub.subscribe(channel_name)

    def event_stream():
        try:
            yield 'data: {"event": "CONNECTION_ESTABLISHED"}\n\n'

            for message in pubsub.listen():
                if message['type'] == 'message':
                    data_payload = message['data'].decode('utf-8')

                    yield f'data: {data_payload}\n\n'

                    data_dict = json.loads(data_payload)
                    if data_dict.get('event') in ['STREAM_END', 'ERROR']:
                        break 
        finally:
            pubsub.close()

    response = StreamingHttpResponse(
        event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
