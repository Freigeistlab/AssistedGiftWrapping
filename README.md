# Server for an assisting gift wrapping system

This system receives wrapping-orders from the [rails-dashboard](https://github.com/Freigeistlab/rails-wrapping-order-app) 
and then manages the user interaction to assist cognitively impaired people to wrap gifts. 

This is done using various Freigeist-IOT-devices 
like the [scale-unit](https://github.com/Freigeistlab/scaleUnit), lightpads and rotary-encoders as input devices and projections and an
 [led-unit](https://github.com/Freigeistlab/ledUnit) to guide the user.
 
### Installation

Make sure you have PostgreSQL installed as our tool uses a pg wrapper

On Linux systems run:

```
	sudo apt install postgresql libpq-dev
```

Afterwards install the packages using pip:

```
	pip3 install -r requirements.txt
```

### Execution
 
```
	python3 Orchestrator.py	
```

This will incidentally also start the device and order server 
on localhost:5000 to which different IOT-devices can send their state.

To see the current projections also open `Projections/index.html` in a Browser.

The format in which orders should be sent is as follows:

```javascript
	data: {
		id: <id>,
		order_products: [<item1_product_id>, <item2_product_id>, <item3_product_id>, <item4_product_id>]
	}
```
