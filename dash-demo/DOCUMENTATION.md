# Dash Documentation

## Official Links

**Dash:** https://dash.plotly.com/
**Dash DAQ:** https://dash.plotly.com/dash-daq
**Dash Bootstrap:** https://dash-bootstrap-components.opensource.faculty.ai/
**Plotly:** https://plotly.com/python/
**Paho MQTT:** https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
**SQLAlchemy:** https://docs.sqlalchemy.org/

## Dash DAQ Components

```python
import dash_daq as daq

# Power button
daq.PowerButton(id='power', on=False, color='#2ca02c')

# LED indicator
daq.Indicator(id='led', value=True, color='#00FF00', label='Status')

# Gauge
daq.Gauge(id='gauge', min=0, max=100, value=50, showCurrentValue=True)

# Slider
daq.Slider(id='slider', min=0, max=100, value=50)

# Boolean switch
daq.BooleanSwitch(id='switch', on=True, label='Active')
```

## Bootstrap Components

```python
import dash_bootstrap_components as dbc

# Layout
dbc.Container([
    dbc.Row([
        dbc.Col([...], width=6),
        dbc.Col([...], width=6),
    ])
])

# Card
dbc.Card([dbc.CardBody([html.H4("Title"), html.P("Content")])])

# Button
dbc.Button("Click", color="primary")

# Tabs
dbc.Tabs([dbc.Tab(label="Tab 1", tab_id="1")])
```

## Plotly Charts

```python
import plotly.express as px

fig = px.line(df, x='date', y='value')       # Line
fig = px.bar(df, x='cat', y='value')         # Bar
fig = px.pie(df, values='value', names='cat') # Pie
```

## MQTT

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.example.com", 1883)
client.publish("topic", "message")
client.subscribe("topic")
client.loop_start()
```

## SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    value = Column(String)

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Use
session = Session()
session.add(Data(value='test'))
session.commit()
results = session.query(Data).all()
session.close()
```
