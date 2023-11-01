from datetime import datetime
from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from db_handler import execute_query
from config import login_manager

from models import User

app = Flask(__name__)
app.secret_key = 'webxemphimkey'

login_manager.init_app(app)

@app.route('/')
@app.route('/movie')
@login_required
def movie():
    select_query = "SELECT movie.id,movie.name_vn,movie.name_en,COALESCE(status.name, 'DefaultValue') AS status,COALESCE(publish_status.name, 'DefaultValue') AS publish_status,COALESCE(lang.name, 'DefaultValue') AS lang,COALESCE(nation.name, 'DefaultValue') AS nation,movie.duration,COALESCE(sub_type.name, 'DefaultValue') AS sub_type,movie.movie_year,movie.source,movie.thumbnail,movie.created_at,movie.categories,movie.actors,COALESCE(series.name, 'DefaultValue') AS series FROM movie LEFT JOIN status ON movie.status = status.id LEFT JOIN publish_status ON movie.publish_status = publish_status.id LEFT JOIN lang ON movie.lang = lang.id LEFT JOIN nation ON movie.nation = nation.id LEFT JOIN sub_type ON movie.sub_type = sub_type.id LEFT JOIN series ON movie.series = series.id"
    movies = execute_query(select_query)
    select_query = "SELECT id,name FROM status"
    statuses = execute_query(select_query)
    select_query = "SELECT id,name FROM publish_status"
    publish_statuses = execute_query(select_query)
    select_query = "SELECT id,name FROM lang"
    langs = execute_query(select_query)
    select_query = "SELECT id,name FROM nation"
    nations = execute_query(select_query)
    select_query = "SELECT id,name FROM sub_type"
    sub_types = execute_query(select_query)
    select_query = "SELECT id,name FROM category"
    categories = execute_query(select_query)
    select_query = "SELECT id,name FROM actor"
    actors = execute_query(select_query)
    select_query = "SELECT id,name FROM series"
    serieses = execute_query(select_query)
    
    return render_template('movie.html', movies=movies, statuses=statuses,publish_statuses=publish_statuses,langs=langs,nations=nations,sub_types=sub_types, categories=categories, actors=actors,serieses=serieses)


@app.route('/series')
@login_required
def series():
    select_query = "SELECT id, name, created_at FROM series LIMIT 18446744073709551615 OFFSET 2;"
    serieses = execute_query(select_query)
    return render_template('series.html', serieses=serieses)

@app.route('/category')
@login_required
def category():
    select_query = "SELECT id, name, created_at FROM category"
    categories = execute_query(select_query)
    return render_template('category.html', categories=categories)

@app.route('/actor')
@login_required
def actor():
    select_query = "SELECT id, name, created_at FROM actor"
    actors = execute_query(select_query)
    return render_template('actor.html', actors=actors)

@app.route('/lang')
@login_required
def lang():
    select_query = "SELECT id, name, created_at FROM lang"
    langs = execute_query(select_query)
    return render_template('lang.html', langs=langs)

@app.route('/nation')
@login_required
def nation():
    select_query = "SELECT id, name, created_at FROM nation"
    nations = execute_query(select_query)
    return render_template('nation.html', nations=nations)

@app.route('/status')
@login_required
def status():
    select_query = "SELECT id, name, created_at FROM status"
    statuses = execute_query(select_query)
    return render_template('status.html', statuses=statuses)

@app.route('/publish-status')
@login_required
def publish_status():
    select_query = "SELECT id, name, created_at FROM publish_status"
    publish_statuses = execute_query(select_query)
    return render_template('publishstatus.html', publish_statuses=publish_statuses)

@app.route('/sub-type')
@login_required
def sub_type():
    select_query = "SELECT id, name, created_at FROM sub_type"
    sub_types = execute_query(select_query)
    return render_template('subtype.html', sub_types=sub_types)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('movie'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Implement your authentication logic here (e.g., check_credentials function)
        if check_credentials(username, password):
            return redirect(url_for('movie'))  # Redirect to the homepage after successful login

    return render_template('login.html')

def check_credentials(username, password):
    select_query = f"SELECT username, password FROM user WHERE username = '{username}'"
    user_data = execute_query(select_query)

    # Kiểm tra thông tin đăng nhập
    if user_data and len(user_data) > 0 and user_data[0][1] == password:
        # Nếu thông tin đúng, đăng nhập người dùng
        user = User(user_data[0][0], user_data[0][1])
        login_user(user)
        return True
    
    return False

@login_manager.user_loader
def load_user(user_id):
    select_query = f"SELECT username, password FROM user WHERE username = '{user_id}'"
    user_data = execute_query(select_query)
    
    if user_data:
        user = User(user_data[0][0], user_data[0][1])
        return user
    else:
        return None
    
@app.route('/protected')
@login_required
def protected():
    return "This page is protected. You can only access it if you are logged in."

@app.route('/manager/movie/add', methods=['POST'])
def manager_movie_add():
    try:
        data = request.json

        add_type = data.get('add_type')
        name_vn = data.get('name_vn')
        name_en = data.get('name_en')
        status = data.get('status')
        publish_status = data.get('publish_status')
        categories = data.get('categories')
        series = data.get('series')
        lang = data.get('lang')
        nation = data.get('nation')
        duration = data.get('duration')
        sub_type = data.get('sub_type')
        movie_year = data.get('movie_year')
        movie_src = data.get('movie_src')
        movie_thumbnail = data.get('movie_thumbnail')
        actors = data.get('actors')

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current datetime
        insert_query = f"INSERT INTO {add_type} (name_vn,name_en,status,publish_status,categories,series,lang,nation,duration,sub_type,movie_year,created_at,source,thumbnail,actors) VALUES ('{name_vn}','{name_en}','{status}','{publish_status}','{categories}','{series}','{lang}','{nation}','{duration}','{sub_type}','{movie_year}','{current_datetime}','{movie_src}','{movie_thumbnail}','{actors}')"
        success = execute_query(insert_query, commit=True)

        if success:
            response = {
                'success': True,
                'message': 'Thêm mới thành công.'
            }
            return jsonify(response), 200
        else:
            response = {
                'success': False,
                'message': 'Thêm mới thất bại.',
                'error': str(success)
            }
            return jsonify(response), 500
    except Exception as ex:
        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(ex)
        }
        return jsonify(response), 400
    
@app.route('/manager/movie/update', methods=['PUT'])
def manager_movie_update():
    try:
        data = request.json

        edit_type = data.get('edit_type')
        edit_id = data.get('edit_id')
        name_vn = data.get('name_vn')
        name_en = data.get('name_en')
        status = data.get('status')
        publish_status = data.get('publish_status')
        categories = data.get('categories')
        series = data.get('series')
        lang = data.get('lang')
        nation = data.get('nation')
        duration = data.get('duration')
        sub_type = data.get('sub_type')
        movie_year = data.get('movie_year')
        movie_src = data.get('movie_src')
        movie_thumbnail = data.get('movie_thumbnail')
        actors = data.get('actors')

        update_query = f"UPDATE {edit_type} SET name_vn='{name_vn}',name_en='{name_en}',status='{status}',publish_status='{publish_status}',categories='{categories}',series='{series}',lang='{lang}',nation='{nation}',sub_type='{sub_type}',duration='{duration}',movie_year='{movie_year}',source='{movie_src}',thumbnail='{movie_thumbnail}',actors='{actors}'  WHERE id = '{edit_id}'"
        success = execute_query(update_query, commit=True)

        if success:
            response = {
                'success': True,
                'message': 'Đã cập nhật thành công'
            }
            return jsonify(response), 200

        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi khi cập nhật thông tin.',
            'error': str(success)
        }
        return jsonify(response), 500
    except Exception as ex:
        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(ex)
        }
        return jsonify(response), 400

@app.route('/manager/parameter/add', methods=['POST'])
def manager_parameter_add():
    try:
        data = request.json

        add_type = data.get('add_type')
        add_name = data.get('add_name')

        # Check if the username already exists
        select_query = f"SELECT name FROM {add_type} WHERE name = '{add_name}'"
        existing_data = execute_query(select_query)

        if existing_data:
            response = {
                'success': False,
                'message': 'Thông tin đã tồn tại'
            }
            return jsonify(response), 400

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current datetime
        insert_query = f"INSERT INTO {add_type} (name, created_at) VALUES ('{add_name}', '{current_datetime}')"
        success = execute_query(insert_query, commit=True)

        if success:
            response = {
                'success': True,
                'message': 'Thêm mới thành công.'
            }
            return jsonify(response), 200
        else:
            response = {
                'success': False,
                'message': 'Thêm mới thất bại.',
                'error': str(success)
            }
            return jsonify(response), 500
    except Exception as ex:
        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(ex)
        }
        return jsonify(response), 400

@app.route('/manager/parameter/update', methods=['PUT'])
def manager_parameter_update():
    try:
        data = request.json
        edit_type = data.get('edit_type')
        edit_name = data.get('edit_name')
        id = data.get('id')

        update_query = f"UPDATE {edit_type} SET name = '{edit_name}' WHERE id = '{id}'"
        success = execute_query(update_query, commit=True)

        if success:
            response = {
                'success': True,
                'message': 'Đã cập nhật thành công'
            }
            return jsonify(response), 200

        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi khi cập nhật thông tin.',
            'error': str(success)
        }
        return jsonify(response), 500
    except Exception as ex:
        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(ex)
        }
        return jsonify(response), 400


@app.route('/manager/parameter/delete/<delete_type>/<delete_id>', methods=['DELETE'])
def manager_parameter_delete(delete_type, delete_id):
    try:
        delete_query = f"DELETE FROM {delete_type} WHERE id = '{delete_id}'"
        success = execute_query(delete_query, commit=True)

        if success:
            response = {
                'success': True,
                'message': 'Đã xoá thành công'
            }
            return jsonify(response), 200

        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi khi xoá thông tin.',
            'error': str(success)
        }
        return jsonify(response), 500
    except Exception as ex:
        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(ex)
        }
        return jsonify(response), 400
    
@app.route('/manager/series/get-movie/<series_id>', methods=['GET'])
def manager_get_series_movie_by_id(series_id):
    try:
        get_query = f"SELECT movie_id FROM series_movie WHERE series_id = '{series_id}'"
        movies = execute_query(get_query)

        print(movies)
        
        if movies:
            response = {
                'success': True,
                'data': movies
            }
            return jsonify(response), 200

        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(movies)
        }
        return jsonify(response), 500
    except Exception as ex:
        response = {
            'success': False,
            'message': 'Đã xảy ra lỗi.',
            'error': str(ex)
        }
        return jsonify(response), 400


if __name__ == '__main__':
    app.run()
