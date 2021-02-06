import json
from django.core.management.base import BaseCommand, CommandError
from io import StringIO, BytesIO
from urllib import request
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfFileReader
from web.models import PoliticalOrganization, Document, Dimension

class Command(BaseCommand):
    help = "PDF to Text from JNE."

    URL = 'https://declara.jne.gob.pe/ASSETS/PLANGOBIERNO/FILEPLANGOBIERNO/'

    def get_info_from_pdf(self, pdf):
        response = {}
        reader = PdfFileReader(pdf)
        info = reader.getDocumentInfo()
        npages = reader.getNumPages()
        response['author'] = info.author
        response['pages'] = npages
        return response

    def get_text_from_pdf(self, pdf):
        output_string = StringIO()
        parser = PDFParser(pdf)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        return output_string.getvalue()

    def get_plan_by_id(self, id):
        url = 'https://plataformaelectoral.jne.gob.pe/Candidato/GetPlanGobiernoById/'
        response = json.loads(request.urlopen(f"{url}{id}").read())['data']
        dimensions = response['ListPGDSocial']\
            + response['ListPGDEconomica']\
            + response['ListPGDEconomica']\
            + response['ListPGDInstitucional']
        plans = []
        for dimension in dimensions:
            plan = {
                'id_plan': dimension['idPlanGobDimension'],
                'code': dimension['idPlanGobDimension'],
                'problem': dimension['strPGProblema'],
                'target': dimension['strPGObjetivo'],
                'goal': dimension['strPGMeta'],
                'trace': dimension['strPGIndicador'],
                'dimension': dimension['idPGDimension']
            }
            plans.append(plan)
        return plans
        

    def handle(self, *args, **options):
        organizations = PoliticalOrganization.objects.all()
        for organization in organizations:
            url = f'{self.URL}{organization.code}.pdf'
            pdf = BytesIO(request.urlopen(url).read())
            dparams = self.get_info_from_pdf(pdf)
            text = self.get_text_from_pdf(pdf)
            dparams['text'] = text
            dparams['name'] = f'{organization.code}.pdf'
            dparams['url'] = url
            dparams['political_organization'] = organization
            document, dcreated = Document.objects.update_or_create(
                name=f'{organization.code}.pdf',
                defaults=dparams
                )
            if dcreated:
                self.stdout.write(self.style.SUCCESS(f'{document} CREATED'))
            else:
                self.stdout.write(self.style.WARNING(f'{document} UPDATED'))
            
            dimensions = self.get_plan_by_id(organization.code)
            for dimension in dimensions:
                dimension['political_organization'] = organization
                obj, created = Dimension.objects.update_or_create(
                    code=dimension['code'],
                    id_plan=dimension['id_plan'],
                    defaults=dimension
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'{obj} CREATED'))
                else:
                    self.stdout.write(self.style.WARNING(f'{obj} UPDATED'))