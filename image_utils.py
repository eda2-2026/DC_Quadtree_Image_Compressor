from PIL import Image
import numpy as np

def carregar(caminho):
    """
    Carrega uma imagem a partir do caminho, converte para escala de cinza
    e retorna como um array NumPy 2D (uint8).
    """
    # Abre a imagem e converte para 'L' (escala de cinza, 8-bit pixels)
    img = Image.open(caminho).convert('L')
    
    # Converte a imagem do Pillow para um array NumPy
    pixels = np.array(img, dtype=np.uint8)
    
    return pixels

def salvar(pixels, caminho):
    """
    Recebe um array NumPy 2D correspondente a uma imagem em escala de cinza
    e a salva no caminho especificado.
    """
    # Se garantir que está no tipo correto 
    if pixels.dtype != np.uint8:
        pixels = pixels.astype(np.uint8)
        
    # Cria uma imagem a partir do array e salva
    img = Image.fromarray(pixels, mode='L')
    img.save(caminho)

def psnr(original, comprimida):
    """
    Calcula a métrica Peak Signal-to-Noise Ratio (PSNR) entre a imagem 
    original e a comprimida. Quanto maior o PSNR, mais parecida é com a original.
    """
    # Converte os arrays para float64 para evitar overflow na subtração
    orig = original.astype(np.float64)
    comp = comprimida.astype(np.float64)
    
    # Calcula o Erro Quadrático Médio (MSE)
    mse = np.mean((orig - comp) ** 2)
    
    # Se o MSE for zero, as imagens são idênticas
    if mse == 0:
        return float('inf')
        
    max_pixel = 255.0
    # Calcula o PSNR usando a fórmula e a base log10 do numpy
    return 10 * np.log10((max_pixel ** 2) / mse)
