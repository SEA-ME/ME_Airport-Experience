
from donkeycar.parts.controller import Joystick, JoystickController


class MyJoystick(Joystick):
    #An interface to a physical joystick available at /dev/input/js0
    def __init__(self, *args, **kwargs):
        super(MyJoystick, self).__init__(*args, **kwargs)

            
        self.button_names = {
            0x130 : 'A',
            0x131 : 'B',
            0x133 : 'X',
            0x134 : 'Y',
            0x136 : 'l1',
            0x137 : 'r1',
        }


        self.axis_names = {
            0x0 : 'hori',
            0x1 : 'vert',
        }



class MyJoystickController(JoystickController):
    #A Controller object that maps inputs to actions
    def __init__(self, *args, **kwargs):
        super(MyJoystickController, self).__init__(*args, **kwargs)


    def init_js(self):
        #attempt to init joystick
        try:
            self.js = MyJoystick(self.dev_fn)
            self.js.init()
        except FileNotFoundError:
            print(self.dev_fn, "not found.")
            self.js = None
        return self.js is not None


    def init_trigger_maps(self):
        #init set of mapping from buttons to function calls
            
        self.button_down_trigger_map = {
            'A' : self.toggle_mode,
            'B' : self.erase_last_N_records,
            'r1' : self.increase_max_throttle,
            'l1' : self.decrease_max_throttle,
            'X' : self.emergency_stop,
        }


        self.axis_trigger_map = {
            'hori' : self.set_steering,
            'vert' : self.set_throttle,
        }


