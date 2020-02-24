import pynput
import time


class Keyboard:
    def __init__(self):
        self._keyboard = pynput.keyboard.Controller()

    def ctrl_c(self):
        self._keyboard.press(pynput.keyboard.Key.ctrl_l)
        self._keyboard.press('c')
        self._keyboard.release('c')
        self._keyboard.release(pynput.keyboard.Key.ctrl_l)


class Mouse:
    def __init__(self, pt_stash_first, pt_stash_last, pt_inv_first, pt_inv_last):
        self._mouse = pynput.mouse.Controller()
        self._pt_stash_first = pt_stash_first
        self._x_step_stash = (pt_stash_last[0] - pt_stash_first[0]) // 11
        self._y_step_stash = (pt_stash_last[1] - pt_stash_first[1]) // 11

        self._pt_inv_first = pt_inv_first
        self._x_step_inv = (pt_inv_last[0] - pt_inv_first[0]) // 11
        self._y_step_inv = (pt_inv_last[1] - pt_inv_first[1]) // 4

    def move(self, k, stash_or_inventory):
        if stash_or_inventory == 'stash':
            x0, y0 = self._pt_stash_first
            x_step, y_step = self._x_step_stash, self._y_step_stash
            c, r = divmod(k, 12)
        elif stash_or_inventory == 'inventory':
            x0, y0 = self._pt_inv_first
            x_step, y_step = self._x_step_inv, self._y_step_inv
            c, r = divmod(k, 5)
        else:
            raise ValueError('the value of [stash_or_inventory] must be either "stash" or "inventory"')

        x = x0 + c * x_step
        y = y0 + r * y_step
        self._mouse.position = x, y

    def click(self):
        time.sleep(0.1)
        self._mouse.press(pynput.mouse.Button.left)
        time.sleep(0.05)
        self._mouse.release(pynput.mouse.Button.left)
        time.sleep(0.05)

