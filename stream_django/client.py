from stream_django import conf
import os
import stream


if conf.API_KEY and conf.API_SECRET:
    stream_client = stream.connect(
        conf.API_KEY, conf.API_SECRET)
else:
    stream_client = stream.connect()

if os.environ.get('STREAM_URL') is None and not(conf.API_KEY and conf.API_SECRET):
    raise KeyboardInterrupt('Stream credentials are not set in your settings')
