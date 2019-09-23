import random
import string
import sys
from datetime import datetime, timedelta, date

import peewee as pe
import requests
from bs4 import BeautifulSoup

db = pe.SqliteDatabase('members.db')

# Models
class Member(pe.Model):
    memberId = pe.IntegerField(primary_key=True)
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

def getSchedules(targetdate:date = date.today()):
    baseurl = ' http://www.keyakizaka46.com/s/k46o/media/list'
    year = targetdate.year
    month = targetdate.month

    dy = datetime(year, month, 1)

    schedule_list = []

    while dy.month == month:
        dy_str = dy.strftime('%Y%m%d')
        res = requests.get(baseurl, {'dy': dy_str})
        html = res.text
        bs = BeautifulSoup(html, 'html.parser')
        details = bs.select('.box-detail')
        # foreach schedules
        for detail in details:
            # Instanciate Schedule
            schedule_obj = {"title": "", "genre": "", 'day': dy}
            #Set day

            # Set Genre
            genre = detail.select_one('div.box-detail_genre p').text.strip()
            if genre == '誕生日':
                continue
            else:
                schedule_obj["genre"] = genre

            # Set title
            detail_txt = detail.select('.box-detail_txt')[0].select('p')
            for text in detail_txt:
                if not text.has_attr('class'):
                    title = text.text.strip()
                    schedule_obj['title'] = title

            schedule_list.append(schedule_obj)
        dy = dy + timedelta(days=1)
    return  schedule_list
def changedate(ja_date):
    uni_dtime = datetime.strptime(ja_date, '%Y年%m月%d日')
    uni_dt = uni_dtime.date()
    return uni_dt


if __name__ == '__main__':
    # createScheduledb()
    pass

