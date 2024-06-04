import pyautogui
import os
import time
import subprocess
from loguru import logger

cmd_cgyy = "\"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe\" https://cgyy.buaa.edu.cn/"
cmd_order = "\"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe\" https://cgyy.buaa.edu.cn/venue/orders"
cmd_kill = "taskkill /F /IM msedge.exe"


def get_coords(img_path):
    coords = None
    for i in range(10):
        try:
            coords = pyautogui.locateOnScreen(img_path)
            logger.info(f"{img_path} success")
            break
        except pyautogui.ImageNotFoundException:
            logger.warning(f"{img_path} try {i+1} fail")
        time.sleep(1)
    return coords

def login_cgyy(name,passwd):
    subprocess.Popen(cmd_order)
    time.sleep(5)
    logger.info("start")

    # 进入统一认证
    coords = get_coords("pyautogui_img/login-01.png")
    pyautogui.leftClick(pyautogui.center(coords))
    logger.info("进入统一认证")
    time.sleep(2)


    # 登录统一认证
    coords = get_coords("pyautogui_img/login-02.png")
    x,y = pyautogui.center(coords)
    pyautogui.leftClick(x,y-125)
    logger.info("登录统一认证")
    time.sleep(2)


    pyautogui.press('shiftleft')
    pyautogui.typewrite(message=name,interval=0.1)
    pyautogui.press('tab')
    pyautogui.typewrite(message=passwd,interval=0.1)
    pyautogui.leftClick(pyautogui.center(coords))
    


def login_order():
    subprocess.Popen(cmd_order)
    time.sleep(5)

    coords = get_coords("pyautogui_img/order-01.png")
    pyautogui.leftClick(pyautogui.center(coords))
    logger.info("点击继续支付")
    time.sleep(2)


    coords = get_coords("pyautogui_img/order-02.png")
    pyautogui.leftClick(pyautogui.center(coords))
    logger.info("点击支付")
    time.sleep(2)

    coords = get_coords("pyautogui_img/order-03.png")
    pyautogui.leftClick(pyautogui.center(coords))
    logger.info("点击使用电脑支付")
    time.sleep(2)



    for img in ["pyautogui_img/order-04.png","pyautogui_img/order-05.png","pyautogui_img/order-06.png"]:
        coords = get_coords(img)
        if coords is None:
            continue
        pyautogui.leftClick(pyautogui.center(coords))
        logger.info("微信支付")
        break

if __name__ == '__main__':
    login_cgyy("ZY2103533",'CG3z56c87J7sb3')
    login_order()
    