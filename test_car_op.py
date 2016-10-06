#!/usr/bin/python
#coding:utf-8
import RPi.GPIO as GPIO
import time
import sys
#设置GPIO模式
GPIO.setmode(GPIO.BOARD)

#设置in1到in4接口
IN1 = 12
IN2 = 16
IN3 = 18
IN4 = 22

#初始化接口
def init():
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)

    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.HIGH)
    GPIO.output(IN1,GPIO.HIGH)

#前进的代码
def go_front(sleep_time):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()

#后退
def go_back(sleep_time):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(sleep_time)
    GPIO.cleanup()

#左转
def go_left(sleep_time):
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()

#右转
def go_right(sleep_time):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    time.sleep(sleep_time)
    GPIO.cleanup()

#  digitalWrite(1, LOW);digitalWrite(4,LOW);digitalWrite(5, LOW);digitalWrite(6,LOW)
def go_stop():
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    GPIO.cleanup()

if(len(sys.argv)>1):   
    op=sys.argv[1]
    runsecond=10
    if(len(sys.argv)==3):
        runsecond=sys.argv[2]
    print op
    init() 
    if(op=='front'):
        go_front(runsecond)
    if(op=='back'):
        go_back(runsecond)
    if(op=='left'):
        go_left(runsecond)
    if(op=='right'):
        go_right(runsecond)
    if(op=='stop'):
        go_stop()

