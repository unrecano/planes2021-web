from string import digits
from django.core.management.base import BaseCommand, CommandError
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import regexp_tokenize, sent_tokenize
from web.models import Document, Sentence

class Command(BaseCommand):

    def handle(self, *args, **options):
        documents = Document.objects.all()
        numbers = [str(n) for n in range(0, 10000)]
        more_words = ['así', 'www', 'com', 'web', 'pe', 'N', 'S', 'I', 'Jr', 'Urb']
        stoplist = stopwords.words('spanish') \
            + list(digits) \
            + more_words \
            + list(numbers)
        for document in documents:
            dtokens = []
            words = regexp_tokenize(document.text, '\w+')
            tokens = [w for w in words if w.lower() not in stoplist]
            frecuencies = FreqDist(tokens)
            for word, frequency in frecuencies.items():
                dtokens.append({
                    'word': word,
                    'frequency': frequency
                })
            document.tokens = dtokens
            document.save()
            self.stdout.write(self.style.WARNING(f'{document} UPDATED'))

            # Partir por oraciones.
            
            sentences = sent_tokenize(document.text)
            i = 0
            for sentence in sentences:
                params = {'text': sentence}
                i += 1
                obj, created = Sentence.objects.update_or_create(
                    number=i,
                    document=document,
                    defaults=params
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'{obj} CREATED'))
                else:
                    self.stdout.write(self.style.WARNING(f'{obj} UPDATED'))