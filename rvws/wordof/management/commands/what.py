from django.core.management.base import BaseCommand, CommandError
from wordof.models import *
from wordof.management.wordof.pitchfork import Pitchfork

class Command(BaseCommand):
  args = '<critic_name critic_name ...>'
  help = ''

  def handle(self, *args, **options):
    for critic_name in args:
      try:
        critic = Critic.objects.get(name=critic_name)
      except Critic.DoesNotExist:
        raise CommandError('Critic "%s" does not exist' % critic_id)

      for category in critic.category_set.all():
        self.stdout.write("category: %s" % category)

        source = Pitchfork(url=category.feed)
        for review in source.reviews:
          print review.artist
