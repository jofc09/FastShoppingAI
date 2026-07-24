
import unittest
# Aquí importaríamos las funciones desde app si estuvieran modularizadas
# Por ahora, definimos la lógica para validar el entorno de pruebas

def validar_acceso_rol(rol_seleccionado, seccion_objetivo):
    permisos = {
        "Comprador 🛒": ["Catalogo", "Carrito", "Perfil"],
        "Repartidor 🛵": ["Mapa", "Entregas", "Perfil"]
    }
    return seccion_objetivo in permisos.get(rol_seleccionado, [])

class TestFastShoppingLogic(unittest.TestCase):
    def test_acceso_comprador(self):
        self.assertTrue(validar_acceso_rol("Comprador 🛒", "Catalogo"))

    def test_acceso_repartidor(self):
        self.assertTrue(validar_acceso_rol("Repartidor 🛵", "Mapa"))

if __name__ == '__main__':
    unittest.main()
