from flask import jsonify, render_template, request

def register_error_handlers(app):
    
    @app.errorhandler(400)
    def bad_request(error):
        if request.is_json:
            return jsonify({
                'error': 'Bad Request',
                'message': str(error.description)
            }), 400
        return render_template('error.html', error='Bad Request', message=str(error.description)), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_json:
            return jsonify({
                'error': 'Unauthorized',
                'message': str(error.description)
            }), 401
        return render_template('error.html', error='Unauthorized', message='Please log in to access this page'), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        if request.is_json:
            return jsonify({
                'error': 'Forbidden',
                'message': str(error.description)
            }), 403
        return render_template('error.html', error='Forbidden', message='You do not have permission to access this page'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        if request.is_json:
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found'
            }), 404
        return render_template('error.html', error='Page Not Found', message='The page you are looking for does not exist'), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        if request.is_json:
            return jsonify({
                'error': 'Unprocessable Entity',
                'message': str(error.description)
            }), 422
        return render_template('error.html', error='Unprocessable Entity', message=str(error.description)), 422
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.is_json:
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An internal server error occurred'
            }), 500
        return render_template('error.html', error='Internal Server Error', message='Something went wrong on our end'), 500