"""Helper classes to allow function testing with a testbrowser"""

from pylons import config
from pylons.test import pylonsapp
from repoze.tm import TM
import zope.testbrowser.wsgi

adhocracy_domain = config.get('adhocracy.domain').strip()
app_url = "http://%s" % adhocracy_domain
instance_url = "http://test.%s" % adhocracy_domain


class Browser(zope.testbrowser.wsgi.Browser):
    """Simplify zope.testbrowser sessions"""

    REMOTE_USER_HEADER = 'REMOTE_USER'

    app_url = app_url
    instance_url = instance_url

    def dc(self, filename="/tmp/test-output.html"):
        open(filename, 'w').write(self.contents)

    def login(self, username):
        self.logout()
        # 'REMOTE_USER' will turn into HTTP_REMOTE_USER in the wsgi environ.
        self.addHeader(self.REMOTE_USER_HEADER, username)

    def logout(self):
        self.mech_browser.addheaders = [header for header in
                                        self.mech_browser.addheaders if
                                        header[0] != self.REMOTE_USER_HEADER]


class AdhocracyAppLayer(zope.testbrowser.wsgi.Layer):
    """Layer to setup the WSGI app"""

    def make_wsgi_app(self):
        app = pylonsapp
        app = zope.testbrowser.wsgi.AuthorizationMiddleware(app)
        app = TM(app)
        zope.testbrowser.wsgi._allowed.add(adhocracy_domain)
        zope.testbrowser.wsgi._allowed_2nd_level.add(adhocracy_domain)
        return app

    def setUp(test, *args, **kwargs):
        print(
            "\n--------------------------------------------------------------"
            "\n--- Setting up database test environment, please stand by. ---"
            "\n--------------------------------------------------------------"
            "\n")
        #TODO start solr and co

    def tearDown(self, test):
        pass


ADHOCRACY_LAYER = AdhocracyAppLayer()
ADHOCRACY_LAYER_APP = ADHOCRACY_LAYER.make_wsgi_app()
