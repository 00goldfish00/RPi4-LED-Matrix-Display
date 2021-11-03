#########
# Student name: Daniel Parrish
# Course: COSC 4973 Section 01 – Pi & Python
# Assignment: Semester Project
# Filename: control_server.py
#
# Purpose: To run an HTML server displaying controls for the 2D LED matrix
#
# Input: HTML forms using post
#
# Output: Audio visualization, colors, and patterns on LED matrix
#
# Assumptions: 
#
# Limitations: 
#
# Development Computer: Desktop
# Operating System: Windows 10
# Compiler: Python 3.9.1
# Integrated Development Environment (IDE): VSCode
# Operational Status: WIP
#########

import http.server
import cgi
from os import curdir, sep
import RPi.GPIO as IO
from threading import *
import atexit


# handler class for the server get and post functions
class MyHandler(http.server.BaseHTTPRequestHandler):

    # handler for GET requests
    def do_GET(self):
        
        if self.path == "/" or self.path == "/send":
            self.path = "TESTWebPage.html"
        
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
                                f'<input type="range" name="r_range" min="0" max="100" value="{r_val}" />\n'
                                '<label>Red</label><br>\n'
                                f'<input type="range" name="g_range" min="0" max="100" value="{g_val}" />\n'
                                '<label>Green</label><br>\n'
                                f'<input type="range" name="b_range" min="0" max="100" value="{b_val}" />\n'
                                '<label>Blue</label><br>\n'
                                '<input type="submit" name="color" value="Send Color" />\n'
                            '</form>\n'
                            '<form action="/send_toggle" method="post">\n'
                                '<input type="submit" name="toggle" value="TOGGLE LED" />\n'
                            '</form>\n'
                            f'<p>LED is {"OFF" if led_state else "ON"}</p>\n'
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

        #global r_val, g_val, b_val, led_state

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
                r_val = form["r_range"].value
                g_val = form["g_range"].value
                b_val = form["b_range"].value
            
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
               led_state = not led_state
            
            self.do_GET()
            return


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
def run_gpio():
    while True:
        if led_state:
            data_pwm.ChangeDutyCycle(r_val)
        else:
            data_pwm.ChangeDutyCycle(0)


# method is called when GUI is closed to clean up the program
def exit_protocall():
    print('Running GPIO cleanup')
    IO.cleanup()
    print('Running socket cleanup')
    server.socket.close()


# main code body
if __name__ == '__main__':
    
    # setup port and localhost
    PORT = 8000
    HOST = '0.0.0.0'
    
    # setup pin names
    DATA_PIN = 11

    # init color values to black and LED strip to off
    r_val = 0
    g_val = 0
    b_val = 0
    led_state = False

    # setup board pins and interrupts
    IO.setmode(IO.BOARD)
    IO.setwarnings(False)

    # init pins to output
    IO.setup(DATA_PIN, IO.OUT)

    # init PWM objects to zero
    data_pwm = IO.PWM(DATA_PIN, 60) # (pin, Hz)
    data_pwm.start(0)
    
    # create and start thread to update the LEDs
    gpio_thread = Thread(target=run_gpio)
    gpio_thread.daemon = True
    gpio_thread.start()

    # create and start thread to run the server
    server = http.server.HTTPServer((HOST, PORT), MyHandler)
    server_thread = Thread(target=run_server, args=(server,))
    server_thread.daemon = True
    server_thread.start()
    
    # register cleanup method to be called when exiting
    atexit.register(exit_protocall)
