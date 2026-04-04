import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from image_utils import cor_media, variancia

def teste_cor_media_variancia():
    print("Iniciando Testes da Issue #3...")
    
    # Matriz 4x4 preenchida com valores nulos
    pixels = np.zeros((4, 4), dtype=np.uint8)
    
    # Preencheremos o bloco de interesse x=1, y=1, largura=2, altura=2
    pixels[1, 1] = 10
    pixels[1, 2] = 20
    pixels[2, 1] = 30
    pixels[2, 2] = 40
    
    # ── Teste Cor Média ───────────────────────────────────────
    media_calc = cor_media(pixels, 1, 1, 2, 2)
    assert media_calc == 25, f"Média falhou, retornou {media_calc} invés de 25"
    assert isinstance(media_calc, int), "A média deve retornar um tipo inteiro."
    print("Cor Média OK")
    print(f"Cor Média calculada: {media_calc}")
    
    # ── Teste Variância ───────────────────────────────────────
    var_calc = variancia(pixels, 1, 1, 2, 2)
    assert abs(var_calc - 125.0) < 1e-5, f"Variância falhou, retornou {var_calc} invés de 125.0"
    assert isinstance(var_calc, float), "A variância deve ser um tipo float."
    print("Variância OK")
    print(f"Variância calculada: {var_calc}")
    
    print("\n Issue #3 concluída com sucesso!")

if __name__ == "__main__":
    teste_cor_media_variancia()
