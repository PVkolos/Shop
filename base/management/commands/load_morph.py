from django.core.management.base import BaseCommand, CommandError
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


class Command(BaseCommand):
    help = 'load_morph'

    def handle(self, *args, **kwargs):
        try:
            pass
        except:
            raise CommandError('Initalization failed.')