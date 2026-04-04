import os
import numpy as np
from image_utils import carregar, salvar

def teste_carregar_salvar():
    caminho_teste = "img_teste_issue2.png"
    
    # Criar um array dummy de 100x100
    pixels_originais = np.zeros((100, 100), dtype=np.uint8)
    pixels_originais[25:75, 25:75] = 120  # Adiciona um quadrado cinza no meio
    
    # Testar se a função salvar cria o arquivo
    salvar(pixels_originais, caminho_teste)
    assert os.path.exists(caminho_teste), "Arquivo não foi salvo corretamente."
    
    # Testar se a função carregar consegue ler como um numpy array
    pixels_carregados = carregar(caminho_teste)
    assert type(pixels_carregados) is np.ndarray, "O retorno de carregar deve ser um numpy array."
    assert pixels_carregados.dtype == np.uint8, "O array deve ser do tipo uint8."
    assert pixels_carregados.shape == (100, 100), "A imagem carregada deve ter a mesma dimensão."
    
    # Assegurar que os dados se mantiveram
    assert np.array_equal(pixels_originais, pixels_carregados), "Os pixels carregados devem ser os mesmos salvos."
    
    # Limpar o arquivo de teste temporário
    os.remove(caminho_teste)
    print("Issue #2 (carregar, salvar) concluída com sucesso!")

if __name__ == "__main__":
    teste_carregar_salvar()
