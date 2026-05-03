"""
Tests de integración — Envíos Terrestres.

Prueba el flujo completo incluyendo:
  - Creación con validaciones de formato
  - Cálculo de descuentos por volumen
  - Unicidad del número de guía
  - Cambio de estado
  - Protección JWT
"""
import pytest


class TestCrearEnvioTerrestre:

    def test_crea_envio_exitosamente(self, client, usuario_token, datos_semilla):
        """Creación con datos válidos retorna 201 y el envío completo."""
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 5,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "TER1234567",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["placa"] == "ABC123"
        assert data["numero_guia"] == "TER1234567"
        assert data["estado"] == "registrado"
        assert data["cantidad_producto"] == 5
        assert float(data["descuento"]) == 0.0   # sin descuento (5 <= 10)

    def test_aplica_descuento_5_porciento_con_cantidad_mayor_a_10(
        self, client, usuario_token, datos_semilla
    ):
        """Con 15 unidades a $50,000 c/u, el descuento debe ser $37,500."""
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 15,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "TER0000001",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert float(data["subtotal"]) == 750_000.00    # 15 × 50,000
        assert float(data["descuento"]) == 37_500.00    # 5% de 750,000
        assert float(data["total"]) == 712_500.00       # subtotal - descuento

    def test_sin_descuento_con_cantidad_exactamente_10(
        self, client, usuario_token, datos_semilla
    ):
        """El umbral es estrictamente > 10. Con 10 no debe haber descuento."""
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 10,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "TER0000002",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )
        assert response.status_code == 201
        assert float(response.json()["descuento"]) == 0.0

    def test_numero_guia_duplicado_retorna_400(self, client, usuario_token, datos_semilla):
        """El número de guía debe ser único globalmente."""
        payload = {
            "cliente_id": usuario_token["cliente_id"],
            "producto_id": datos_semilla["producto_terrestre"]["id"],
            "cantidad_producto": 3,
            "fecha_entrega": "2026-12-31",
            "placa": "ABC123",
            "numero_guia": "GUIAUNICA1",
            "bodega_id": datos_semilla["bodega"]["id"],
        }
        client.post("/api/v1/envios-terrestres/", headers=usuario_token["headers"], json=payload)

        # Segundo envío con la misma guía
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={**payload, "placa": "XYZ999"},
        )
        assert response.status_code == 400
        assert "guía" in response.json()["detail"].lower()

    @pytest.mark.parametrize("placa_invalida", [
        "AB123",     # Faltan letras
        "ABCD123",   # Demasiadas letras
        "ABC12",     # Faltan números
        "123ABC",    # Formato invertido
        "abc 123",   # Espacio interno
    ])
    def test_placa_invalida_retorna_422(
        self, client, usuario_token, datos_semilla, placa_invalida
    ):
        """Placas con formato inválido deben retornar 422 (Pydantic)."""
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 5,
                "fecha_entrega": "2026-12-31",
                "placa": placa_invalida,
                "numero_guia": "TER9999999",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )
        assert response.status_code == 422

    def test_cantidad_cero_retorna_422(self, client, usuario_token, datos_semilla):
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 0,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "TER9999998",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )
        assert response.status_code == 422

    def test_producto_maritimo_en_envio_terrestre_retorna_400(
        self, client, usuario_token, datos_semilla
    ):
        """No se puede usar un producto marítimo en un envío terrestre."""
        response = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_maritimo"]["id"],  # ← marítimo
                "cantidad_producto": 5,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "TER9999997",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )
        assert response.status_code == 400
        assert "terrestre" in response.json()["detail"].lower()

    def test_sin_autenticacion_retorna_401_o_403(self, client, datos_semilla):
        response = client.post("/api/v1/envios-terrestres/", json={})
        assert response.status_code in (401, 403)


class TestListarEnviosTerrestres:

    def test_lista_envios_del_usuario(self, client, usuario_token, datos_semilla):
        """Lista retorna los envíos creados."""
        # Crear un envío primero
        client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 2,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "LISTA00001",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        )

        response = client.get(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
        )
        assert response.status_code == 200
        envios = response.json()
        assert isinstance(envios, list)
        assert len(envios) >= 1

    def test_lista_vacia_sin_envios(self, client, usuario_token):
        response = client.get(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
        )
        assert response.status_code == 200
        assert response.json() == []


class TestCambiarEstadoEnvioTerrestre:

    def test_cambio_estado_exitoso(self, client, usuario_token, datos_semilla):
        """El estado de un envío puede actualizarse."""
        # Crear envío
        envio = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 3,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "ESTADO0001",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        ).json()

        # Cambiar estado
        response = client.patch(
            f"/api/v1/envios-terrestres/{envio['id']}/estado",
            headers=usuario_token["headers"],
            json={"estado": "en_transito"},
        )
        assert response.status_code == 200
        assert response.json()["estado"] == "en_transito"

    def test_estado_invalido_retorna_422(self, client, usuario_token, datos_semilla):
        """Un estado que no existe en el Enum retorna 422."""
        envio = client.post(
            "/api/v1/envios-terrestres/",
            headers=usuario_token["headers"],
            json={
                "cliente_id": usuario_token["cliente_id"],
                "producto_id": datos_semilla["producto_terrestre"]["id"],
                "cantidad_producto": 1,
                "fecha_entrega": "2026-12-31",
                "placa": "ABC123",
                "numero_guia": "ESTADO0002",
                "bodega_id": datos_semilla["bodega"]["id"],
            },
        ).json()

        response = client.patch(
            f"/api/v1/envios-terrestres/{envio['id']}/estado",
            headers=usuario_token["headers"],
            json={"estado": "estado_que_no_existe"},
        )
        assert response.status_code == 422

    def test_envio_inexistente_retorna_404(self, client, usuario_token):
        response = client.patch(
            "/api/v1/envios-terrestres/99999/estado",
            headers=usuario_token["headers"],
            json={"estado": "en_transito"},
        )
        assert response.status_code == 404