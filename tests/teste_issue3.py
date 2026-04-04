import numpy as np
from image_utils import cor_media, variancia

def teste_cor_media_variancia():
    # Matriz 4x4 preenchida com valores nulos
    pixels = np.zeros((4, 4), dtype=np.uint8)
    
    # Preencheremos o bloco de interesse x=1, y=1, largura=2, altura=2
    # Elementos do bloco: [10, 20],
    #                     [30, 40]
    pixels[1, 1] = 10
    pixels[1, 2] = 20
    pixels[2, 1] = 30
    pixels[2, 2] = 40
    
    # Média: (10+20+30+40)/4 = 100/4 = 25
    media_calc = cor_media(pixels, 1, 1, 2, 2)
    assert media_calc == 25, f"Média falhou, retornou {media_calc} invés de 25"
    assert isinstance(media_calc, int), "A média deve retornar um tipo inteiro."
    
    # Variância: mean((x - 25)^2) 
    # (15^2 + 5^2 + 5^2 + 15^2) / 4 = (225 + 25 + 25 + 225) / 4 = 125.0
    var_calc = variancia(pixels, 1, 1, 2, 2)
    assert abs(var_calc - 125.0) < 1e-5, f"Variância falhou, retornou {var_calc} invés de 125.0"
    assert isinstance(var_calc, float), "A variância deve ser um tipo float."
    
    print("Issue #3 (cor_media, variancia) concluída com sucesso!")

if __name__ == "__main__":
    teste_cor_media_variancia()
