from flask_restful import Resource, Api, reqparse, abort
from models.post import Post
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import Blueprint, flash, redirect, url_for, abort as flask_abort
from flask_login import login_required, current_user

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

# Web route for deleting post
@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id and current_user.role != 'admin':
        flask_abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('dashboard'))

# Request parser
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, help='Title is required')
post_parser.add_argument('content', type=str, required=True, help='Content is required')
post_parser.add_argument('summary', type=str, required=False)
post_parser.add_argument('tags', type=str, required=False)
post_parser.add_argument('status', type=str, required=False, default='draft')

class PostListResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        posts = Post.query.filter_by(status='published').all()
        return {
            'posts': [post.to_dict() for post in posts],
            'total': len(posts)
        }, 200

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if 'publisher' not in claims.get('roles', []) and 'admin' not in claims.get('roles', []):
            abort(403, message='Insufficient permissions to create posts')

        args = post_parser.parse_args()

        post = Post(
            title=args['title'],
            content=args['content'],
            summary=args['summary'],
            tags=args['tags'],
            status=args['status'],
            author_id=current_user_id
        )

        db.session.add(post)
        db.session.commit()

        return {
            'message': 'Post created successfully',
            'post': post.to_dict(),
            'links': [
                {'rel': 'self', 'href': f'/api/posts/{post.id}'},
                {'rel': 'edit', 'href': f'/api/posts/{post.id}'},
                {'rel': 'delete', 'href': f'/api/posts/{post.id}'}
            ]
        }, 201

class PostResource(Resource):
    @jwt_required(optional=True)
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            abort(404, message='Post not found')

        post.views += 1
        db.session.commit()

        return {
            'post': post.to_dict(),
            'links': [
                {'rel': 'self', 'href': f'/api/posts/{post.id}'},
                {'rel': 'collection', 'href': '/api/posts'}
            ]
        }, 200

    @jwt_required()
    def put(self, post_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        post = Post.query.get(post_id)
        if not post:
            abort(404, message='Post not found')

        if post.author_id != current_user_id and 'admin' not in claims.get('roles', []):
            abort(403, message='Insufficient permissions to edit this post')

        args = post_parser.parse_args()

        post.title = args['title']
        post.content = args['content']
        post.summary = args['summary']
        post.tags = args['tags']
        post.status = args['status']

        db.session.commit()

        return {
            'message': 'Post updated successfully',
            'post': post.to_dict()
        }, 200

    @jwt_required()
    def delete(self, post_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        post = Post.query.get(post_id)
        if not post:
            abort(404, message='Post not found')

        if post.author_id != current_user_id and 'admin' not in claims.get('roles', []):
            abort(403, message='Insufficient permissions to delete this post')

        db.session.delete(post)
        db.session.commit()

        return {'message': 'Post deleted successfully'}, 200


def register_api(app):
    api = Api(app, prefix='/api')
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/posts/<int:post_id>')