import copy
import json
import logging
import os.path
import random
import re
from typing import Dict, overload, Any, List, Union
import requests
import tenacity
from tenacity import retry, stop_after_attempt, retry_if_result, retry_if_exception_type, stop_after_delay, wait_exponential
import httpx
from blocksModel import Block, Mention, RichText, LinkPreview, Divider, Column, ColumnList, TableX


class easyNotion:
    @overload

    def __init__(self,
                 notion_id: str,
                 token: Union[str, List[str]],
                 sort_key: List[str] = '',
                 reverse: List[bool] = '',
                 retry_time: int = 4,
                 timeout: int = 15,
                 get_all: bool = True,
                 is_page: bool = False,
                 need_recursion: bool = False,
                 need_download: bool = False,
                 download_path: str = '',
                 trust_env: bool = False):
        ...


    def __init__(self, notion_id: str, token: Union[str, List[str]], **kwargs):
        """
        获得notion服务,可选的关键字参数解释如下\n
        sort_key:List[str] - 排序的列,支持根据多列排序\n
        reverse:List[bool] - 默认升序,为True时降序\n
        retry_time:int - 重试次数,默认3次\n
        timeout:int - 超时时间,默认15s\n
        get_all:bool - 是否获取所有数据,默认获取\n
        is_page:bool - 是否为页面,默认为否\n
        need_recursion:bool - 是否需要递归获得页面的数据,默认不需要\n
        need_download:bool - 是否需要下载到本地,默认不需要\n
        download_path:str - 若有文件保存到哪个目录中\n
        trust_env:bool - 是否关闭代理,默认关闭\n
        :param notion_id: 数据库/页面ID
        :param token: 集成令牌
        :param kwargs: 关键字参数
        """
        # 数据库/页面配置
        self.notion_id = notion_id  # 数据库或页面ID
        self.__all_token = token  # 全部token
        self.__token = ''  # 当前使用token
        self.__sort_key = kwargs.get('sort_key', [])  # 排序键
        self.__reverse = kwargs.get('reverse', [False] * len(self.__sort_key))  # 是否逆序
        self.retry_time = kwargs.get('retry_time', 4)  # 重试次数
        self.timeout = kwargs.get('timeout', 15)  # 超时时间
        self.get_all = kwargs.get('get_all', True)  # 是否获得数据库中全部数据
        self.is_page = kwargs.get('is_page', False)  # 是否是页面
        self.need_recursion = kwargs.get('need_recursion', False)  # 是否递归获得页面数据
        self.__need_download = kwargs.get('need_download', False)  # 是否下载
        self.download_path = kwargs.get('download_path', '')  # 下载地址
        self.__trust_env = kwargs.get('trust_env', False)  # 是否关闭代理

        # 网络相关配置
        self.__session = requests.Session()  # session
        self.__session.trust_env = self.__trust_env  # 初始化本地环境
        self.__baseUrl = 'https://api.notion.com/v1/'  # 基础url

        # 数据库对象信息
        self.__table = []  # 数据表
        self.__col_name = {}  # 列类型
        self.__start_cursor = True  # 查询起始点

    # 使用包裹器发送请求
    def __send_request(self, *args, **kwargs):
        # 检查返回值,错误则返回真
        def is_failure(result: requests.models.Response):
            if result.status_code in [400, 401, 403, 404, 409, 429, 500, 502, 503, 504]:
                logging.warning(f'请求错误.{result.text}')
                return True
            else:
                return False

        # 请求头
        headers = {
            'Accept': 'application/json',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
            'Cookie': '__cf_bm=uxsliE4EFVpT5YkTZ6ACr1jH2vu1TjkfG1gTPXYDyKg-1683367680-0-AVbHMiNx95PBmx3aRCHSTZhivPqUb/Chgy2MTqqPTAkVweNB6jjhKyixXIak85+bXiotNY0RQCRRi3XWtGQ4L4s='
        }

        # 重试前行为
        def before_retry(retry_statue: tenacity.RetryCallState):
            # 检查是否有异常
            exception = retry_statue.outcome.exception() or ''
            exception = '重试原因:' + str(exception)
            logging.warning(f'第{retry_statue.attempt_number}次重试.{exception}')  # 输出次数以及异常
            headers.update({'Connection': 'close'})  # 关闭持续链接

        # 重试结束前行为
        def retry_error(retry_statue):
            if retry_statue.outcome.exception():
                raise retry_statue.outcome.exception()
            else:
                raise Exception(f'达到重试上限!{retry_statue.outcome.result()}')

        # 随机添加一个请求代理/token
        def get_random_requests_headers():
            user_agent_list = [
                {
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666'
                }, {
                    'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
                }, {
                    'user-agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
                }, {
                    'user-agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
                }, {
                    'user-agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
                }, {
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
                }, {
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
                }, {
                    'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
                }
            ]  # 全部请求头
            if 'user-agent' in headers:
                new_headers_list = [item for item in user_agent_list if item != headers['user-agent']]  # 不包含原有头的全部投
                del (headers['user-agent'])  # 删除原有头
                headers.update(random.choice(new_headers_list))  # 更新头
            else:
                headers.update(random.choice(user_agent_list))  # 添加头

            if 'Authorization' in headers:
                del (headers['Authorization'])  # 删除原有头

            if type(self.__all_token) == list:
                new_token_list = [item for item in self.__all_token if item != self.__token]  # 新token
                self.__token = random.choice(new_token_list)
                headers.update({'Authorization': 'Bearer %s' % self.__token})
            else:
                self.__token = self.__all_token
                headers.update({'Authorization': 'Bearer %s' % self.__token})

        @retry(stop=stop_after_attempt(self.retry_time) | stop_after_delay(self.timeout * self.retry_time),
               # 达到重试次数或超出时间限制停止重试
               wait=wait_exponential(multiplier=1, min=1, max=5),  # 指数级退避
               retry=retry_if_result(is_failure) | retry_if_exception_type(),  # 若失败则重试
               before_sleep=before_retry,  # 重试前行为
               retry_error_callback=retry_error)  # 结束重试前行为
        def send_request(*args, **kwargs):
            get_random_requests_headers()  # 更新请求代理

            return self.__session.request(*args, **kwargs, timeout=self.timeout, headers=headers)

        return send_request(*args, **kwargs)

    # 获得原始数据表
    def get_original_table(self) -> json:
        """
        获得原始数据表
        :return: 获得数据库中的全部的未处理数据,若成功返回json对象,结果按照no列递增排序,失败则返回错误代码
        """
        payload = {'sorts': []}

        # 排序请求
        for sort_col in zip(self.__sort_key, self.__reverse):
            payload['sorts'].append(
                {'property': sort_col[0],
                 'direction': 'descending' if sort_col[1] else 'ascending'})

        original_table = {}

        while True:
            if self.__start_cursor and isinstance(self.__start_cursor, str):
                payload["start_cursor"] = self.__start_cursor

            # 发送请求
            if self.is_page:  # 页面类型
                res = self.__send_request(method="GET",
                                          url=f'{self.__baseUrl}blocks/{self.notion_id}/children?page_size=100')
            else:  # 数据库类型
                res = self.__send_request(method="POST",
                                          url=f'{self.__baseUrl}databases/{self.notion_id}/query',
                                          json=payload)

            data = res.json()  # 转为dict格式
            # 判断原始表是为为空,不为空则追加
            if original_table:
                original_table['results'].extend(data['results'])
            else:
                original_table = data
            # 记录分页位置
            self.__start_cursor = data["next_cursor"]
            if not data.get("has_more") or not self.get_all:  # 没有后续或不得到全部表则跳出循环
                break

        return original_table

    # 从上一次查询处继续查询100行
    def next(self) -> bool:
        """
        从上一次查询处继续查询100行
        :return:有后续内容返回True,否则返回False
        """

        if self.__start_cursor:
            original_table = self.get_original_table()
            self.__get_table(original_table)
            return True
        else:
            return False

    # 获得处理后的数据表,避免重复查询
    def get_table(self) -> List[Dict[str, str]]:
        """
        获得处理后的数据表
        :return: 处理后的数据表
        """
        # 已经有表则直接返回
        if self.__table:
            return copy.deepcopy(self.__table)

        # 没有表则查询
        base_table = {}
        while type(base_table) is not dict or 'results' not in base_table:  # 避免查询错误
            base_table = self.get_original_table()  # 未处理的表

        self.__get_table(base_table)

        return copy.deepcopy(self.__table)  # 深拷贝

    # 根据原始表获得处理后的表
    def __get_table(self, base_table: json) -> bool:
        """
        处理数据表并返回处理后的表
        :param base_table: 原始数据表
        :return: 成功返回True
        """
        # 从原始表中获得数据

        if self.is_page:

            self.__table.extend(self.__get_page_data(base_table))
        else:
            self.__table.extend(self.__get_database_data(base_table))

        return True

    @staticmethod
    def __get_rich_text_content(row: dict) -> Block:
        text_type = row['type']
        all_rich_text = row[text_type]['rich_text']
        ret = []
        for rich_text in all_rich_text:
            if rich_text['type'] == 'mention':
                temp = Mention(row['id'], rich_text['href'], row['parent']['block_id'])
            else:
                href = None
                if 'href' in rich_text:
                    href = rich_text['href']

                temp = RichText(text_type, row['id'], row['parent'][row['parent']['type']], rich_text['annotations'],
                                href, rich_text['plain_text'])
            ret.append(temp)

        return Block(ret)

    # 获得页面中的数据列表
    def __get_page_data(self, base_table: json) -> List[Dict[str, str]]:
        table = []
        for original_row in base_table['results']:

            row = {'id': original_row['id']}

            rich_text_type = ['paragraph', 'heading_2', 'toggle', 'bulleted_list_item', 'callout']

            if original_row['type'] == 'image':  # 图片类型
                url = original_row['image']['file']['url']
                session = requests.session()
                session.trust_env = self.__session.trust_env
                response = session.get(url)  # 下载文件
                row['image_source_path'] = url
                image_name = re.search(r'.*/(.*\..*)\?.*', url).group(1)  # 得到文件名
                # Check if the request was successful
                if response.ok:
                    if self.__need_download:  # 需要下载到本地时才下载到本地
                        if not os.path.exists(self.download_path):
                            os.mkdir(self.download_path)
                        path = os.path.join(self.download_path, image_name)  # 得到下载路径
                        with open(path, "wb") as image_file:
                            image_file.write(response.content)  # 保存到本地
                        row['image_download_path'] = path
                else:
                    row['image_download_path'] = 'wrong_request'
                session.close()
                self.__col_name[image_name] = 'image'
            elif original_row['type'] in rich_text_type:  # 是富文本类型
                row['block'] = self.__get_rich_text_content(original_row)

            elif original_row['type'] == 'link_preview':  # github大图预览
                row['block'] = LinkPreview(original_row['id'], original_row['link_preview']['url'],
                                           original_row['parent']['block_id'])
            elif original_row['type'] == 'divider':  # 分割线只保留ID
                row['block'] = Divider(original_row['id'], original_row['parent']['block_id'])
            elif original_row['type'] == 'column':  # 列
                row['block'] = Column(original_row['id'], original_row['parent']['block_id'])
            elif original_row['type'] == 'column_list':  # 列列表
                row['block'] = ColumnList(original_row['id'], original_row['parent']['block_id'])

            # 需要递归获得页面数据
            if self.need_recursion and original_row['has_children']:
                self.__get_recursion_data(row)

            table.append(row)

        return table

    # 获得数据库中的数据列表
    def __get_database_data(self, base_table: json) -> List[Dict[str, str]]:
        """
        获得数据库中的所有记录
        :param base_table: 原始数据表
        :return:处理后的数据
        """
        table = []
        for original_row in base_table['results']:
            row = {'id': original_row['id']}  # 行id,这是系统的id不是显示的ID

            for col in original_row['properties']:
                if original_row['properties'][col]['type'] == 'unique_id':  # 处理ID列
                    row[col] = original_row['properties'][col]['unique_id']['prefix'] + '-' + str(  # 若没有前缀则只要数字
                        original_row['properties'][col]['unique_id']['number']) if \
                        original_row['properties'][col]['unique_id']['prefix'] else str(
                        original_row['properties'][col]['unique_id']['number'])
                    self.__col_name[col] = 'ID'  # 列名称:列类型
                elif original_row['properties'][col]['type'] == 'title':  # 处理title列
                    title = original_row['properties'][col]['title']
                    if len(title) != 0:
                        row[col] = original_row['properties'][col]['title'][0]['plain_text']
                    else:
                        row[col] = ''
                    self.__col_name[col] = 'title'  # 列名称:列类型
                elif original_row['properties'][col]['type'] == 'url':  # 处理url列
                    url = original_row['properties'][col]['url']
                    if url:
                        row[col] = url
                    else:
                        row[col] = ''
                    self.__col_name[col] = 'url'  # 列名称:列类型
                elif original_row['properties'][col]['type'] == 'rich_text':  # 处理text列
                    text = original_row['properties'][col]['rich_text']
                    if len(text) != 0:
                        row[col] = original_row['properties'][col]['rich_text'][0]['plain_text']
                    else:
                        row[col] = ''
                    self.__col_name[col] = 'text'  # 列名称:列类型
                elif original_row['properties'][col]['type'] == 'checkbox':  # 处理text列
                    text = original_row['properties'][col]['checkbox']
                    if bool(text):
                        row[col] = bool(text)
                    else:
                        row[col] = False
                    self.__col_name[col] = 'checkbox'  # 列名称:列类型
                elif original_row['properties'][col]['type'] == 'files':  # 处理text列
                    text = original_row['properties'][col]['files']

                    if len(text) != 0:
                        row[col] = original_row['properties'][col]['files'][0]["external"]["url"]
                    else:
                        row[col] = ''
                    self.__col_name[col] = 'files'  # 列名称:列类型
            table.append(row)

            # 需要递归获得页面数据
            if self.need_recursion:
                self.__get_recursion_data(row)
        return table

    def __get_recursion_data(self, row: dict) -> None:
        page_svc = easyNotion(row['id'], self.__token, is_page=True, need_recursion=True,
                              need_download=self.__need_download, download_path=self.download_path)
        row['son_blocks'] = page_svc.get_table()

        self.__col_name[row['id']] = page_svc.get_col_name()
        page_svc.close_session()

    # 获得列名称列表
    def get_col_name(self) -> Dict[str, str]:
        """
        获得列名称:列类型列表
        :return: 列名称字典,{'text':['文本类型的列名'],'ID':'ID类型的列明','title':'title类型的列名'}
        """
        # 已经有列名:列类型则直接返回
        if self.__col_name:
            return copy.deepcopy(self.__col_name)
        # 没有则查询
        self.get_table()
        return copy.deepcopy(self.__col_name)

    # 通用查询
    def query(self, query_col: List[str], query_condition: Dict[str, Union[str, re.Pattern]] = '') -> List[
        Union[str, Dict[str, str]]]:
        """
        根据query_condition条件对数据表的query_col列进行查询
        :param query_col:要查询的列名,为空列表时查询所有的列
        :param query_condition:查询条件,{'列名':'列值'},默认查询全部行
        :return:满足条件的行(当只查询一列时返回一个列表,多列时返回字典列表),查询行数,列表中元素的类型(没有结果时为None)
        """
        table = self.get_table()
        ret = []

        # 遍历表
        for row in table:
            # 判断是否满足条件
            if self.__is_match_condition(row, query_condition):
                if query_col:  # 查询特定列时
                    if len(query_col) == 1:  # 只查询一列
                        temp_row = row[query_col[0]]
                    else:  # 查询多列
                        temp_row = {col: row[col] for col in query_col}
                else:  # 查询所有列返回整行
                    temp_row = row

                ret.append(temp_row)

        return copy.deepcopy(ret)


    def __is_match_condition(row: Dict[str, str], condition: Dict[str, Union[str, re.Pattern]]) -> bool:
        """
        判断row是否符合条件condition,condition为正则表达式
        :param row: 行Dict格式
        :param condition: 条件,Dict格式,支持正则
        :return: 符合条件返回True,否则返回False
        """

        for i in condition:
            if type(condition[i]) == re.Pattern:  # 正则表达式使用正则处理
                if not re.search(condition[i], row[i]):  # 不符合正则则返回False
                    return False
            else:  # 普通字符串做普通处理
                if row[i] != condition[i]:  # 不相等返回False
                    return False
        else:
            return True

    # 获得数据库基本信息
    def __get_database_info(self) -> None:
        """
        获得数据库基本信息——用于当数据库为空时获得基本信息
        :return: None
        """
        res = self.__send_request(method='GET',
                                  url=self.__baseUrl + 'databases/' + self.notion_id)

        table_info = json.loads(res.text)
        for col in table_info['properties']:
            if table_info['properties'][col]['type'] == 'title':
                self.__col_name[col] = 'title'
            elif table_info['properties'][col]['type'] == 'rich_text':
                self.__col_name[col] = 'text'
            elif table_info['properties'][col]['type'] == 'unique_id':
                self.__col_name[col] = 'unique_id'
            elif table_info['properties'][col]['type'] == 'url':
                self.__col_name[col] = 'url'
            elif table_info['properties'][col]['type'] == 'checkbox':
                self.__col_name[col] = 'checkbox'
            elif table_info['properties'][col]['type'] == 'files':
                self.__col_name[col] = 'files'

    # 插入数据

    def insert(self, data: Dict[str, str]) -> requests.models.Response:
        """
        插入数据
        :param data:所要插入的数据,{列名1:值1,列名2:值2}
        """

        col_names = self.get_col_name()
        payload = {}

        if len(col_names) == 0:
            self.__get_database_info()
            col_names = self.get_col_name()

        # 遍历全部列
        for col_name in col_names:
            if col_name in data:  # 若已指定数据则插入指定数据
                payload.update(self.__get_payload(col_name, data[col_name]))
            else:  # 没有指定则为空
                payload.update(self.__get_payload(col_name, ''))

        payload = {
            "parent": {
                "database_id": self.notion_id
            },
            "properties": payload
        }

        res = None
        while not isinstance(res, requests.models.Response):
            res = self.__send_request(method="POST",
                                      url=f'{self.__baseUrl}pages',
                                      json=payload)

        if res.ok:
            # 更新表
            insert_data = (json.loads(res.text))
            insert_data = {'results': [insert_data]}
            self.__get_table(insert_data)

        return res

    # 插入页面数据
    def insert_page(self,
                    blocks: List[
                        Union[Divider, Mention, LinkPreview, RichText, Block, TableX]]) -> requests.models.Response:
        """
        插入页面数据
        :param blocks: 富文本块列表
        """
        payload = []

        for block in blocks:
            temp_payload = {
                'object': 'block',
                'type': block.text_type,
            }
            temp_payload.update(block.get_payload())
            payload.append(temp_payload)

        payload = {
            'children': payload
        }
        return self.__send_request(method="PATCH",
                                   url=self.__baseUrl + 'blocks/' + blocks[0].parent_id + '/children',
                                   json=payload)

    def create_page(self, title: str, parent_id: str) -> str:
        """
        插入页面数据
        :param blocks: 富文本块列表
        """
        payload = {
            "parent": {
                "page_id": parent_id
            },
            "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            }
        }
        client = httpx.Client(timeout=10.0, headers=
        {
            "Notion-Version": "2022-06-28",
            "Authorization": "Bearer secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ",
            "Content-Type": "application/json"
        })
        response = client.post("https://api.notion.com/v1/pages", json=payload)
        data=response.json()
        return data["id"]

    # 更新数据
    def update(self, update_data: Dict[str, str], update_condition: Dict[str, Union[str, re.Pattern]]) -> \
            List[requests.models.Response]:
        """
        将满足update_condition条件的行更新为update_data
        :param update_condition: 更新条件,{'列名':'列值'}
        :param update_data: 更新的数据
        :return:符合条件的每一行请求对象
        """
        payload = {"properties": {}}
        # 获得更新payload
        for col_name in update_data:
            payload['properties'].update(self.__get_payload(col_name, update_data[col_name]))

        id_list = self.query(['id'], update_condition)

        ret = []
        for ID in id_list:
            temp_ret = None
            while not isinstance(temp_ret, requests.models.Response):
                temp_ret = self.__send_request(method='PATCH',
                                               url=self.__baseUrl + 'pages/' + ID,
                                               json=payload)

            ret.append(temp_ret)

        # 更新表
        if len(ret):
            table = self.get_table()
            for row in table:  # 遍历表,找到更新的行
                if row['id'] in id_list and ret[id_list.index(row['id'])].ok:  # 只有成功更新的才更新表:
                    for col_name in update_data:
                        row[col_name] = update_data[col_name]

            self.__table = table

        return ret

    # 更新页面中的块
    def update_page(self, block: Union[Divider, Mention, LinkPreview, RichText]):
        return self.__send_request(method='PATCH',
                                   url=self.__baseUrl + 'blocks/' + block.id,
                                   json=block.get_payload())

    def delete_page(self, page_id: str):
        return self.__send_request(method='DELETE',
                                   url=self.__baseUrl + 'blocks/' + page_id)

    # 得到各种类型数据的用于更新、插入数据的payload
    def __get_payload(self, col_name: str, content: str) -> dict[Any, Any] | dict[
        str, list[dict[str, str | dict[str, str]]]]:
        """
        得到各种类型的用于更新、插入数据的payload
        :param col_name:列名称
        :param content:要插入或更新的内容
        :return:一个包含用于更新、插入的payload的Dict
        """
        col_names = self.get_col_name()

        if col_names[col_name] == 'title':  # 标题类型
            return {
                col_name: {
                    "title": [
                        {
                            'type': 'text',
                            'text': {'content': str(content)},
                            "plain_text": str(content)
                        }
                    ]
                }
            }
        elif col_names[col_name] == 'text':  # 文本类型
            return {
                col_name: {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(content)
                            },
                            "plain_text": str(content)
                        }
                    ]
                }}
        elif col_names[col_name] == 'url':  # url类型
            return {
                col_name: {
                    'type': 'url',
                    'url': str(content) if content else ' '
                }
            }
        elif col_names[col_name] == 'checkbox':  # url类型
            return {
                col_name: {
                    'type': 'checkbox',
                    'checkbox': bool(content) if content else False
                }
            }
        elif col_names[col_name] == 'files':  # url类型

            return {col_name: {"files": [{"type": "external", "name": "Cover",
                                          "external": {
                                              "url": str(content)}}]}}
        else:
            return {}

    #
    def delete(self, delete_condition: Dict[str, Union[str, re.Pattern]]) -> List[requests.models.Response]:
        """
        删除满足delete_condition条件的行
        :param delete_condition: 删除条件,{'列名':'列值'}
        :return:返回响应对象
        """
        id_list = self.query(['id'], delete_condition)

        ret = []
        for ID in id_list:
            temp_ret = None
            while not isinstance(temp_ret, requests.models.Response):
                temp_ret = self.__send_request(method='DELETE',
                                               url=self.__baseUrl + 'blocks/' + ID)
            ret.append(temp_ret)

        # 更新表
        if len(ret):
            table = self.get_table()
            for row in table:
                if row['id'] in id_list and ret[id_list.index(row['id'])].ok:
                    table.remove(row)

            self.__table = table

        return ret

    # 追加内容
    def append(self, append_data: Dict[str, str], append_condition: Dict[str, Union[str, re.Pattern]], divide='') -> \
            List[requests.models.Response]:
        """
        向满足append_condition条件的行追加append_data内容
        :param append_data:追加内容
        :param append_condition:追加条件
        :param divide:分隔符,默认为空
        :return:响应对象列表
        """
        query_col = list(append_data.keys())  # 获得更新的列
        query_col.append('id')  # 同时查询id

        src_contents = self.query(query_col, append_condition)  # 获得原始内容
        new_contents = []
        for src_content in src_contents:  # 遍历满足追加条件的行
            temp = {}
            for data in append_data:  # 遍历追加内容
                temp[data] = src_content[data] + divide + str(append_data[data])  # 新行=旧行+追加内容
            temp['id'] = src_content['id']
            new_contents.append(temp)

        ret = []
        for new_content in new_contents:  # 遍历新行
            update_content = {k: v for k, v in new_content.items() if k != 'id'}  # 获得不包含id的更新内容
            ret.extend(
                self.update(update_content, {'id': new_content['id']}))  # 更新行

        return ret

    # 获得truest_env
    @property
    def trust_env(self):
        return self.__trust_env

    # 设置truest_env
    @trust_env.setter
    def trust_env(self, value: bool):
        self.__trust_env = value
        self.__session.trust_env = value

    # 关闭session
    def close_session(self) -> None:
        """
        关闭session
        """
        return self.__session.close()

    # 垃圾回收器
    def __del__(self):
        self.close_session()
