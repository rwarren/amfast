"""An example server using the CherryPy web framework."""
import os
import optparse

import cherrypy

import amfast
from amfast.remoting.cherrypy_channel import CherryPyChannelSet, CherryPyChannel
import utils

class App(CherryPyChannelSet):
    """Base web app."""

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('/addressbook.html')

if __name__ == '__main__':
    usage = """usage: %s [options]""" % __file__
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-p", default=8000,
        dest="port", help="port number to serve")
    parser.add_option("-d", default="localhost",
        dest="domain", help="domain to serve")
    parser.add_option("-l", action="store_true",
        dest="log_debug", help="log debugging output")
    (options, args) = parser.parse_args()

    amfast.log_debug = options.log_debug

    cp_options = {
        'global':
        {
            'server.socket_port': int(options.port),
            'server.socket_host': str(options.domain),
        },
        '/':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.getcwd(), '../flex/deploy')
        }
    }

    channel_set = App()
    rpc_channel = CherryPyChannel('amf')
    channel_set.mapChannel(rpc_channel)
    utils.setup_channel_set(channel_set)

    cherrypy.quickstart(channel_set, '/', config=cp_options)

    print "Serving on %s:%s" % (options.domain, options.port)
    print "Press ctrl-c to halt."
