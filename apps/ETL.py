from abc import ABC, abstractmethod
import sys, fitz
import cv2
import matplotlib.pyplot as plt
import fitz
from fitz import Document, Page, Rect
import codecs
import os
import platform
from pdf2image import convert_from_path
import re
import numpy as np
import pandas as pd
import xlsxwriter
import logging
import logging.config
import yaml
from django.conf import settings

with open('log.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

DIR_EXCEL = F'{settings.MEDIA_ROOT}/tmp/excel'
DIR_IMAGEM = F'{settings.MEDIA_ROOT}/tmp/imagens'
DIR_ARQUIVO_TEXTO = F'{settings.MEDIA_ROOT}/texto'
DIR_SAIDA_PDF = F'{settings.MEDIA_ROOT}/tmp/pdf'
POPPLER_PATH = r"C:\Users\danie\poppler-22.12.0\Library\bin"

'''
Estas classes definem o processo de ETL (Extração - Tranformação - Carregamento) dos dados provenientes das faturas em pdf.
'''
class FaturaBase(ABC):
    '''
    Esta classe é uma interface para a etapa de extração de dados de faturas em pdf.
    '''
    def __init__(self, nome_arquivo_fatura: str):
        self.nome_arquivo = nome_arquivo_fatura
        self.nome_arquivo_img = None
        self.nome_arquivo_texto = None
        self.img = None
        self.doc = None
        self.page = None
        self.rectangles_list = []
        self.keywords = {
            'Itens de Fatura' : {
                'caixa': 'DESCRIÇÃO DO FATURAMENTO',
                'x_colunas': [362.52, 374.4, 396.36, 426.6, 448.56, 473.4, 495.72, 513.72, 531.36],
                'x_width': [84.24, 11.88, 21.96, 30.24, 21.96, 24.84, 22.32, 18, 17.64],
                'texto': [],
                'texto_saida': [],
                'campos': ['Itens de Fatura','Unid','Quant.','Preço unit (R$) com tributos','Valor (R$)','PIS/CONFINS','Base Calc ICMS (R$)', 'Alíquota ICMS','ICMS','Tarifa unit (R$)'],
                'filtros': ['r1','r1','r1','r2','r1','r1','r2','r2','r1','r2'],
                'tipo_de_dados': [str, str, float, float, float, float, float, str, float, float]
            },
            'Grandezas': {
                'caixa': 'DADOS DE MEDIÇÃO',
                'x_colunas': [81.36, 141.12, 174.6, 200.16, 227.16, 249.12],
                'x_width': [39.24, 59.76, 33.48, 25.56, 27, 21.96],
                'texto': [],
                'texto_saida': [],
                'campos': ['Medidor','Grandezas','Postos Tarifários','Leitura Anterior','Leitura Atual','Const. Medidor','Consumo kWh'],
                'filtros': ['r1','r1','r2','r2','r2','r2','r2'],
                'tipo_de_dados': [str, str, str, float, float, int, float]
            },
            'MÊS/ANO': {
                'caixa': 'HISTÓRICO DO FATURAMENTO',
                'x_colunas': [90.72, 129.24, 177.84, 212.76, 261.36],
                'x_width': [49.32, 38.52, 48.6, 34.92, 48.6],
                'texto': [],
                'texto_saida': [],
                'campos': ['MÊS/ANO','Demanda Hora Ponta','Demanda Hora Fora Ponta','Consumo Faturado Hora Ponta', 'Consumo Faturado Hora Fora Ponta'],
                'filtros': ['r1','r-2','r-2','r-2','r-2','r-2'],
                'tipo_de_dados': [str, float, float, float, float, int]
            },
            'PIS/PASEP': {
                'caixa': 'TRIBUTOS',
                'x_colunas': [72.72, 110.16, 146.16],
                'x_width': [30.24, 37.44, 36],
                'texto': [],
                'texto_saida': [],
                'campos': ['TRIBUTOS', 'BASE CALC (R$)', 'ALIQUOTA (%)', 'VALOR (R$)'],
                'filtros': [None, None, None, None],
                'tipo_de_dados': [str, float, float, float]
            }
        }


    @abstractmethod
    def extrair(self):
        pass


    def converteParaImagem(self):
        fatura = self.nome_arquivo
        if platform.system() == 'Windows':
            pages = convert_from_path(fatura, poppler_path=POPPLER_PATH)
        else:
            pages = convert_from_path(fatura)
        
        filename = os.path.split(self.nome_arquivo)[-1]
        filename = filename.split('.')[0]
        self.nome_arquivo_img = f"{DIR_IMAGEM}/{filename}.jpg"

        # Salva somente primeira pagina
        pages[0].save(self.nome_arquivo_img, "JPEG")


    def detectaCaixas(self, plotar=False):
        '''
            Identifica as caixas a partir da imagem da fatura e preenche as coordenadas na variável rectangles_list
        '''
        assert self.nome_arquivo_img is not None, "Certifique-se de chamar o método converteParaImagem primeiro."
        
        self.img = cv2.imread(self.nome_arquivo_img)
        # Restringe a área de interesse
        self.img = self.img[0:1940, 0:2339]
        # Aplica escala de cinza
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) #convert to gray scale
        if plotar:
            fig = plt.figure(figsize= [10,10])
            plt.title('Escala cinza', fontweight ="bold")
            plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

        # Aplicar limiarização. Ajuste do limiar está no segundo parâmetro da função
        ret,thresh = cv2.threshold(gray,200,255,0) 
        if plotar:
            fig = plt.figure(figsize= [10,10])
            plt.title('Limiarizacao', fontweight ="bold")
            plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))

        # Detectar contornos
        contours, _ = cv2.findContours(thresh, 1, 2)
        
        for cnt in contours:
            x1,y1 = cnt[0][0]
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                if w > 10 and w > 50 and w < 1650:
                    logger.debug(f'Dimensions: {x,y,w,h}')
                    rectangle = [x, y, w, h]
                    self.rectangles_list.append(rectangle)
                    self.img = cv2.rectangle(self.img,(x,y),(x+w,y+h),(0,255,0),3)

        if plotar:
            fig= plt.figure(figsize= [10,10])
            plt.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
            path, filename = os.path.split(self.nome_arquivo_img)
            plt.savefig(os.path.join(path, "Caixas_" + filename))
            plt.show()
    

    def checaLarguradaCaixa(self, keyword, rect) -> bool:
        '''
            Verifica se a soma das larguras das colunas é menor que a largura da caixa. 
            Caso contrário, significa que a caixa identificada não atende.
        '''
        return True if sum(self.keywords[keyword]['x_width']) < (rect.x1 - rect.x0) else False


    def checaPalavrasChave(self, text_box, rect):
        assert self.page is not None, "page não pode ser nulo. Certifique-se de chamar a função extraiTextoDoDocumento primeiro"
        
        x2_limit = rect.x1
        keyword = [item for item in self.keywords.keys() if item in text_box]
        idx = 0
        if len(keyword) > 0:
            keyword = keyword[0]
            if self.checaLarguradaCaixa(keyword, rect):
                for x_width in self.keywords[keyword]['x_width']:
                    idx += 1
                    rect.x1 = rect.x0 + x_width
                    self.page.draw_rect(rect, width=1, color=(0, 1, 0))
                    text = self.page.get_textbox(rect)
                    self.keywords[keyword]['texto'].append(text)
                    logger.debug(f'Coluna {idx}:\n{text}\n')
                    rect.x0 = rect.x1
            
                # Ultima coluna
                idx += 1
                rect.x1 = x2_limit
                self.page.draw_rect(rect, width=1, color=(0, 1, 0))
                text = self.page.get_textbox(rect)
                self.keywords[keyword]['texto'].append(text)
                logger.debug(f'Coluna {idx}:\n{text}\n')



    def extraiTexto(self, file=None):
        assert len(self.rectangles_list) > 0, "Caixas não podem estar vazias. Certifique-se de executar o método detectaCaixas primeiro"
        assert self.page is not None, "page não pode ser nulo. Certifique-se de chamar a função extraiTextoDoDocumento primeiro"

        for idx, rectangle in enumerate(self.rectangles_list):
            MULT = 0.36
            rectangle = [item * MULT for item in rectangle]
            x0, y0, x1, y1 = rectangle[0], rectangle[1], rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]
            rect_object = Rect(x0, y0, x1, y1)
            text_box = self.page.get_textbox(rect_object)
            self.page.draw_rect(rect_object, width=2, color=(1, 0, 0))
            logger.debug(f'Retangulo {idx+1}. x1: {x0}, y1: {y0}, x2: {x1}, y2: {y1}\n{text_box}\n')
            self.checaPalavrasChave(text_box, rect_object)
            if file is not None:
                file.write(f'👉 Retângulo {idx+1}\n{text_box}\n\n')



    def extraiTextoDoDocumento(self, salvar_saida=True):
        self.doc: Document = fitz.open(self.nome_arquivo)
        self.page: Page = self.doc[0]
        self.page.clean_contents() 

        if salvar_saida:
            filename = os.path.split(self.nome_arquivo)[-1]
            filename = filename.split('.')[0] + str('.txt')
            self.nome_arquivo_texto = f'{DIR_ARQUIVO_TEXTO}/{filename}'
            file = codecs.open(self.nome_arquivo_texto, "w", "utf-8")
            
            self.extraiTexto(file)
            
            file.close()
            head, tail = os.path.split(self.nome_arquivo)
            viz_name = os.path.join(DIR_SAIDA_PDF, "Caixas_" + tail)
            self.doc.save(viz_name)

        else:
            self.extraiTexto()
            self.deletaImagemFatura()
        logger.debug(self.keywords)

    
    def deletaImagemFatura(self):
        filename = os.path.split(self.nome_arquivo)[-1]
        filename = filename.split('.')[0]
        imagem_fatura = f"{DIR_IMAGEM}/{filename}.jpg"
        imagem_caixa_fatura = f"{DIR_IMAGEM}/Caixas_{filename}.jpg"
        
        os.remove(imagem_fatura)
        if os.path.exists(imagem_caixa_fatura):
            os.remove(imagem_caixa_fatura) 


    def processaTexto(self):
        number = 0
        with open(self.nome_arquivo_texto, "r", encoding="utf8") as file:
            for i, line in enumerate(file):
                if re.search(r"^👉", line, re.IGNORECASE):
                    number += 1
                    logger.debug(line)


    def filtraCampos(self):
        for keyword, fields in self.keywords.items():
            logger.debug(f'keyword: {keyword}\nfields: {fields}\n')
            assert len(self.keywords[keyword]['filtros']) > 0, f"Não foi encontrado nenhum campo filtros na palavra-chave {keyword}"

            for idx, filtro in enumerate(fields['filtros']):
                logger.debug(f'idx: {idx}\nfiltro: {filtro}\ntexto de saida:\n{self.keywords[keyword]["texto_saida"][idx]}\n')
                if filtro is None:
                    continue

                if filtro.startswith('r'):
                    qtd_linhas = int(re.findall(r'[-+]?[.]?[\d]', filtro)[0])
                    logger.debug(f'remove {qtd_linhas} linhas')
                    if qtd_linhas > 0:
                        self.keywords[keyword]['texto_saida'][idx] = fields['texto_saida'][idx][qtd_linhas:]
                    else:
                        self.keywords[keyword]['texto_saida'][idx] = fields['texto_saida'][idx][:qtd_linhas]    
                    
                    # for _ in range(abs(qtd_linhas)):
                    #     if qtd_linhas < 0:
                    #         self.keywords[keyword]['texto_saida'][idx].pop(-1)
                    #     else:
                    #         self.keywords[keyword]['texto_saida'][idx].pop(1)
                logger.debug(f'SAIDA:\nidx: {idx}\nfiltro: {filtro}\ntexto de saida:\n{self.keywords[keyword]["texto_saida"][idx]}\n')


    def processaDadosEntrada(self):
        '''
            Esta função divide cada campo da caixa correspondente à
            palavra-chave em linhas a partir do caractere '\n'
        '''
        for key, fields in self.keywords.items():
            texto_saida = [row.split('\n') for row in fields['texto']]
            fields['texto_saida'] = texto_saida


    def exportaParaExcel(self):
        filename = os.path.split(self.nome_arquivo)[-1]
        filename = filename.split('.')[0]
        filename = f"{DIR_EXCEL}/{filename}.xlsx"

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        row, column, init_row, last_keyword = 0, 0, 0, 0

        for keyword, fields in self.keywords.items():
            assert len(fields['texto_saida']) > 0, f"Campo texto_saida da palavra-chave {keyword} não pode ser vazio"

            column = 0
            init_row = init_row + len(self.keywords[last_keyword]['texto_saida'][0]) + 3 if last_keyword != 0 else 0
            worksheet.write(init_row, column, fields['caixa'])
            row = init_row + 1

            for idx, campo in enumerate(fields['campos']):
                try:
                    worksheet.write(row, column, campo)
                except:
                    worksheet.write(row, column, '')
                    
                row += 1
                for valor in fields['texto_saida'][idx]:
                    worksheet.write(row, column, valor)
                    row += 1
                row = init_row + 1
                column += 1
            
            last_keyword = keyword

        workbook.close()


    def estruturaDados(self):
        '''
            Processa os campos textuais, filtrando e organizando-os para
            prepará-los para a exportação. Os dados filtrados são atribuídos
            na variável texto_saida.
        '''
        self.processaDadosEntrada()
        self.filtraCampos()
        

    def detectaTabela(self):
        '''
            Ainda não está eficiente! Ajustar parametros de kernel, erosão e dilatação.
        '''
        arquivo = f'{DIR_IMAGEM}/3.jpg'

        img = cv2.imread(arquivo, 0)
        img = img[794:1284, 117:766]
        plot1 = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Aplica inversão de imagem
        thresh,img_bin = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
        img_bin = 255-img_bin
        plotting = plt.imshow(img_bin,cmap='gray')
        plt.title("Inverted Image with global thresh holding")

        # Aplica inversão com otsu
        img_bin1 = 255-img
        thresh1,img_bin1_otsu = cv2.threshold(img_bin1,128,255,cv2.THRESH_OTSU)
        plotting = plt.imshow(img_bin1_otsu,cmap='gray')
        plt.title("Inverted Image with otsu thresh holding")

        # Aplica inversão com os dois algoritmos
        img_bin2 = 255-img
        thresh1,img_bin_otsu = cv2.threshold(img_bin2,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        plotting = plt.imshow(img_bin_otsu,cmap='gray')
        plt.title("Inverted Image with otsu thresh holding")

        # Define comprimento do kernel
        kernel_length = np.array(img).shape[1]//300

        # Kernel vertical
        vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        # Kernel horizontal
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # A kernel of (3 X 3) ones.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))# Morphological operation to detect verticle lines from an image
        # Sentido Vertical
        # Aplica erosão para remoção de ruído
        img_temp1 = cv2.erode(img_bin_otsu, vert_kernel, iterations=5)
        # Aplica dilatação para unir partes
        verticle_lines_img = cv2.dilate(img_temp1, vert_kernel, iterations=30)
        # cv2.imwrite("verticle_lines.jpg",verticle_lines_img)# Morphological operation to detect horizontal lines from an image
        # Sentido Horizontal
        img_temp2 = cv2.erode(img_bin_otsu, hor_kernel, iterations=5)
        horizontal_lines_img = cv2.dilate(img_temp2, hor_kernel, iterations=30)
        # cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)# Weighting parameters, this will decide the quantity of an image to be added to make a new image.

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        fig.suptitle('Aplicação dos kernels horizontais e verticais')
        ax1.imshow(img_temp2, cmap = 'gray')
        ax1.set_title('Image after erosion with horizontal kernel'), plt.xticks([]), plt.yticks([])
        ax2.imshow(horizontal_lines_img, cmap = 'gray')
        ax2.set_title('Image after dilation with horizontal kernel'), plt.xticks([]), plt.yticks([])

        ax3.imshow(img_temp1, cmap = 'gray')
        ax3.set_title('Image after erosion with vertical kernel'), plt.xticks([]), plt.yticks([])
        ax4.imshow(verticle_lines_img, cmap = 'gray')
        ax4.set_title('Image after dilation with vertical kernel'), plt.xticks([]), plt.yticks([])
        plt.show()

        # Faz a soma das duas imagens, vertical e horizontal
        alpha = 0.5
        beta = 1.0 - alpha
        
        img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
        (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)# For Debugging
        plot1 = plt.imshow(cv2.cvtColor(img_final_bin, cv2.COLOR_BGR2RGB))
        plt.title("Image with vertical and horizontal lines")
        plt.show()
        # cv2.imwrite("img_final_bin.jpg",img_final_bin)

        # Encontra os contornos
        contours, hierarchy = cv2.findContours(
            img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Ordena os contornos de cima para baixo
        reverse = False
        i = 1
        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in contours]
        (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),
            key=lambda b:b[1][i], reverse=reverse))
        
        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv2.boundingRect(c)# If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
            new_img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

        plot1 = plt.imshow(cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB))
        plt.title("Final Image Output")
        plt.show()



class FaturaGrupoA4(FaturaBase):
    def extrair(self, plotar_saida=False, salvar_saida=False):
        self.converteParaImagem()
        self.detectaCaixas(plotar=plotar_saida)
        self.extraiTextoDoDocumento(salvar_saida)
        self.estruturaDados()
        self.exportaParaExcel()



class FaturaGrupoA1(FaturaBase):
    def extrair(self):
        return f'Dados do grupo A1 extraídos do arquivo {self.nome_arquivo}'


class FaturaBaseDB(FaturaBase):

    def __init__(self, nome_arquivo_fatura: str, model: object):
        self.model = model
        super().__init__(nome_arquivo_fatura)


    def converteDadosParaDB(self):
        ...


    def salvaDadosNoDB(self):
        ...    
        

    def extrair(self, plotar_saida=False, salvar_saida=False):
        self.converteParaImagem()
        self.detectaCaixas(plotar=plotar_saida)
        self.extraiTextoDoDocumento(salvar_saida)
        self.estruturaDados()
        self.exportaParaExcel()