from urllib2 import urlopen, quote
import simplejson
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd
from dictclient import Database, Connection

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
        return '\n\n'.join([definition.getword() + ': ' + definition.getdefstr() for definition in definitions])

    BREWERY_DB_TOKEN = 'e4a10b897c8cf67f6dc01d02dd769284'
    BREWERY_DB_URL_SEARCH = 'http://api.brewerydb.com/v2/search?key=%s'%BREWERY_DB_TOKEN

    @botcmd
    def beer(self, mess, args):
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
                self.send(mess.getFrom(), choosen_label)
            if name:
                shortdesc = name + '\n' + '-' * len(name) + '\n' + description
                self.send(mess.getFrom(), shortdesc)
            if style_name:
                styledesc = style_name + '\n' + '-' * len(style_name) + '\n' + style_description
                self.send(mess.getFrom(), styledesc)
        return '/me is looking for your beer'




