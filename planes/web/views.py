from django.shortcuts import render
from web.models import Document, Sentence, PoliticalOrganization

def index(request):
    pos = []
    for organization in PoliticalOrganization.objects.all():
        document = organization.documents.first()
        po = {
            'name': organization.name,
            'url': document.url,
            'words': sorted(document.tokens, key=lambda k: k['frequency'],
                reverse=True)[:10],
            'document': document.id,
            'wordcloud': document.wordcloud
        }
        pos.append(po)

    return render(request, 'web/index.html', {'pos': pos})

def search(request):
    words = request.GET.get('query') if request.GET.get('query') else ''
    query_words = [word.strip() for word in words.split(' ') if word]
    pos = []
    if words:
        for organization in PoliticalOrganization.objects.all():
            tokens = []
            document = organization.documents.first()
            for token in document.tokens:
                if token['word'] in query_words:
                    tokens.append(token)

            if len(tokens):
                po = {
                    'name': organization.name,
                    'url': document.url,
                    'words': tokens,
                    'document': document.id
                }
                pos.append(po)

    return render(request, 'web/search.html', {'pos': pos, 'words': words})

def detail(request, id):
    words = request.GET.get('words')
    document = Document.objects.get(id=id)
    sentences = []
    if words:
        query_words = [word.strip() for word in words.split(' ') if word]
        sentences = Sentence.objects.search(query_words).filter(document=document)
    context = {
        'document': document,
        'sentences': sentences,
        'word': words
    }
    
    return render(request, 'web/detail.html', context)