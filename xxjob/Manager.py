import efinance as ef
from datetime import datetime, timedelta
import pandas as pd
from xxjob.blocksModel import RichText, TableX
from dingtalkchatbot.chatbot import DingtalkChatbot
import holidays
import copy
from decimal import Decimal

from xxjob.easyNotion import easyNotion


def dingpush(jsondataArray):
    webhook = ('https://oapi.dingtalk.com/robot/send?access_token'
               '=dd9371044f8fa37f87d0e2d6aa7779e9e0fe5726fa37d512d07c153829a526ab')
    secret = 'SECd1cdc38d02add22f10362755d61e5d8608a86a36036dae78be30875490608bb8'  # 可选：创建机器人勾选“加签”选项时使用
    xiaoding = DingtalkChatbot(webhook, pc_slide=True, secret=secret)
    text_str = ''
    current_date = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now()
    year, current_week, weekday = now.isocalendar()
    for jsondata in jsondataArray:
        isup = hasattr(jsondata, 'upNum')
        text_str += f"[{jsondata["Name"]}](http://coding.net)\n\n\n"
        text_str += f"![{jsondata["Name"]}](https://j3.dfcfw.com/images/APPFavorNav/big/SYL_3Y/{jsondata['Code']}.png)\n\n\n"
        text_str += f"[{jsondata["vals"]}]\n\n\n"
        text_str += jsondata[f'{current_week}Week'] + " " + jsondata[f'{current_week - 1}Week'] + " " + jsondata[
            f'{current_week - 2}Week'] + "\n\n\n"
    xiaoding.send_markdown(title='提醒', text=text_str, is_at_all=False)


def get_week_start_end_date(year, week_num):
    cn_holidays = holidays.CN()
    start_of_week = datetime.strptime(f'{year}-W{week_num}-1', '%Y-W%W-%w')
    end_of_week = start_of_week + timedelta(days=4)
    work_days = [d for d in pd.date_range(start=start_of_week, end=end_of_week) if d not in cn_holidays]
    first_work_day = min(work_days)
    last_work_day = max(work_days)
    now = datetime.now()
    if last_work_day > now:
        last_work_day = now
        if now.hour < 18:
            last_work_day = last_work_day + timedelta(days=-1)
    return first_work_day.date(), last_work_day.date()


def calculate_percentage(old, new):
    if new == 0 or old == 0:
        return 0
    # 计算百分比并格式化输出为两位小数
    percentage = ((new - old) / old) * 100
    return round(percentage, 2)


if __name__ == '__main__':
    dbPage = easyNotion(notion_id='d5c62b873aef4b77afc2e7870de97e38',
                        token='secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ',
                        is_page=True)
    current_date = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now()
    year, current_week, weekday = now.isocalendar()
    step = current_week if int(current_week) - 4 > 0 else 0
    parent_id = dbPage.create_page(title=f"{current_date}周报", parent_id="d5c62b873aef4b77afc2e7870de97e38")
    jsonArray = []
    jsonPushData = []
    title = {'Name': '名称', 'Code': 'Code'}
    for i in range(current_week, step, -1):
        title.update({f'{i}Week': f'{i}Week'})
    jsonArray.append(title)
    with open('./txt_dingfund.txt', 'r') as file:
        for item in file:
            baseinfo = ef.fund.get_base_info(item.strip())
            df1 = ef.fund.get_quote_history(item.strip(), 30)
            itm = {'Name': baseinfo["基金简称"], 'Code': baseinfo["基金代码"]}
            for i in range(current_week, step, -1):
                start_date, end_date = get_week_start_end_date(2024, i)
                result0 = df1[df1['日期'] == f'{start_date}']
                result1 = df1[df1['日期'] == f'{end_date}']
                if len(result0) != 0 and len(result1) != 0:
                    vl = calculate_percentage(result0.iloc[0]['单位净值'], result1.iloc[0]['单位净值'])
                    itm.update({f'{i}Week': f'{vl:.2f}%'})
                else:
                    itm.update({f'{i}Week': f'{0:.2f}%'})
            jsonArray.append(itm)
            itm_new = copy.deepcopy(itm)

            dayNum_up = 3
            dayNum_down = 3
            subset_df = df1.head(dayNum_down)
            vals = subset_df['涨跌幅'].astype(str).str.cat(sep='  ')
            if all(subset_df['涨跌幅'] < 0):
                itm_new.update({'downNum': f'{dayNum_down}', "vals": vals})
                jsonPushData.append(itm_new)
            if all(subset_df['涨跌幅'] > 0):
                itm_new.update({'upNum': f'{dayNum_up}', "vals": vals})
                jsonPushData.append(itm_new)
            if Decimal(itm[f'{current_week}Week'].replace("%", "")) > 0 and Decimal(itm[f'{current_week}Week'].replace("%", "")) > 0 and Decimal(itm[f'{current_week}Week'].replace("%", "")) > 0:
                jsonPushData.append(itm)
            if Decimal(itm[f'{current_week}Week'].replace("%", "")) + Decimal(itm[f'{current_week}Week'].replace("%", "")) + Decimal(itm[f'{current_week}Week'].replace("%", "")) > 0:
                jsonPushData.append(itm)
    content_blocks = [
        RichText(text_type="callout", id="", parent_id=parent_id, plain_text="callout",
                 annotations={"color": "red"}),
        TableX("", jsonArray, parent_id),
    ]
    dingpush(jsonPushData)
    dbPage.insert_page(blocks=content_blocks)
    # df1["单位净值"] = [str(ite) for ite in df1["单位净值"]]
    # df1["Color"] = ["gray" if ite > 0 else 'red' for ite in df1["涨跌幅"]]
    # df1["涨跌幅"] = [str(ite) for ite in df1["涨跌幅"]]
    # json_data = json.loads(df1.to_json(orient='records'))
    # for item in json_data:
    #     del item["累计净值"]
    # json.dumps(json_data)
    # content_blocks = [
    #     ColumnList(parent_id=parent_id,
    #                id='',
    #                content=[
    #                    TableX("", json_data[:10], parent_id),
    #                    Image(parent_id,
    #                          "https://gw.alipayobjects.com/zos/bmw-prod/b874caa9-4458-412a-9ac6-a61486180a62.svg"),
    #                ]),
    #     RichText(text_type="paragraph", id="", parent_id=parent_id, plain_text="paragraph"),
    #     RichText(text_type="quote", id="", parent_id=parent_id, plain_text="quote#@@@@@@@"),
    #     RichText(text_type="callout", id="", parent_id=parent_id, plain_text="callout",
    #              annotations={"color": "red"})
    # ]
    # dbPage.insert_page(content_blocks)

    # # 更新指定的行
    # res = db.update({'Name': 'new_value'}, {'Name': '张三'})
    # pprint(res)
    # https://www.notion.so/FIND-5a055a5ef33c4a2eac7e6db00d3ce64c?pvs=4
    # # 删除指定的行
    # res = db.delete({'Name': 'new_value'})
    # # pprint(res)
