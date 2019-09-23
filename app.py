from flask import Flask, abort, make_response, jsonify, render_template

from util.utils import Member

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def index():
    api_list = ['/members', '/member/20']
    return render_template('index.html', api_list=api_list)


@app.route('/member/<int:memberId>', methods=['GET'])
def get_member(memberId):
    try:
        member = Member.get(Member.memberId == memberId)
    except Member.DoesNotExist:
        return make_response(jsonify({'error': 'Not found'}), 404)

    items = []

    items.append({
        "memberId": member.memberId,
        "name": member.name,
        "furigana": member.furigana,
        "en": member.en,
        "birthday": member.birthday.isoformat(),
        "birthplace": member.birthplace,
        "constellation": member.constellation,
        "height": member.height,
        "bloodtype": member.bloodtype,
        "thumb": member.thumb_url
    })

    result = {
        "ResultInfo": {
            "result": True,
            "count": len(items),
        },
        "items": items
    }

    return make_response(jsonify(result))


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = Member.select()
    except Member.DoesNotExist:
        abort(404)

    items = []

    for member in members:
        items.append({
            "memberId": member.memberId,
            "name": member.name,
            "furigana": member.furigana,
            "birthplace": member.birthplace,
        })

    result = {
        "ResultInfo": {
            "result": True,
            "count": len(items),
        },
        "items": items
    }

    return make_response(jsonify(result))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
