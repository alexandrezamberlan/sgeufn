from __future__ import unicode_literals

import locale
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin
from .forms import BuscaAtestadoManualForm
from .models import AtestadoManual


class AtestadoManualListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = AtestadoManual

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            # quando ja tem dados filtrando
            context['form'] = BuscaAtestadoManualForm(data=self.request.GET)
        else:
            # quando acessa sem dados filtrando
            context['form'] = BuscaAtestadoManualForm()
        return context

    def get_queryset(self):
        qs = super().get_queryset().all()

        if self.request.GET:
            # quando ja tem dados filtrando
            form = BuscaAtestadoManualForm(data=self.request.GET)
        else:
            # quando acessa sem dados filtrando
            form = BuscaAtestadoManualForm()

        if form.is_valid():
            pesquisa = form.cleaned_data.get('pesquisa')

            if pesquisa:
                qs = qs.filter(
                    Q(nome__icontains=pesquisa) | Q(atividade__icontains=pesquisa) | Q(responsavel__icontains=pesquisa))

        return qs


class AtestadoManualCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = AtestadoManual
    fields = ['nome', 'atividade', 'responsavel', 'instituicao', 'carga_horaria', 'data_inicio', 'data_fim',
              'is_active']
    success_url = 'atestado_manual_list'

    def get_success_url(self):
        messages.success(self.request, 'Atestado cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class AtestadoManualUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = AtestadoManual
    fields = ['nome', 'atividade', 'responsavel', 'instituicao', 'carga_horaria', 'data_inicio', 'data_fim',
              'is_active']
    success_url = 'atestado_manual_list'

    def get_success_url(self):
        messages.success(self.request, 'Atestado atualizado com sucesso na plataforma!')
        return reverse(self.success_url)


class AtestadoManualDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = AtestadoManual
    success_url = 'atestado_manual_list'

    def get_success_url(self):
        messages.success(self.request, 'Atestado removido com sucesso da plataforma!')
        return reverse(self.success_url)

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse Atestado, permissão negada!')
        return redirect(self.success_url)


class AtestadoManualPdfView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = AtestadoManual

    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        atestado_manual = self.get_object()

        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = f'attachment; filename="atestado_participacao_{atestado_manual.nome}_{atestado_manual.instituicao}.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4,
                                topMargin=1 * inch, bottomMargin=1 * inch,
                                leftMargin=1 * inch, rightMargin=1 * inch)
        story = []

        styles = getSampleStyleSheet()

        caminho_imagem = finders.find('core/img/logoUFN_hor.jpg')
        caminho_imagem_lap = finders.find('core/img/logo_lapinf_hor.png')

        imagem = Image(caminho_imagem, width=220, height=100)
        imagem_lap = Image(caminho_imagem_lap, width=220, height=75)

        # Estilo do título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=40,
            spaceBefore=40,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Estilo para texto justificado
        justify_style = ParagraphStyle(
            'JustifyStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=18
        )

        # Estilo para texto centralizado
        center_style = ParagraphStyle(
            'CenterStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )

        right_style = ParagraphStyle(
            'RightStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_RIGHT,
            fontName='Helvetica'
        )

        # colocar logo da UFN ao lado do logo do LAP
        # story.append(imagem)
        story.append(imagem_lap)

        # Título do documento
        story.append(Paragraph("ATESTADO DE PARTICIPAÇÃO", title_style))
        story.append(Spacer(1, 20))

        # Formatação das datas e horários
        data_inicio = atestado_manual.data_inicio.strftime('%d/%m/%Y') if atestado_manual.data_inicio else 'N/A'
        data_fim = atestado_manual.data_fim.strftime('%d/%m/%Y') if atestado_manual.data_fim else 'N/A'
        data_atual = timezone.now().date()

        texto_atestado = f"""
                Atestamos que <b>{atestado_manual.nome}</b> participou da atividade <b>{atestado_manual.atividade}</b>, 
                realizada no período de <b>{data_inicio}</b> a <b>{data_fim}</b>, 
                promovida pelo(a) <b>{atestado_manual.instituicao}</b>. 
                A referida atividade teve carga horária total de <b>{atestado_manual.carga_horaria}</b> 
                hora(s) e foi coordenada por <b>{atestado_manual.responsavel}</b>.
                <br/><br/>
                O código de verificação para validação do atestado é <b>{atestado_manual.codigo_matricula}</b>.
                """

        story.append(Paragraph(texto_atestado, justify_style))
        story.append(Spacer(1, 40))

        data_texto = f"Santa Maria, {data_atual.strftime('%d de %B de %Y')}."
        story.append(Paragraph(data_texto, right_style))
        story.append(Spacer(1, 50))

        # Texto final explicativo
        texto_final = """
        <i>O atestado de participação é gerado automaticamente pelo Sistema de Gestão de Eventos (SGEUFN), 
        no momento em que o participante confirma sua presença no evento. Para validar a autenticidade
        deste atestado, utilize o código de inscrição fornecido acima no formulário de validação do SGEUFN.</i>
        """

        story.append(Paragraph(texto_final, justify_style))
        story.append(Spacer(1, 40))

        # Rodapé com informações do sistema
        story.append(Spacer(1, 20))

        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique',
            textColor=colors.grey
        )

        rodape_texto = f"""
        ___________________________________________________<br/>
        Laboratório de Práticas Computação UFN<br/>
        Rua dos Andradas, 1614 – Santa Maria – RS<br/>
        CEP 97010-032 - https://sge.lapinf.ufn.edu.br
        """

        story.append(Paragraph(rodape_texto, footer_style))

        # Constrói o PDF
        doc.build(story)

        return response
