from flask import render_template, request, flash, redirect, url_for
import RPi.GPIO as GPIO
from app.models import LED
from app import app, db

GPIO.setmode(GPIO.BCM)
led_gpios = [26, 20, 21]
GPIO.setup(led_gpios, GPIO.OUT)

for gpio in led_gpios:
    newled = LED(gpionumber = gpio, state = 0)
    try:
        db.session.add(newled)
        db.session.commit()
    except:
        print("gpio exists in db")

@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return render_template('index.html', title='Homepage')

@app.route('/gpio', methods=['GET'])
def gpio():
    leds = LED.query.order_by(LED.id).all()
    return render_template('gpio.html', title='gpio', leds=leds)

@app.route('/gpio/<gpionumber>', methods=['GET', 'POST'])
def gpio_bynumber(gpionumber):
    
    leds = LED.query.order_by(LED.id).all()

    for led in leds:
        if int(gpionumber) == led.gpionumber:
            if request.method == 'GET':
                return str(led.state)
            elif request.method == 'POST':
                led.state = not led.state
                GPIO.output(led.gpionumber, led.state)
                try:
                    db.session.commit()
                except:
                    flash("There was an issue updating LED-state")
                    return "There was an issue updating LED-state"
                flash('Succesfully toggled LED{}'.format(led.gpionumber))
                return redirect(url_for('gpio'))

    flash('No such GPIO number {}'.format(gpionumber))

    return render_template('gpio.html', title='gpio', leds=leds)