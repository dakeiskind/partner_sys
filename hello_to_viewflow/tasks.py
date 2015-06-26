from __future__ import absolute_import
__author__ = 'dAKE'

from celery import shared_task
from viewflow.flow import flow_job
from viewflow.activation import Activation

@shared_task()
@flow_job()
def send_hello_world_request(activation):
    # with open(os.devnull, "w") as world:
    with open(r"D:\CodeStore\PyCharm\partner_sys\world.txt", mode='a') as world:
        world.write(activation.process.text)

# @shared_task()
# @flow_job()
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

@shared_task()
def mul(x, y):
    return x*y

