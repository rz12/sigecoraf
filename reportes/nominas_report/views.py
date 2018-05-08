from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.aggregates import Count, Sum
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weasyprint import HTML, CSS


@api_view(['POST'])
def ver_rolpago(request):
    """
    return:
    """
    context = {
        'title': 'Rol de Pago',
        'titulo': 'Minería el Malecon',
        'subtitulo': 'Sistema de Gestión Coorporativo Financiero',
        'asunto': '',
        'detalle': 'Documento generado a partir de las Ordenes de Pago del Usuario',
        'fecha': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'usuario': '',
        'rol_pago': request.data,
    }
    html_template = get_template('nominas_report/templates/rol_pago.html')
    html = html_template.render(context)
    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rol_pago.pdf"'

    return response
