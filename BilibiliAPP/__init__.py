from BilibiliAPP import HttpUtil, UrlConstant
from instance import *
import video


class View:
    @staticmethod
    def input_bili_id(bili_id: str) -> str:
        bili_id = re.findall("video/(\\w+)/?", bili_id)[0] if 'http' in bili_id else bili_id
        if bili_id.find('av') != -1 or bili_id.isdigit() is True:
            return UrlConstant.AID_INFO_API.format(re.sub(r"av", "", bili_id))
        elif bili_id.find("BV") != -1:
            return UrlConstant.AID_INFO_API.format(Transformation().AV(bili_id))

    @staticmethod
    def web_interface_view(api_url: str, max_retry: int = 5) -> dict:
        web_interface_view_url = View.input_bili_id(api_url)
        for retry in range(max_retry):
            return HttpUtil.get(web_interface_view_url).json()
        else:
            print("web_interface_view:", Vars.video_info.get("message"))

    @staticmethod
    def play_url_by_cid(bid, cid, qn, max_retry: int = 5) -> dict:
        # get video play video url
        for index in range(max_retry):
            params = {'bvid': bid, 'qn': qn, 'cid': cid, 'fnval': '0', 'fnver': '0', 'fourk': '1'}
            return HttpUtil.get(UrlConstant.VIDEO_API, params=params).json()
        else:
            print("play_url_by_cid:", Vars.video_info.get("message"))


def get_video_url(bid, cid, qn, title) -> [str, str]:
    response = View.play_url_by_cid(bid, cid, qn)
    if response.get("code") == 0:
        video_url = [durl['url'] for durl in response.get("data")['durl']]
        return video_url[0], re_book_name(title)


class Transformation:
    @staticmethod
    def AV(bv_id: str):
        key = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        result = sum([{key[i]: i for i in range(58)}[bv_id[[11, 10, 3, 8, 4, 6][i]]] * 58 ** i for i in range(6)])
        return (result - 8728348608) ^ 177451812

    @staticmethod
    def BV(av_id: int):
        key = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        x = (av_id ^ 177451812) + 8728348608
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[[11, 10, 3, 8, 4, 6][i]] = key[x // 58 ** i % 58]
        return ''.join(r)

    # print(AV('BV17x411w7KC'))
    # print(BV(722602127))
