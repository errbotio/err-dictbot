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

    BREWERY_DB_TOKEN = 'e4a10b897c8cf67f6dc01d02dd769284'
    BREWERY_DB_URL_SEARCH = 'http://api.brewerydb.com/v2/search?key=%s'%BREWERY_DB_TOKEN

    @botcmd
    def beer(self, mess, args):
        """
        Find back a beer from the Brewery DB
        """
        args = args.strip()
        if not args:
            return 'What beer do you want me to search for ?'
        content = urlopen(self.BREWERY_DB_URL_SEARCH + '&q=' + quote(args.strip()) + '&type=beer' )
        results = simplejson.load(content)
        for beer_data in results.get('data', []):
            name = beer_data.get('name', None)
            description = beer_data.get('description', '')
            labels = beer_data.get('labels', None)
            label_icon = labels.get('icon') if labels else None
            label_medium = labels.get('medium') if labels else None
            label_large = labels.get('large') if labels else None
            choosen_label = label_medium if label_medium else label_large if label_large else label_icon if label_icon else None
            style = beer_data.get('style', None)
            style_name = style.get('name', '') if style else None
            style_description = style.get('description', None) if style else None
            if choosen_label:
                self.send(mess.getFrom(), choosen_label, message_type=mess.getType())
            if name:
                shortdesc = name + '\n' + description
                self.send(mess.getFrom(), shortdesc, message_type=mess.getType())
            #if style_name:
            #    styledesc = style_name + '\n' + '-' * len(style_name) + '\n' + style_description
            #    self.send(mess.getFrom(), styledesc, message_type=mess.getType())
        return '/me is looking for your beer'

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


