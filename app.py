import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Artist, Album, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # setup cross origin
    CORS(app)

    # Setup home route
    @app.route('/')
    def welcome():
        return 'Welcome to music store.'

    """Albums Routes"""

    # Route for getting all albums
    @app.route('/albums')
    @requires_auth('get:albums')
    def get_albums(jwt):
        """Get all albums"""

        albums = Album.query.all()
        formatted_albums = [album.format() for album in albums]

        return jsonify({
            'success': True,
            'albums': formatted_albums
        }), 200

    # Route for getting a specific album
    @app.route('/albums/<int:id>')
    @requires_auth('get:albums')
    def get_album_by_id(jwt, id):
        album = Album.query.filter(Album.id == id).one_or_none()

        # return 404 if there is no album with album_id
        if album is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'album': album.format(),
            }), 200

    @app.route('/albums', methods=['POST'])
    @requires_auth('post:albums')
    def post_album(jwt):
        # Process request data
        data = request.get_json()
        title = data.get('title', None)
        year = data.get('year', None)
        artist = data.get('artist', None)

        # return 400 for empty title or year or artist
        if title is None or year is None or artist is None:
            abort(400)

        try:
            album = Album(title=title, year=year, artist=artist)
            album.insert()
            return jsonify({
                'success': True,
                'album': album.format()
            }), 201
        except Exception:
            abort(500)

    @app.route('/albums/<int:id>', methods=['PATCH'])
    @requires_auth('patch:albums')
    def patch_album(jwt, id):

        data = request.get_json()

        album = Album.query.filter(Album.id == id).one_or_none()

        if album is None:
            abort(404)

        try:

            if title in data:
                album.title = data.get('title')

            if year in data:
                album.year = data.get('year')

            if artist in data:
                album.artist = data.get('artist')

            album.update()
            return jsonify({
                'success': True,
                'album': album.format()
            }), 200
        except Exception:
            abort(500)

    @app.route('/albums/<int:id>', methods=['DELETE'])
    @requires_auth('delete:albums')
    def delete_album(jwt, id):
        album = Album.query.filter(Album.id == id).one_or_none()

        if album is None:
            abort(404)
        try:
            album.delete()
            return jsonify({
                'success': True,
                'deleted': id,
            })
        except Exception:
            db.session.rollback()
            abort(500)

    """Artists Routes"""

    @app.route('/artists')
    @requires_auth('get:artists')
    def get_artists(jwt):

        artists = Artist.query.all()
        formatted_artists = [artist.format() for artist in artists]

        return jsonify({
            'success': True,
            'artists': formatted_artists
        }), 200

    @app.route('/artists/<int:id>')
    @requires_auth('get:artists')
    def get_artist_by_id(jwt, id):
        artist = Artist.query.filter(Artist.id == id).one_or_none()

        if artist is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'artist': artist.format(),
            }), 200

    @app.route('/artists', methods=['POST'])
    @requires_auth('post:artists')
    def post_artist(jwt):
        data = request.get_json()
        name = data.get('name', None)

        artist = Artist(name=name)

        if name is None:
            abort(400)

        try:
            artist.insert()
            return jsonify({
                'success': True,
                'artist': artist.format()
            }), 201
        except Exception:
            abort(500)

    @app.route('/artists/<int:id>', methods=['PATCH'])
    @requires_auth('patch:artists')
    def patch_artist(jwt, id):
        data = request.get_json()

        artist = Artist.query.filter(Artist.id == id).one_or_none()

        if artist is None:
            abort(404)

        try:
            if name in data:
                artist.name = data.get('name')

            print(artist.name)

            artist.update()
            return jsonify({
                'success': True,
                'artist': artist.format()
            }), 200
        except Exception:
            abort(500)

    @app.route('/artists/<int:id>', methods=['DELETE'])
    @requires_auth('delete:artists')
    def delete_artist(jwt, id):
        artist = Artist.query.filter(Artist.id == id).one_or_none()

        if artist is None:
            abort(404)
        try:
            artist.delete()
            return jsonify({
                'success': True,
                'deleted': id,
            })
        except Exception:
            db.session.rollback()
            abort(500)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)