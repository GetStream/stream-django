from stream_django.client import stream_client


def stream(request):
    context = {}
    context['STREAM_API_KEY'] = stream_client.api_key
    context['STREAM_SITE_ID'] = stream_client.site_id
    return context