from constants import *
from pymycobot import MyCobot280
import utils as u
import time

class Arm(MyCobot280):
    def __init__(self, port, baudrate="115200", timeout=0.1, debug=False, thread_lock=True):
        super().__init__(port, baudrate, timeout, debug, thread_lock)
        
    def INIT(self):
        self.PumpOff()
        self.Forward(DEFAULT_COORD)
        
    def GET(self, pixel_x, pixel_y):
        x, y = u.Pixel2Coord(pixel_x, pixel_y)
        self.Forward([x, y, PUMP_Z_1, *PUMP_ANGLE])
        self.PumpOn()
        self.Forward([x, y, PUMP_Z_2, *PUMP_ANGLE], speed=PUMP_SPEED)
        time.sleep(PUMP_TIME_1)
        self.Forward([x, y, PUMP_Z_3, *PUMP_ANGLE])
        # self.Forward(COORDS['c'][0])
        self.Forward(TRANSIT_COORD)
        return

    def PUT(self, tag):
        self.Forward(COORDS[tag][0])
        # self.Forward(COORDS[tag][1])
        self.PumpOff()
        time.sleep(PUMP_TIME_2)
        # self.Forward(COORDS[tag][0])
        self.Forward(MIDDLE_COORD)
        
    def PumpOn(self):
        for i in PUMP_PORT:
            self.set_basic_output(i, 0)
    
    def PumpOff(self):
        for i in PUMP_PORT:
            self.set_basic_output(i, 1)
            
    def Forward(self, coords, speed=DEFAULT_SPEED):
        print(f"Forward {coords=}")
        print("-------------------------")
        assert len(coords) == 6 , "Invalid position or angle"
        self.send_coords(coords, speed, COORD_MODE)
        start = time.time()
        try:
            while u.Cmp(self.get_coords()[:3], coords[:3]) > DELTA:
                if time.time() - start > FORWARD_TIME:
                    return FAILURE
                time.sleep(0.1)
            return SUCCESS
        except Exception as e:
            print(e)
            return EXCEPTION

if __name__ == "__main__":
    arm = Arm('COM9')
    # arm.INIT()
    # arm.GET(1, 0.5)
    # arm.PUT('ur')

    arm.release_all_servos()
    print(arm.get_coords())