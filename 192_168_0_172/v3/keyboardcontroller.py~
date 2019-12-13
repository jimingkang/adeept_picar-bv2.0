import keyboard
from threading import Thread

class Keyboard(Thread):

    def __init__(self):
        Thread.__init__(self)

        self.commands = {
            # First command runs on press
            # Second command runs on release
            'q': ('disconnect',''),
            'w': ('forward','coast'), #TODO: impliment coast
            's': ('reverse','coast'),
            'space': ('stop','coast'),
            '2': ('all_ahead',''),
            'a': ('left','straight'),
            'd': ('right','straight'),
            'i': ('tilt_down',''),
            'j': ('pan_left',''),
            'k': ('tilt_up',''),
            'l': ('pan_right','')
            }


        self.start()

    def run_cmd(self,cmd):  #TODO: impliment
        print(cmd)

    def run(self):
        while True:
            key = keyboard.read_event(suppress=True)
            if key.name=='esc':
                break
            
            if key.name in self.commands:
                if key.event_type=='down':
                    # on press
                    self.run_cmd(self.commands[key.name][0])
                elif key.event_type=='up':
                    # on release
                    self.run_cmd(self.commands[key.name][1])

if __name__=='__main__':
    controller = Keyboard()
