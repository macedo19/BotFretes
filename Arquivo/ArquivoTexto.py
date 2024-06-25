class ArquivoTexto:

    CAMINHO_ARQUIVO = 'C:\FRETES\Credenciais\credenciais.txt'

    def ler(self):
        arquivo = open(self.CAMINHO_ARQUIVO, 'r')
        info = arquivo.read()
        arquivo.close
        return info