# coding=utf-8
from errbot.backends.test import FullStackTest, popMessage


class TestCommands(FullStackTest):

    def test_define(self):
        self.assertCommand('!define human', 'humanus')

    def test_battle(self):
        self.assertCommand('!battle toto vs titi', 'left')
        self.assertIn('WINNER', popMessage())
