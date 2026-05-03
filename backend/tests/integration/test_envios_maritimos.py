"""
Tests de integración — Envíos Marítimos.

Espejo de los tests terrestres pero con las reglas marítimas:
  - Número de flota formato AAA1234A
  - Descuento del 3% (no 5%)
  - Puerto en lugar de bodega
"""
import pytest


class TestCrearEnvioMaritimo:

    def test_crea_envio_exitosamente(self, client, usuario_token, datos_semilla):
        response = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": 3,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "MAR1234567",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["numero_flota"] == "ABC1234D"
        assert data["numero_guia"] == "MAR1234567"
        assert data["estado"] == "registrado"
        assert float(data["descuento"]) == 0.0  # 3 <= 10, sin descuento

    def test_aplica_descuento_3_porciento_con_cantidad_mayor_a_10(
        self, client, usuario_token, datos_semilla
    ):
        """Con 12 unidades a $850,000 c/u, el descuento debe ser $306,000."""
        response = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": 12,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "MAR0000001",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert float(data["subtotal"]) == 10_200_000.00    # 12 × 850,000
        assert float(data["descuento"]) == 306_000.00      # 3% de 10,200,000
        assert float(data["total"]) == 9_894_000.00

    def test_descuento_maritimo_menor_que_terrestre(
        self, client, usuario_token, datos_semilla
    ):
        """
        Con la misma cantidad (>10), el descuento marítimo (3%)
        debe ser menor que el terrestre (5%).
        """
        # Crear producto terrestre con mismo precio que marítimo para comparar
        prod_terre_igual_precio = client.post(
            "/api/v1/productos/",
            headers=usuario_token["headers"],
            json={
                "tipo_producto": "Producto Igual Precio Terrestre",
                "precio_unitario": 850000.00,
                "tipo_logistica": "terrestre",
            },
        ).json()

        cantidad = 12

        resp_terre = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": prod_terre_igual_precio["id"],
                "cantidad_producto": cantidad,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "COMPA00001",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        ).json()

        resp_mari = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": cantidad,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "COMPA00002",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        ).json()

        assert float(resp_mari["descuento"]) < float(resp_terre["descuento"])

    def test_sin_descuento_cantidad_exactamente_10(
        self, client, usuario_token, datos_semilla
    ):
        response = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": 10,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "MAR0000002",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        )
        assert response.status_code == 201
        assert float(response.json()["descuento"]) == 0.0

    @pytest.mark.parametrize("flota_invalida", [
        "AB1234D",     # Solo 2 letras iniciales
        "ABCD1234D",   # 4 letras iniciales
        "ABC123D",     # Solo 3 números
        "ABC12345D",   # 5 números
        "ABC1234",     # Falta letra final
    ])
    def test_numero_flota_invalido_retorna_422(
        self, client, usuario_token, datos_semilla, flota_invalida
    ):
        response = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": 5,
                "fecha_entrega": "2026-12-31",
                "numero_flota": flota_invalida,
                "numero_guia": "MAR9999999",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        )
        assert response.status_code == 422

    def test_producto_terrestre_en_envio_maritimo_retorna_400(
        self, client, usuario_token, datos_semilla
    ):
        """No se puede usar un producto terrestre en un envío marítimo."""
        response = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],  # ← terrestre
                "cantidad_producto": 5,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "MAR9999998",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        )
        assert response.status_code == 400
        assert "marítim" in response.json()["detail"].lower()

    def test_numero_guia_duplicado_retorna_400(self, client, usuario_token, datos_semilla):
        """La unicidad del número de guía aplica también entre marítimos."""
        payload = {
            "cliente_id": usuario_token["cliente_id"],
            "producto_id": datos_semilla["producto_maritimo"]["id"],
            "cantidad_producto": 2,
            "fecha_entrega": "2026-12-31",
            "numero_flota": "ABC1234D",
            "numero_guia": "GUIAUNI001",
            "puerto_id": datos_semilla["puerto"]["id"],
        }
        client.post("/api/v1/envios-maritimos/", headers=usuario_token["headers"], json=payload)

        response = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={**payload, "numero_flota": "XYZ9999Z"},
        )
        assert response.status_code == 400

    def test_sin_autenticacion_retorna_401_o_403(self, client):
        response = client.post("/api/v1/envios-maritimos/", json={})
        assert response.status_code in (401, 403)


class TestListarEnviosMaritimos:

    def test_lista_vacia_sin_envios(self, client, usuario_token):
        response = client.get(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_lista_incluye_envio_creado(self, client, usuario_token, datos_semilla):
        client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": 1,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "LISTAM0001",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        )
        response = client.get(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1


class TestCambiarEstadoEnvioMaritimo:

    def test_todos_los_estados_validos(self, client, usuario_token, datos_semilla):
        """Verifica que todos los estados válidos pueden aplicarse."""
        envio = client.post(
            "/api/v1/envios-maritimos/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],
                "cantidad_producto": 2,
                "fecha_entrega": "2026-12-31",
                "numero_flota": "ABC1234D",
                "numero_guia": "ESTM000001",
                "puerto_id": datos_semilla["puerto"]["id"],
            },
        ).json()

        for estado in ["en_transito", "entregado"]:
            response = client.patch(
                f"/api/v1/envios-maritimos/{envio['id']}/estado",
                headers=usuario_token["headers"],
                json={"estado": estado},
            )
            assert response.status_code == 200
            assert response.json()["estado"] == estado

    def test_envio_inexistente_retorna_404(self, client, usuario_token):
        response = client.patch(
            "/api/v1/envios-maritimos/99999/estado",
            headers=usuario_token["headers"],
            json={"estado": "entregado"},
        )
        assert response.status_code == 404