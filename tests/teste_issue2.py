import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from image_utils import carregar, salvar

def teste_carregar_salvar():
    print("Iniciando Testes da Issue #2...")
    caminho_teste = "img_teste_issue2.png"
    
    # ── Teste Salvar ──────────────────────────────────────────
    pixels_originais = np.zeros((100, 100), dtype=np.uint8)
    pixels_originais[25:75, 25:75] = 120  # Adiciona um quadrado cinza no meio
    
    salvar(pixels_originais, caminho_teste)
    assert os.path.exists(caminho_teste), "Arquivo não foi salvo corretamente."
    print("Salvar OK")
    
    # ── Teste Carregar ────────────────────────────────────────
    pixels_carregados = carregar(caminho_teste)
    assert type(pixels_carregados) is np.ndarray, "O retorno de carregar deve ser um numpy array."
    assert pixels_carregados.dtype == np.uint8, "O array deve ser do tipo uint8."
    assert pixels_carregados.shape == (100, 100), "A imagem carregada deve ter a mesma dimensão."
    print("Carregar OK")
    
    # ── Teste Igualdade de Dados ──────────────────────────────
    assert np.array_equal(pixels_originais, pixels_carregados), "Os pixels carregados devem ser os mesmos salvos."
    print("Validação de Dados OK")
    
    # Limpar o arquivo de teste temporário
    os.remove(caminho_teste)
    print("\n Issue #2 concluída com sucesso!")

if __name__ == "__main__":
    teste_carregar_salvar()
