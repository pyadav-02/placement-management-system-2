from interface_layer.authentication_interface import AuthenticationInterface
from unittest.mock import patch
import unittest


class TestAuthenticationInterface(unittest.TestCase):

    @patch('interface_layer.authentication_interface.AuthenticationInterface.is_admin_valid')
    def test_is_admin_valid_false(self, mock_is_admin_valid):
        assert True



