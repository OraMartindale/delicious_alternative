from flask import Flask, request, render_template
import format_bookmarks
app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Hello, World!'


@app.route('/bookmarks/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def bookmarks_page():
    func = BOOKMARK_FUNCS[request.method]
    return func()


def _get_bookmarks():
    bookmarks = format_bookmarks._get_bookmarks()
    return render_template('homepage.html', bookmarks=bookmarks)


def _add_bookmark():
    return 'Add Bookmarks Functionality coming soon.'


def _update_bookmark():
    return 'Update Bookmarks Functionality coming soon.'


def _delete_bookmark():
    return 'Delete Bookmarks Functionality coming soon.'


BOOKMARK_FUNCS = {
    'POST': _add_bookmark,
    'GET': _get_bookmarks,
    'PUT': _update_bookmark,
    'DELETE': _delete_bookmark
}

if __name__ == "__main__":
    app.run()
