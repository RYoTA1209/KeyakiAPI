import sys
from datetime import datetime

import peewee as pe
import requests
from bs4 import BeautifulSoup

db = pe.SqliteDatabase('members.db')


# Models
class Member(pe.Model):
    memberId = pe.IntegerField()
    name = pe.TextField()
    furigana = pe.TextField()
    en = pe.TextField()
    birthday = pe.DateField()
    birthplace = pe.TextField()
    constellation = pe.TextField()
    height = pe.IntegerField()
    bloodtype = pe.TextField()
    thumb_url = pe.TextField()

    class Meta:
        database = db


db.create_tables([Member])


# DB Creation

def creatememberdb():
    baseURL = 'http://www.keyakizaka46.com/s/k46o/artist/'
    memberId = -1
    for i in range(1, 52):
        memberId = i
        if memberId >= 23 and memberId <= 42:
            continue
        response = requests.get(baseURL + str(memberId).zfill(2))
        # memberIdが23以降日向坂メンバーにリダイレクトされるため
        if response.status_code != 200:
            continue
        html = response.text
        bs = BeautifulSoup(html, 'html.parser')

        member_name = bs.select('p.name')[0].text.strip()
        member_furigana = bs.select('p.furigana')[0].text.strip()
        member_en = bs.select('span.en')[0].text.strip()
        member_img = bs.select('div.box-profile_img img')[0].attrs["src"]
        member_info = [str(tag.text).strip() for tag in bs.select('div.box-info dl dt')]
        member_info[0] = changedate(member_info[0])

        try:
            q = Member.create(memberId=memberId, name=member_name, furigana=member_furigana, en=member_en,
                              birthday=member_info[0], birthplace=member_info[3], constellation=member_info[1],
                              height=member_info[2], bloodtype=member_info[4], thumb_url=member_img)
            print(member_name)
        except Member.DoesNotExist:
            print("Error!! Member.DoesNotExist", file=sys.err)
            continue


def changedate(ja_date):
    uni_dtime = datetime.strptime(ja_date, '%Y年%m月%d日')
    uni_dt = uni_dtime.date()
    return uni_dt


if __name__ == '__main__':
    creatememberdb()
