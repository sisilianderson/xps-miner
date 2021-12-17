import logging
import time
import datetime


def switch_to_popup_wnd(driver):
    main_window_handle = get_current_wnd(driver)
    for handle in driver.window_handles:
        if handle != main_window_handle:
            signin_window_handle = handle
            break
    driver.switch_to.window(signin_window_handle)


def get_current_wnd(driver):
    return driver.current_window_handle


def is_popup_window(driver):
    # print(f"driver.window_handles {len(driver.window_handles)}")
    return True if len(driver.window_handles) == 2 else False


def switch_to_wnd(driver, wnd_handle):
    driver.switch_to.window(wnd_handle)


def wait_element_by_xpath(driver, xpath, timeout=30):
    start = datetime.datetime.now()
    element = None
    while not element:
        if (datetime.datetime.now() - start).seconds > timeout:
            break
        try:
            element = driver.find_element_by_xpath(xpath)
        except Exception:
            time.sleep(0.1)
    return element
