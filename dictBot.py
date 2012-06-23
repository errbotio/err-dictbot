from time import sleep
from urllib2 import urlopen, quote, Request
import simplejson
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd
from dictclient import Database, Connection

GOOGLE_WEB_URL = ('https://ajax.googleapis.com/ajax/services/search/web?' +
                'v=1.0&q=%s')

class DictBot(BotPlugin):

    @botcmd
    def define(self, mess, args):
        """ Query dict.org for a definition
        Example: !define cat
        It will find the english definition of 'cat'
        """
        if not args:
            return 'You need at least a word as parameter.'
        args = args.strip()
        conn = Connection('dict.org')
        english = Database(conn, 'english')
        definitions = english.define(args)
        if not definitions:
            return 'Sorry I cannot find any definition for "%s"' % args
        return '\n\n'.join([definition.getword() + ': ' + definition.getdefstr() for definition in definitions])

    def get_estimated_count(self, query):
        request = Request(GOOGLE_WEB_URL % quote(query), None, {'Referer': 'http://www.gootz.net/'})
        response = urlopen(request)
        results = simplejson.load(response)
        return int(results['responseData']['cursor']['estimatedResultCount'])

    @botcmd
    def battle(self, mess, args):
        """ Shows you who wins between the two
        Example: !battle toto vs titi
        """
        SYNTAX = 'To start a google battle write a query like !battle toto vs titi'
        if not args or args.find(' vs ')== -1:
            return SYNTAX
        args = args.split(' vs ')
        left = args[0].strip()
        right = args[1].strip()
        if not left or not right:
            return SYNTAX
        left_result = self.get_estimated_count(left)
        self.send(mess.getFrom(), 'On the left "%s" gets %i points .... and on the right ... ' %(left, left_result), message_type=mess.getType())
        right_result = self.get_estimated_count(right)
        sleep(5)
        return '"%s" gets %i points!\nthe WINNER IS *** %s *** !!' %(right, right_result, left if left_result>right_result else right)


