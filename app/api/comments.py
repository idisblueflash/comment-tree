from flask import jsonify, request
from flask_login import login_required

from . import api

from sqlalchemy import text
from app import db
from .errors import bad_request
from .forms import CommentForm
from ..models import Comment


@api.route('/comments/')
def get_comments():
    sql = text("""
    select node.id, node.left_index, node.message, node.user_id, users.username, node.timestamp, (count(parent.message) -1) as depth
    from comments as node, comments as parent
    join users on users.id = node.user_id
    where node.left_index between parent.left_index and parent.right_index
    group by node.message
    order by node.left_index
    """)
    with db.engine.connect() as connection:
        result = connection.execute(sql)
        comments = []
        for row in result:
            id, left_index, message, user_id, username, timestamp, depth = row
            comments.append(
                {'id': id, 'left_index': left_index, 'message': message, 'user_id': user_id, 'username': username,
                 'timestamp': timestamp, 'depth': depth})

    return jsonify({'comments': comments})


@api.route('/comments/post/', methods=['POST'])
@login_required
def post_comment():
    payload = request.json
    form = CommentForm(**payload, meta={'csrf': False})
    if not form.validate():
        return bad_request(form.errors)
    left_index = payload.get('left_index') or 1
    comment_count = len(Comment.query.all())
    sql_insert_root_message = f"""
    insert into comments(message, left_index, right_index, user_id, timestamp ) 
    values('root message', 1, 2, {payload['user_id']}, '{payload['timestamp']}');
    """

    sql_update_right_index = f"""
    update comments set right_index = right_index + 2 where right_index > {left_index};
    """
    sql_update_left_index = f"""
    update comments set left_index = left_index + 2 where left_index > {left_index};
    """
    sql_insert = f"""
    insert into comments(message, left_index, right_index, user_id, timestamp) 
    values('{payload['message']}', {left_index}+1, {left_index}+2, {payload['user_id']}, '{payload['timestamp']}');
    """
    with db.engine.connect() as connection:
        if not comment_count:
            connection.execute(sql_insert_root_message)
        connection.execute(sql_update_right_index)
        connection.execute(sql_update_left_index)
        result = connection.execute(sql_insert)
        comment = Comment.query.filter_by(id=result.lastrowid).first()
        return jsonify(comment.to_json())
