from openpyxl import Workbook
from datetime import date
from datetime import datetime
import os

class Excell :

    DIRETORIO_SALVAR = "C:/FRETES"

    def __init__(self) :
        self.wb = Workbook()
        self.wb.remove(self.wb.active)

    def getWb(self):
        return self.wb
    
    def salvaArquivoMaquina(self, wb):
        hoje = date.today()
        hora = datetime.now()
        data_dia = hoje.strftime("%d-%m-%Y")
        hora_exatada = hora.strftime("%H%M%S")
        nome_arquivo = "frete_dia_" + data_dia + "_"+ hora_exatada + ".xlsx"
        caminho_completo = os.path.join(self.DIRETORIO_SALVAR, nome_arquivo)
        os.makedirs(self.DIRETORIO_SALVAR, exist_ok=True)
        wb.save(caminho_completo)