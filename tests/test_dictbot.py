# coding=utf-8
from errbot.backends.test import FullStackTest, popMessage


class TestCommands(FullStackTest):
    @classmethod
    def setUpClass(cls, extra=None):
        super(TestCommands, cls).setUpClass(__file__)

    def test_define(self):
        self.assertCommand('!define human', 'humanus')

    def test_battle(self):
        self.assertCommand('!battle toto vs titi', 'left')
        self.assertIn('WINNER', popMessage())