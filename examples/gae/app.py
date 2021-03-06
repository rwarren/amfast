import logging
import os
import traceback

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import apiproxy_stub_map

import amfast
from amfast.remoting.memcache_subscription_manager import MemcacheSubscriptionManager
from amfast.remoting.gae_channel import GaeChannelSet, GaeChannel

import autoretry

# Setup AmFast here.
# This code gets run once per webserver.
amfast.log_debug = False # Set to True to log AmFast debug messages
channel_set = GaeChannelSet(subscription_manager=MemcacheSubscriptionManager())

if os.environ['SERVER_SOFTWARE'].find('Development') >= 0:
    # Use regular polling when running under development server.
    # Long poll setup does not seem to work correctly in development server.
    channel_set.mapChannel(GaeChannel('amf'))
else:
    # User long polling when running on GAE.
    channel_set.mapChannel(GaeChannel('amf', wait_interval=20000, poll_interval=500))

def main():
    """
    GAE handlers with a 'main' function are cached.
    Every request will cause this function to be called.

    'run_wsgi_app' converts CGI requests to WSGI requests.
    """

    run_wsgi_app(channel_set)

def log_datastore_access():
    """Logs DB query data."""
    def hook(service, call, request, response):
        logging.info('%s %s - %s' % (service, call, str(request)))
        stack = traceback.format_stack()
        logging.debug('%s %s - %s' % (service, call, "n".join(stack)))

    apiproxy_stub_map.apiproxy.GetPreCallHooks().Append('db_log', hook, 'datastore_v3')

if __name__ == "__main__":
    #log_datastore_access() #Un-comment this to view how the datastore is being accessed. 

    # This wrapper script automatically re-tries datastore queries that timeout.
    autoretry.autoretry_datastore_timeouts()
    main()
