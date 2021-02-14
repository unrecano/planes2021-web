from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from web.models import Document, Sentence, PoliticalOrganization, Dimension

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
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

@cache_page(CACHE_TTL)
def search(request):
    words = request.GET.get('query') if request.GET.get('query') else ''
    query_words = [word.strip() for word in words.split(' ') if word]
    pos = []
    if words:
        for organization in PoliticalOrganization.objects.all():
            document = organization.documents.first()
            tokens = document.matched_tokens(query_words)

            if len(tokens):
                po = {
                    'name': organization.name,
                    'url': document.url,
                    'words': tokens,
                    'document': document.id
                }
                pos.append(po)

    return render(request, 'web/search.html', {'pos': pos, 'words': words})

@cache_page(CACHE_TTL)
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

@cache_page(CACHE_TTL)
def summary(request):
    query = request.GET.get('query')
    dimensions = dict(Dimension.DIMENSION)
    organizations = PoliticalOrganization.objects.all()
    pos = []
    if query:
        for organization in organizations:
            po = {
                'name': organization.name
            }
            po['dimensions'] = Dimension.objects.filter(political_organization=organization).filter(dimension=query).order_by('dimension')
            pos.append(po)
    else:
        for organization in organizations:
            po = {
                'name': organization.name
            }
            po['dimensions'] = Dimension.objects.filter(political_organization=organization).order_by('dimension')
            pos.append(po)
    context = {
        'dimensions': dimensions,
        'organizations': pos
    }
    return render(request, 'web/summary.html', context)

@cache_page(CACHE_TTL)
def about(request):
    return render(request, 'web/about.html', {})