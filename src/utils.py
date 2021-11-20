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


# def ready_to_mine(account, config, verbose=False):
#     stater = PickleSaver(account_name=account, main_cfg=config)
#     if not stater.is_account():
#         stater.create_account()
#     if stater.is_account() and stater.get_login_status() > 3:
#         return False
#     if stater.is_account() and stater.get_chilled_status():
#         delay = stater.get_chilled_delay()
#         logging.info(f"This account is relaxing another {delay} seconds")
#         if verbose:
#             print(f"This account is relaxing another {delay} seconds")
#         chilled_time = (datetime.datetime.now() - stater.get_chilled_time()).seconds
#
#         if chilled_time > delay:
#             logging.info(f"Rest time elapsed time to mine")
#             if verbose:
#                 print(f"Rest time elapsed time to mine")
#             stater.set_chilled_time(0)
#             stater.set_chilled_status(0)
#             stater.set_chilled_delay(0)
#             return True
#         else:
#             logging.info(f"wait another {delay - chilled_time} seconds")
#             if verbose:
#                 print(f"wait another {delay - chilled_time} seconds")
#             stater.set_chilled_time(datetime.datetime.now())
#             stater.set_chilled_status(1)
#             stater.set_chilled_delay(delay - chilled_time)
#             time.sleep(5)
#             return False
#     return True
