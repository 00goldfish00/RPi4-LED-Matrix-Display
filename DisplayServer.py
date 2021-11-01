#########
# Team name: El Double-E Dee
# Student names: Daniel Parrish, Samson Segovia
# Course: COSC 4973 Section 01 – Pi & Python
# Assignment: Semester Project
# Filename: DispalyServer.py
#
# Purpose: 
#
# Input: 
#
# Output: 
#
# Assumptions: 
#
# Limitations: 
#
# Development Computer: Raspberry Pi
# Operating System: Raspbian
# Compiler: Python 3.9.1
# Integrated Development Environment (IDE): VSCode
# Operational Status: WIP
#########

from tkinter import *
import http.server
import cgi
from os import curdir, sep
import RPi.GPIO as IO
from threading import *
import atexit

# setup port and localhost
PORT = 8000
HOST = '0.0.0.0'

RPIN = 11
GPIN = 13
BPIN = 15

# handler class for the server get and post functions
class MyHandler(http.server.BaseHTTPRequestHandler):
    # bring in gui to use its RGB color settings
    global gui

    # handler for GET requests
    def do_GET(self):
        
        if self.path == "/" or self.path == "/send":
            self.path = "DisplayControlPage.html"
        
        try:
            send_reply = False
            
            if self.path.endswith('.html'):
                mime_type = 'text/html'
                send_reply = True
                
            if send_reply:
                print("Opening", curdir + sep + self.path)
                f = open(curdir + sep + self.path)
                
                self.send_response(200)
                self.send_header('content-type', mime_type)
                self.end_headers()
                self.wfile.write(f.read().encode())
                
                # create HTML code with updated slider and status variable to be sent back to web page
                body = ('<form action="/send_color" method="post">\n'
                                f'<input type="range" name="r_range" min="0" max="100" value="{gui.r_val.get()}" />\n'
                                '<label>Red</label><br>\n'
                                f'<input type="range" name="g_range" min="0" max="100" value="{gui.g_val.get()}" />\n'
                                '<label>Green</label><br>\n'
                                f'<input type="range" name="b_range" min="0" max="100" value="{gui.b_val.get()}" />\n'
                                '<label>Blue</label><br>\n'
                                '<input type="submit" name="color" value="Send Color" />\n'
                            '</form>\n'
                            '<form action="/send_toggle" method="post">\n'
                                f'<input type="submit" name="toggle" value="Display is {"OFF" if gui.led_state.get() == 0 else "ON"}" />\n'
                            '</form>\n'
                            '<form action="/" method="post">\n'
                                '<input type="submit" value="Update Page" />\n'
                            '</form>\n'
                            '</body>\n'
                            '</html>')
                
                self.wfile.write(body.encode())
                f.close()
                
            return
        
        except IOError:
            self.send_error(404, 'file not found: %s' % self.path)
                
    
    def do_POST(self):

        # call empty do_GET to update web page variables if update page button was pressed
        if self.path == "/":
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {
                "REQUEST_METHOD":"POST",
                "CONTENT_TYPE":self.headers["Content-Type"]
            })

            self.do_GET()
            return
        
        # update gui RGB value if send color button was pressed
        if self.path == "/send_color":
            self.path = "/"
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {
                "REQUEST_METHOD":"POST",
                "CONTENT_TYPE":self.headers["Content-Type"]
            })
            
            if form["color"].value == "Send Color":
                gui.r_val.set(form["r_range"].value)
                gui.g_val.set(form["g_range"].value)
                gui.b_val.set(form["b_range"].value)
            
            self.do_GET()
            return

        # toggle led state variable if toggle button was pressed
        if self.path == "/send_toggle": 
            self.path = "/"
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {
                "REQUEST_METHOD":"POST",
                "CONTENT_TYPE":self.headers["Content-Type"]
            })
            
            if form["toggle"].value == "TOGGLE LED":
               gui.toggle_led()
            
            self.do_GET()
            return

'''Needs to be removed. First find a way to replace: led_state, r_val, g_val, b_val'''
class GUI():
    # initialize GUI window, sliders, and buttons
    def __init__(self, root):
        root.title('Auto-Home')
        root.geometry('720x400')
        self.create_widgets(root)

    # method to toggle the LED state and update GUI text
    def toggle_led(self, channel=None):
        if self.led_state.get() == 1:
            self.led_state.set(0)
        else:
            self.led_state.set(1)
        self.led_text.set('LED is {0}'.format('OFF' if self.led_state.get() == 0 else 'ON'))
    
    # method to add all the sliders and button to the GUI
    def create_widgets(self, root):
        root.columnconfigure(0, weight=1)
        for i in range(5):
            root.rowconfigure(i, weight=1)
    
        self.r_val = IntVar()
        self.r_scale = Scale(root, activebackground='#AA0000', bg='#EB3434', label='Red', orient=HORIZONTAL, variable=self.r_val)
        self.r_scale.grid(row=0, sticky=N+E+S+W)

        self.g_val = IntVar()
        self.g_scale = Scale(root, activebackground='#00AA00', bg='#34EB34', label='Green', orient=HORIZONTAL, variable=self.g_val)
        self.g_scale.grid(row=1, sticky=N+E+S+W)

        self.b_val = IntVar()
        self.b_scale = Scale(root, activebackground='#0000AA', bg='#3434EB', label='Blue', orient=HORIZONTAL, variable=self.b_val)
        self.b_scale.grid(row=2, sticky=N+E+S+W)
        
        self.led_state = IntVar()
        self.led_state.set(1)
        self.led_text = StringVar()
        self.led_text.set('LED is {0}'.format('ON' if self.led_state.get() == 1 else 'OFF'))
        self.led_btn = Button(root, textvariable=self.led_text, command=self.toggle_led)
        self.led_btn.grid(row=3, sticky=W+E)

# method recieves server object and starts it
def run_server(html_server):
    try:
        print("Started on port: %d" % PORT)
        html_server.serve_forever()
        
    except KeyboardInterrupt:
        print(" recieved, shutting down server")
    finally:
        print('Running socket cleanup')
        html_server.socket.close()

# method that updates the RGB LED output
def update_dispaly():
    global gui
    while True:
        if gui.led_state.get() == 1:
            r_pwm.ChangeDutyCycle(gui.r_val.get())
            g_pwm.ChangeDutyCycle(gui.g_val.get())
            b_pwm.ChangeDutyCycle(gui.b_val.get())
        else:
            r_pwm.ChangeDutyCycle(0)
            g_pwm.ChangeDutyCycle(0)
            b_pwm.ChangeDutyCycle(0)

# method is called when GUI is closed to clean up the program
def exit_protocall():
    print('Running GPIO cleanup')
    IO.cleanup()
    print('Running socket cleanup')
    my_server.socket.close()

# main code body
if __name__ == '__main__':
    
    # create GUI object
    window = Tk()
    gui = GUI(window)
    
    # setup board pins and interrupts
    IO.setmode(IO.BOARD)
    IO.setwarnings(False)

    IO.setup(RPIN, IO.OUT)
    IO.setup(GPIN, IO.OUT)
    IO.setup(BPIN, IO.OUT)

    # initialize PWM to zero
    r_pwm = IO.PWM(RPIN, 60) # pin, Hz
    r_pwm.start(0)
    g_pwm = IO.PWM(GPIN, 60) # pin, Hz
    g_pwm.start(0)
    b_pwm = IO.PWM(BPIN, 60) # pin, Hz
    b_pwm.start(0)

    # create and start thread to update the LED
    gpio_thread = Thread(target=update_dispaly)
    gpio_thread.daemon = True
    gpio_thread.start()

    # create and start thread to run the server
    my_server = http.server.HTTPServer((HOST, PORT), MyHandler)
    server_thread = Thread(target=run_server, args=(my_server,))
    server_thread.daemon = True
    server_thread.start()
    
    # start GUI in main thread
    window.mainloop()
    # register cleanup method to be called when exiting
    atexit.register(exit_protocall)
