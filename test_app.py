
import unittest

def buscar_productos(catalogo, termino_busqueda, categoria=None):
    resultados = []
    termino = termino_busqueda.lower()
    for producto in catalogo:
        match_nombre = termino in producto['nombre'].lower()
        match_cat = categoria is None or producto['categoria'] == categoria
        if match_nombre and match_cat:
            resultados.append(producto)
    return resultados

class TestFastShoppingSearch(unittest.TestCase):
    def setUp(self):
        self.catalogo = [
            {'nombre': 'Manzana', 'categoria': 'Alimentos'},
            {'nombre': 'Leche', 'categoria': 'Alimentos'},
            {'nombre': 'Aspirina', 'categoria': 'Farmacia'}
        ]

    def test_busqueda_nombre(self):
        res = buscar_productos(self.catalogo, 'Manzana')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['nombre'], 'Manzana')

    def test_busqueda_categoria(self):
        res = buscar_productos(self.catalogo, '', categoria='Farmacia')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['categoria'], 'Farmacia')

if __name__ == '__main__':
    unittest.main()
