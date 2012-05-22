from botplugin import BotPlugin
from jabberbot import botcmd
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
        definitions = self.define(args)
        return '\n\n'.join([definition.getword() + ': ' + definition.getdefstr() for definition in definitions])

