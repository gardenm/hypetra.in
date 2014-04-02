from django.core.management.base import BaseCommand, CommandError
from wordof.models import *
from wordof.management.wordof.pitchfork import Pitchfork
from wordof.management.wordof.metacritic import Metacritic


class Command(BaseCommand):
    args = '<critic_name critic_name ...>'
    help = ''

    def handle(self, *args, **options):
        for critic_name in args:
            try:
                critic = Critic.objects.get(name=critic_name)
            except Critic.DoesNotExist:
                raise CommandError('Critic "%s" does not exist' % critic_name)

            for category in critic.category_set.all():
                self.stdout.write("category: %s" % category)

                # TODO: Can factor more out of the Metacritic/Pitchfork creation ... it's very similar now.
                if critic.name == 'Pitchfork':
                    source = Pitchfork()
                else:
                    source = Metacritic()

                for feed_name, feed in source.feeds.iteritems():
                    for review in source.feeds[feed_name].reviews:
                        print review.artifact.artist
