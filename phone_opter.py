import os
import time
import numpy as np
import cv2
from loguru import logger

# time_str = time.strftime("%Y%m%d_%H%M%S")

key_map = {
    "home":3,
    "back":4,
    "power":26,
}


passwd_ui_map = {
    "1":[1,948,239,1050],
    "2":[240,948,479,1050],
    "3":[480,948,719,1050],
}
passwd_key_map = {}

for k,v in passwd_ui_map.items():
    l,t,r,b = v
    passwd_key_map[k] = [(l+r)/2,(t+b)/2]


app_ui_map = {
    "clean":[360,442,528,624],
    "scan":[528,442,696,624],
    "pay":[18,490,702,576],
}
app_key_map = {}

for k,v in app_ui_map.items():
    l,t,r,b = v
    app_key_map[k] = [(l+r)/2,(t+b)/2]





sdcard_path = "/sdcard/_bs"



def img_compare(img1,img2):
    '''
        逐像素比对图片相似度
    '''
    diff_cnt = 0
    if img1.shape != img2.shape:
        logger.info("img shape is not same")
        logger.info(f"img1: {img1.shape}")
        logger.info(f"img2: {img2.shape}")
        return -1
    img1_flat = img1.flatten()
    img2_flat = img2.flatten()
    size = img1_flat.shape[0]
    diff_xor = np.bitwise_xor(img1_flat,img2_flat)
    diff_xor[diff_xor!=0] = 1
    diff_cnt = np.sum(diff_xor)
    return (size-diff_cnt)/size


def screenshot():
    img_dir = "dl_img"
    time_str = time.strftime("%Y%m%d_%H%M%S")
    photo_path = f"{sdcard_path}/screenshoot_{time_str}.png"
    adb_cmd = f"adb shell screencap -p {photo_path}"
    os.system(adb_cmd)

    adb_cmd = f"adb pull {photo_path} {img_dir}"
    os.system(adb_cmd)
    return f"{img_dir}/screenshoot_{time_str}.png"

def upload_img(img_path):
    adb_cmd = f"adb push {img_path} {sdcard_path}"
    os.system(adb_cmd)
    img_name = os.path.basename(img_path)
    logger.info(img_name)
    adb_cmd = f"adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{sdcard_path}/{img_name}"
    os.system(adb_cmd)

def key_input(key):
    # https://blog.csdn.net/liukang325/article/details/79268173
    adb_cmd = f"adb shell input keyevent {key_map[key]}"
    os.system(adb_cmd)

def finger_swap(start,end):
    # adb shell input swipe 250 250 300 300
    adb_cmd = "adb shell input swipe {} {} {} {}".format(*start,*end)
    os.system(adb_cmd)

def finger_tap(point):
    # adb shell input swipe 250 250 300 300
    adb_cmd = "adb shell input tap  {} {}".format(*point)
    os.system(adb_cmd)




def unlock_screen():
    key_input("power")
    time.sleep(0.5)
    # 向上滑
    finger_swap([500,1000],[500,0])


def return_home():
    key_input("home")
    time.sleep(0.1)
    key_input("home")





def passwd_input(passwd):
    for i in passwd:
        finger_tap(passwd_key_map[i])
        time.sleep(1)


def dl_uimap():
    time_str = time.strftime("%Y%m%d_%H%M%S")
    uimap_path = f"{sdcard_path}/uidump_{time_str}.xml"
    adb_cmd = f"adb shell uiautomator dump {uimap_path}"
    os.system(adb_cmd)

    adb_cmd = f"adb pull {uimap_path} dl_img"
    os.system(adb_cmd)


def wechat_pay():
    l,t,r,b = app_ui_map["pay"]
    img_pay = cv2.imread("phone_img/screen_pay.png")

    # 返回主界面
    return_home()
    time.sleep(2)
    # 一键清理
    finger_tap(app_key_map["clean"])
    time.sleep(10)
    # 打开扫一扫
    finger_tap(app_key_map["scan"])
    time.sleep(5)


    while True:
        # 判断是否可以支付
        cnt_screen = cv2.imread(screenshot())
        if img_compare(img_pay[t:b,l:r,:],cnt_screen[t:b,l:r,:]) > 0.99:
            logger.info("scan QR done")
            break
        logger.info("No QR, wait")
        time.sleep(3)
        
    # 立即支付
    logger.info("tap pay")
    finger_tap(app_key_map["pay"])
    time.sleep(1)
    passwd_input("112233")
    logger.info("pay done")

if __name__ == '__main__':
    wechat_pay()
    


    # finger_tap([(27+1053)/2,(736+866)/2])
    # dl_uimap()
    # screenshot()
    # wechat_pay()
    # passwd_input("112233")
    # finger_tap([(27+1053)/2,(736+866)/2])
    # time.sleep(1)
    # passwd_input("275991")
