# -*- coding: utf-8 -*-
# 第一《忉利天宫神通品》共2203字；
##
# 第二《分身集会品》共687字；
##
# 第三《观众生业缘品》共964字；
##
# 第四《阎浮众生业感品》共2044字；
##
# 第五《地狱名号品》共830字；
##
# 第六《如来赞叹品》共1910字；
##
# 第七《利益存亡品》共989字；
##
# 第八《阎罗王众赞叹品》共1725字；
##
# 第九《称佛名号品》共751字；
##
# 第十《校量布施功德缘品》共1013字；
##
# 第十一《地神护法品》共564字；
##
# 第十二《见闻利益品》共2343字；
##
# 第十三《嘱累人天品》共1033字。
##
# 合计17056个字不含标点

from collections import OrderedDict
from flask import Flask, render_template, url_for

class TextChecker(object):
    def __init__(self, text):
        self._text = text
        self.counter = {}
        self.hancounter = OrderedDict()
        self.result = []

    def is_chinese(self, ch):
        if '\u4e00' <= ch <= '\u9fff' and ch != '　':
            return True
        return False

    def countch(self, sens):
        cnt = 0
        for ch in sens:
            if self.is_chinese(ch):
                cnt += 1
        return cnt

    def toveccnt(self):
        for idx, ch in enumerate(self._text, 1):
            self.counter[idx] = ch
            if self.is_chinese(ch):
                self.hancounter[idx] = ch

    def countval(self):
        self.length = len(self.counter)
        self.hanlength = len(self.hancounter)

    def countergen(self):
        for i in self.counter:
            yield self.counter[i]

    def rangetotxt(self, start, end):
        return "".join([self.counter[k] for k in range(start, end)])

    def cut(self, length):
        times = self.hanlength // length
        keylst = list(self.hancounter)
        for time in range(times):
            start = time * length
            end = time * length + length
            self.result.append(self.rangetotxt(keylst[start], keylst[end]))

        self.result.append(self._text[keylst[end] - 1:])

    def smart_cut(self, length):
        single = []
        buff_size = 0
        for i in self._text.split('\n'):
            if buff_size >= length:
                target = "\n".join(single)
                single = []
                self.result.append(target)
                buff_size = 0
            else:
                single.append(i)
                buff_size += self.hanlen(i)
        else:
            if len(single) > 0:
                target = "\n".join(single)
                single = []
                self.result.append(target)
                buff_size = 0

    def hanlen(self, text):
        cnt = 0
        for i in text:
            if self.is_chinese(i):
                cnt += 1

        return cnt


with open('dizangjing.txt', 'r') as f:
    text = f.read()
    t = TextChecker(text)
    t.toveccnt()
    t.countval()

app = Flask(__name__)

@app.route('/<int:cut>/<int:cnt>')
def index(cut, cnt):
    t.result = []
    t.smart_cut(cut)
    if cnt <= 0:
        cnt = 1
    try:
        txt = t.result[cnt - 1]
    except IndexError:
        txt = t.result[-1]
    hanlen = t.hanlen(txt)
    html = ""
    for i in txt.split('\n\n'):
        html += "<p>{}</p>".format(i.replace('\n', '<br \\>'))
    options = ""
    for i in range(len(t.result)):
        url = url_for('index', cut=cut, cnt=i+1)
        if i != cnt - 1:
            options += f"<option value='{url}'>{i + 1}</option>"
        else:
            options += f"<option value='{url}' selected=\"selected\">{i + 1}</option>"
    return render_template('index.html', html=html,
                           hanlen=hanlen,
                           options=options,
                           cut=cut,
                           cnt=cnt)


if __name__ == '__main__':
    app.run()
