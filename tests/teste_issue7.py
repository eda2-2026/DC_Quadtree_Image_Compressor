import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from image_utils import psnr

def teste_psnr():
    print("Iniciando Testes da Issue #7...")
    img_original = np.array([[100, 100], [100, 100]], dtype=np.uint8)
    
    # ── Teste PSNR (Imagens Idênticas) ────────────────────────
    img_identica = np.array([[100, 100], [100, 100]], dtype=np.uint8)
    psnr_identico = psnr(img_original, img_identica)
    assert psnr_identico == float('inf'), "PSNR de imagens idênticas deve ser infinito."
    print("PSNR Imagens Idênticas OK")
    print(f"Valor retornado: {psnr_identico}")
    
    # ── Teste PSNR (Imagens com Ruído/Diferentes) ─────────────
    img_diferente = np.array([[50, 50], [50, 50]], dtype=np.uint8)
    valor_psnr = psnr(img_original, img_diferente)
    
    assert isinstance(valor_psnr, float), "PSNR deve retornar um float"
    assert valor_psnr < float('inf'), "O valor de imagens diferentes não deve ser infinito"
    assert valor_psnr > 0, "O valor de cálculo tem de ser positivo"
    
    print("PSNR Imagens Diferentes OK")
    print(f"Valor PSNR calculado: {valor_psnr:.2f} dB")
    
    print("\n Issue #7 concluída com sucesso!")

if __name__ == "__main__":
    teste_psnr()
