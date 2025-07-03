from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.post import Post
from models.user import User
from forms.auth_forms import PostForm
from extensions import db

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

# ------------------------
# WEB ROUTES
# ------------------------

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            summary=form.summary.data,
            tags=form.tags.data,
            status=form.status.data,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_post.html', form=form)


@posts_bp.route('/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()
    return render_template('post_detail.html', post=post)


@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.summary.data
        post.tags = form.tags.data
        post.status = form.status.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    return render_template('edit_post.html', form=form, post=post)


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


@posts_bp.route('/all', methods=['GET'])
def all_posts():
    q = request.args.get('q', '').strip()
    tag = request.args.get('tag', '').strip()

    query = Post.query.filter_by(status='published')

    if q:
        query = query.filter(
            Post.title.ilike(f"%{q}%") | Post.content.ilike(f"%{q}%")
        )

    if tag:
        query = query.filter(Post.tags.ilike(f"%{tag}%"))

    posts = query.order_by(Post.created_at.desc()).all()

    # Get distinct tags (or categories) for dropdown
    tag_data = db.session.query(Post.tags).distinct().all()
    tags = [t[0] for t in tag_data if t[0]]

    return render_template('posts/all_posts.html', posts=posts, tags=tags)

# ------------------------
# API ROUTES
# ------------------------

@posts_bp.route('/api', methods=['POST'])
@jwt_required()
def create_post_api():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    if 'publisher' not in claims.get('roles', []) and 'admin' not in claims.get('roles', []):
        abort(403, 'Insufficient permissions')
    data = request.get_json()
    post = Post(
        title=data.get('title'),
        content=data.get('content'),
        summary=data.get('summary'),
        tags=data.get('tags'),
        status=data.get('status', 'draft'),
        author_id=current_user_id
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@posts_bp.route('/api', methods=['GET'])
@jwt_required(optional=True)
def get_posts_api():
    posts = Post.query.filter_by(status='published').all()
    return jsonify([post.to_dict() for post in posts]), 200


@posts_bp.route('/api/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post_api(post_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user_id and 'admin' not in claims.get('roles', []):
        abort(403, 'Insufficient permissions')
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.summary = data.get('summary', post.summary)
    post.tags = data.get('tags', post.tags)
    post.status = data.get('status', post.status)
    db.session.commit()
    return jsonify(post.to_dict()), 200


@posts_bp.route('/api/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post_api(post_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user_id and 'admin' not in claims.get('roles', []):
        abort(403, 'Insufficient permissions')
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200
