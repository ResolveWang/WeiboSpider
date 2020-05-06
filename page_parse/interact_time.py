import datetime
import re

from logger import parser


def get_create_time_from_text_default_error_handler(
        create_time_str: str, e: Exception) -> datetime.datetime:
    """[default error handler will return datetime of now]

    Arguments:
        create_time_str {str} -- [origin str]
        e {Exception} -- [Exception]

    Returns:
        datetime -- [datetime of now]
    """

    parser.error('解析评论时间失败，原时间为"{}"，具体信息是{}'.format(create_time_str, e))
    return datetime.datetime.now()


def get_create_time_from_text(create_time_str: str) -> datetime.datetime:
    """[Get create time from text]

    Arguments:
        create_time_str {str} -- [create time str]

    Returns:
        datetime -- [create time]
    """

    # 第XX楼
    create_time_str = re.sub(r"\u7b2c[0-9]+\u697c", "", create_time_str)
    create_time_str = create_time_str.strip()
    if '秒' in create_time_str:
        # 40秒前
        # Since the datetime accuracy is set to minute,
        # we use now as create time
        create_time = datetime.datetime.now()
    elif '分钟前' in create_time_str:
        # 2分钟前/12分钟前/55分钟前
        create_time_minute = re.sub(r"\D", "", create_time_str)  # 10分钟前 -> 10
        create_time_minute = int(create_time_minute)
        create_time = (datetime.datetime.now() +
                       datetime.timedelta(minutes=-create_time_minute))
    elif '今天' in create_time_str:
        # 今天 22:11/今天 21:44/今天 05:11
        create_time = create_time_str.split()
        if len(create_time) == 2:
            create_time = datetime.datetime.now().strftime(
                "%Y-%m-%d ") + create_time[1] + ":00"
            create_time = datetime.datetime.strptime(create_time,
                                                     "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError
    elif '月' in create_time_str:
        # 9月21日 14:05/9月21日 03:07/9月20日 22:20/1月5日 08:39
        create_time = datetime.datetime.strptime(create_time_str,
                                                 "%m月%d日 %H:%M")
        # the year of create_time will be 1900 (default value)
        year = int(datetime.datetime.now().strftime("%Y"))
        # https://stackoverflow.com/questions/12468823/python-datetime-setting-fixed-hour-and-minute-after-using-strptime-to-get-day#comment16772522_12468869
        create_time = create_time.replace(year=year)
    else:
        # 2017-12-29 10:48/2017-12-28 10:15
        create_time = datetime.datetime.strptime(create_time_str,
                                                 "%Y-%m-%d %H:%M")
    return create_time
