
import time
import logging
from jaeger_client import Config


def init_tracer(service):
  logging.getLogger('').handlers = []
  logging.basicConfig(format='%(message)s', level=logging.DEBUG)

  config = Config(
      config={ # usually read from some yaml config
          'sampler': {
              'type': 'const',
              'param': 1,
          },
          'logging': True,
          'reporter_batch_size': 1,
      },
      service_name=service,
  )

  # this call also sets opentracing.tracer
  return config.initialize_tracer()

def say_hello(hello_to):
  with tracer.start_span('say-hello') as span:
      span.set_tag('hello-to', hello_to)

      hello_str = 'Hello, %s!' % hello_to
      span.log_kv({'event': 'string-format', 'value': hello_str})

      print(hello_str)
      span.log_kv({'event': 'println'})

tracer = init_tracer('hello-world')

say_hello("ABC")

# yield to IOLoop to flush the spans
time.sleep(2)
tracer.close()