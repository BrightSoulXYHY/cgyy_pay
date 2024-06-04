from edge_operater import login_cgyy,login_order
from phone_opter import wechat_pay

import time
from loguru import logger

pay_users = [
    {
        "name":"ZY2103533",
        "passwd":"CG3z56c87J7sb3",
    }
]


if __name__ == '__main__':
    start_time = time.strptime(time.strftime('07:03:00', time.localtime()), '%H:%M:%S')
    end_time = time.strptime(time.strftime('07:08:00', time.localtime()), '%H:%M:%S')
    logger.info("等待中")
    
    while True:
        cnt_time = time.strptime(time.strftime('%H:%M:%S', time.localtime()), '%H:%M:%S')    
        if start_time < cnt_time < end_time:
            break
        time.sleep(1)

    logger.info("开始付款！")
    for pay_user in pay_users:
        login_cgyy(**pay_user)
        login_order()
        time.sleep(5)
        wechat_pay()