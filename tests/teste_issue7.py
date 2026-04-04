import numpy as np
from image_utils import psnr

def teste_psnr():
    # Cria uma simulação de imagem original de 2x2
    img_original = np.array([[100, 100], [100, 100]], dtype=np.uint8)
    
    # Testa PSNR com a imagem idêntica
    img_identica = np.array([[100, 100], [100, 100]], dtype=np.uint8)
    assert psnr(img_original, img_identica) == float('inf'), "PSNR de imagens idênticas deve ser infinito."
    
    # Testa PSNR com uma imagem modificado/com ruído
    img_diferente = np.array([[50, 50], [50, 50]], dtype=np.uint8)
    valor_psnr = psnr(img_original, img_diferente)
    
    # A resposta deve ser float
    assert isinstance(valor_psnr, float), "PSNR deve retornar um float"
    assert valor_psnr < float('inf'), "O valor de imagens diferentes não deve ser infinito"
    assert valor_psnr > 0, "O valor de cálculo tem de ser positivo"
    
    print(f"PSNR calculado com diferença: {valor_psnr:.2f} dB")
    print("Issue #7 (psnr) concluída com sucesso!")

if __name__ == "__main__":
    teste_psnr()
