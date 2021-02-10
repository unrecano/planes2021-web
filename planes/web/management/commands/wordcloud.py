from string import digits
from django.core.management.base import BaseCommand, CommandError
from wordcloud import WordCloud
from planes import settings
from web.models import Document

class Command(BaseCommand):

    def tokens_to_text(self, tokens):
        array = []
        for token in tokens:
            for i in range(1, int(token['frequency']) + 1):
                array.append(token['word'])
        return " ".join(array)

    def handle(self, *args, **options):
        documents = Document.objects.all()
        for document in documents:
            text = self.tokens_to_text(document.tokens)
            if len(text):
                wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white',
                        collocations = False,
                        min_font_size = 10).generate(text)
                wordcloud.to_file(f"{settings.MEDIA_ROOT}/{document.id}.png")
                document.wordcloud = f"{settings.MEDIA_URL}{document.id}.png"
                document.save()
                self.stdout.write(self.style.SUCCESS(f'{document} CREATED'))
            else:
                self.stdout.write(self.style.ERROR(f'{document} EMPTY'))