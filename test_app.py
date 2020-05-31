import os
import unittest
import json

from app import create_app
from models import setup_db, Album, Artist

# Tokens are formatted as such to limit length on a line
CUSTOMER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllXYWdaWFItXzBFdlNyM280RGlLZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlY2FjNjRlZWU1NmM0MGM2ZDg1N2ZlNyIsImF1ZCI6Im11c2ljc3RvcmUiLCJpYXQiOjE1OTA5NDYzODcsImV4cCI6MTU5MTAzMjc4NywiYXpwIjoidTQzTEZ5Sk1EMVNOWlBPMHZBenE1M3gwT2Z5aGdtb24iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphbGJ1bXMiLCJnZXQ6YXJ0aXN0cyJdfQ.BS-42jRG4RwEWstgJyKaKXI7ye6cCiuenglyyrO_NvVMGTEa_IZ3VbhHkr1zYQdoO11kIbfmrkVSoUH7lhB9d830W68hJEFEaNvEWhN0ekzaXYS0DlgPjdgKynCL33hWhtKPI11LlyC5GgB4SG29wZfahznwW69bt7MmNHISu6Q-PIw_TXk1HrovrjsUuYf1-H3OGNU6T_r1MaMOvUKx_RXJfpJjDMv7r27HrWe_-gigszPtP6qG5Qc4xAnxDDT67JNWBql3AEjP33pfwDD17JRL4wxmoCBeIulrGKpCqlpxgu0g63xdLw2FAjKYxQ_FsiMH32ZKFIWmUD9ENKqrFw')

MANAGER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllXYWdaWFItXzBFdlNyM280RGlLZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlY2FjNWM3OTJkY2U4MGM2ZjE4NDFiOSIsImF1ZCI6Im11c2ljc3RvcmUiLCJpYXQiOjE1OTA5NDI3MzIsImV4cCI6MTU5MTAyOTEzMiwiYXpwIjoidTQzTEZ5Sk1EMVNOWlBPMHZBenE1M3gwT2Z5aGdtb24iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphbGJ1bXMiLCJkZWxldGU6YXJ0aXN0cyIsImdldDphbGJ1bXMiLCJnZXQ6YXJ0aXN0cyIsInBhdGNoOmFsYnVtcyIsInBhdGNoOmFydGlzdHMiLCJwb3N0OmFsYnVtcyIsInBvc3Q6YXJ0aXN0cyJdfQ.C06D8i4Shv4upj6OUJ0LnHElk57Ce0JdwOFUH5tv45wp_pF0cXjMhCEM4QpoOpsaJJ5DPHwkAuovDjuJ7O0kWXFgwoava8yT-aC4d1X-615IjCx7EhUhmlH6KmldbgdJSOcj-qjbm4M4Nr71D-9Rsv32GbgXdSV0qC-ZDsKX_-h7xSj4Y8VGROpHtan5kByoAbTxpQTE0-ZadrHCtYZoFYjGKYe7ZLp9dhu2NCqgla9J1yJn1KmnSIa7s06G_2WKoV-1P5x_awRlkHH5xTZ23slMEaQhYgpyCQoEhUUAOty8S3lzKktHZ1jXfMTkngYORQ4JajbFSF_GtKgQB9iexg')


class MusicStoreTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        self.test_album = {
            'title': 'Discovery',
            'year': '2001',
            'artist': 'Daft Punk'
        }
        self.test_artist = {
            'name': 'Daft Punk'
        }

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  Tests that you can get all albums
    def test_get_albums(self):
        response = self.client().get(
            '/albums',
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['albums'])

    # Test to get a specific album
    def test_get_album_by_id(self):
        response = self.client().get(
            '/albums/1',
            headers={"Authorization": "Bearer " + CUSTOMER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['album'])
        self.assertEqual(data['album']['title'], 'Abbey Road')

    # tests for an invalid id to get a specific album
    def test_404_get_album_by_id(self):
        response = self.client().get(
            '/albums/100',
            headers={"Authorization": "Bearer " + CUSTOMER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a new album
    def test_post_album(self):
        response = self.client().post(
            '/albums',
            json=self.test_album,
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['album'])
        self.assertEqual(data['album']['title'], 'Discovery')
        self.assertEqual(data['album']['year'], '2001')
        self.assertEqual(data['album']['artist'], 'Daft Punk')

    # Test to create an album if no data is sent
    def test_400_post_album(self):
        response = self.client().post(
            '/albums',
            json={},
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for creating an album
    def test_401_post_album_unauthorized(self):
        response = self.client().post(
            '/albums',
            json=self.test_album,
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to update an album
    def test_patch_album(self):
        response = self.client().patch(
            '/albums/1',
            json={'title': 'Rubber Soul', 'year': '1965'},
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['album'])
        self.assertEqual(data['album']['title'], 'Rubber Soul')
        self.assertEqual(data['album']['year'], '1965')
        self.assertEqual(data['album']['artist'], 'The Beatles')

    # Test that 404 if album_id is incorrect
    def test_404_patch_album(self):
        response = self.client().patch(
            '/albums/100',
            json={},
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # tests RBAC for updating an album
    def test_401_patch_album_unauthorized(self):
        response = self.client().patch(
            '/albums/1',
            json=self.test_album,
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests to delete an album
    def test_delete_album(self):
        response = self.client().delete(
            '/albums/2',
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '2')

    # tests RBAC for deleting an album
    def test_401_delete_album(self):
        response = self.client().delete(
            '/albums/2',
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to delete a specific album
    def test_404_delete_album(self):
        response = self.client().delete(
            '/albums/100',
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    #  Tests that you can get all artists
    def test_get_all_artists(self):
        response = self.client().get(
            '/artists',
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artists'])

    # Test to get a specific artist
    def test_get_artist_by_id(self):
        response = self.client().get(
            '/artists/1',
            headers={"Authorization": "Bearer " + CUSTOMER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artist'])
        self.assertEqual(data['artist']['name'], 'The Beatles')

    # tests for an invalid id to get a specific artist
    def test_404_get_artist_by_id(self):
        response = self.client().get(
            '/artists/100',
            headers={"Authorization": "Bearer " + CUSTOMER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create an artist
    def test_post_artist(self):
        response = self.client().post(
            '/artists',
            json=self.test_artist,
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['artist']['name'], 'Daft Punk')

    # Test to create an artist if no data is sent
    def test_400_post_artist(self):
        response = self.client().post(
            '/artists',
            json={},
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for creating an artist
    def test_401_post_artist_unauthorized(self):
        response = self.client().post(
            '/artists',
            json=self.test_artist,
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update an artist
    def test_patch_artist(self):
        response = self.client().patch(
            '/artists/1',
            json={'name': 'Beatles'},
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['artist']['name'], 'Beatles')

    # tests RBAC for updating an artist
    def test_401_patch_artist_unauthorized(self):
        response = self.client().patch(
            '/artists/1',
            json=self.test_artist,
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific artist
    def test_404_patch_artist(self):
        response = self.client().patch(
            '/artist/100',
            json={'name': 'Adele'},
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests to delete an artist
    def test_delete_artist(self):
        response = self.client().delete(
            '/artists/6',
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '6')

    # tests RBAC for deleting an artist
    def test_401_delete_artist(self):
        response = self.client().delete(
            '/artists/5',
            headers={'Authorization': f'Bearer {CUSTOMER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to delete a specific artist
    def test_404_delete_artist(self):
        response = self.client().delete(
            '/artists/100',
            headers={'Authorization': f'Bearer {MANAGER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
