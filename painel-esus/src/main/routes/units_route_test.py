from unittest import mock
import pytest

from src.main.routes.units_route import units_bp, UnitsPath, units_list
from src.main.server.server import app

def test_units_list_error_handling():
    app.config["ENV"] = "test"
    with mock.patch("src.main.routes.units_route.request_adapter") as mock_adapter:
        mock_adapter.side_effect = Exception("Test Exception")
        with mock.patch("src.main.routes.units_route.extract_token") as mock_extract_token:
            mock_extract_token.return_value = "token"
            with app.test_client() as client:
                response = client.get(UnitsPath.root_path)
                assert response.status_code == 500
                assert b"Server Error" in response.data
                assert b"Test Exception" in response.data
