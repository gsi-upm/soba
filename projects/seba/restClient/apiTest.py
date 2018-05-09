from unittest import TestCase
import json, requests
from jsonschema import validate
import socket
import unittest


ipServer = socket.gethostbyname(socket.gethostname())


URLBASE = "http://127.0.1.1:10000"
URISOBA = "/api/soba/v1/occupants"
URISEBA = "/api/seba/v1/occupants"
URIFIRE = "/api/seba/v1/fire"


class APITest(TestCase):

    def test_general_gets(self, *args, **kwargs):

    #/api/soba/v1/occupants
        print(str('Testing {}').format('/api/soba/v1/occupants'))

        template = {
            "type": "object",
            "properties": {
                "occupants": {
                    "type": "array"
                    }
            }
        }

        for i in range(2):
            url = URLBASE + URISOBA
            data = requests.get(url)
            datajson = data.json()
            print("Response: ", datajson)
            validate(datajson, template)

    #/api/soba/v1/occupants/movements
        print(str('Testing {}').format('/api/soba/v1/occupants/movements'))

        template = {
            "type": "object",
            "properties": {
                "orientation": {
                    "type": "string"
                    },
                "speed": {
                    "type": "number"
                    }
            }
        }

        for i in range(2):
            url = URLBASE + URISOBA + "/movements"
            data = requests.get(url)
            datajson = data.json()
            print("Response: ", datajson)
            for m in datajson:
                validate(m, template)

if __name__ == "__main__":
      unittest.main()