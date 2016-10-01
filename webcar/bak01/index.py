#!/usr/bin/python
#coding: utf8
import sys
import RPi.GPIO as GPIO
import time
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define,options
webport=3180
define("port",default=webport,type=int)
IN1 = 12
IN2 = 16
IN3 = 18
IN4 = 22
def init():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(IN1,GPIO.OUT)
        GPIO.setup(IN2,GPIO.OUT)
        GPIO.setup(IN3,GPIO.OUT)
        GPIO.setup(IN4,GPIO.OUT)

# 前进
def forward(tf):
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 后退
def reverse(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
        time.sleep(tf)
        GPIO.cleanup()

# 左转弯
def left(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 右转弯
def right(tf):
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 后左转弯
def pivot_left(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 后右转弯
def pivot_right(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
        time.sleep(tf)
        GPIO.cleanup()

# 原地左转
def p_left(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 原地右转
def p_right(tf):
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
        time.sleep(tf)
        GPIO.cleanup()
class IndexHandler(tornado.web.RequestHandler):
        def get(self):
                self.render("index.html")
        def post(self):
                init()
                sleep_time = 0.1
                arg = self.get_argument('k')
                if(arg=='w'):
                        forward(sleep_time)
                elif(arg=='s'):
                        reverse(sleep_time)
                elif(arg=='a'):
                        left(sleep_time)
                elif(arg=='d'):
                        right(sleep_time)
                elif(arg=='q'):
                        pivot_left(sleep_time)
                elif(arg=='e'):
                        pivot_right(sleep_time)
                elif(arg=='z'):
                        p_left(sleep_time)
                elif(arg=='x'):
                        p_right(sleep_time)
                else:
                        return False
                self.write(arg)
if __name__ == '__main__':
        tornado.options.parse_command_line()
        app = tornado.web.Application(handlers=[(r"/",IndexHandler)],autoreload=True)
        tornado.autoreload.start()
        tornado.autoreload.watch("index.html");
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        print 'listening in '+str(webport)
        tornado.ioloop.IOLoop.instance().start()
