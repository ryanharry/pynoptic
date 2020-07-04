import React, { useState, useEffect } from 'react';
import './App.css';
import Fullscreen from 'react-full-screen';
import Display from './Display';

export default function App() {

  const baseUrl = 'http://127.0.0.1:5555';
  const [apiKey, setApiKey] = useState('');
  const [isFull, setIsFull] = useState(false);
  const [location, setLocation] = useState({});
  const [weather, setWeather] = useState('');
  const [temperature, setTemperature] = useState('');
  const [stocks, setStocks] = useState([]);
  const [tracker, setTracker] = useState([]);
  const [time, setTime] = useState('');
  const [date, setDate] = useState('');

  useEffect(() => {
    getApiKey();
    getStocks();
    getTracker();
    getTime();
    getLocation();
    setInterval(getTime, 1000);
    setInterval(getDate, 1000);
    setInterval(getStocks, 30000);
  });

  function getWeather() {
    fetch('http://api.openweathermap.org/data/2.5/weather?id='
          + location.location  + '&units=imperial&APPID=' + apiKey, {
        method: 'GET',
      })
      .then(res => res.json())
      .then(json => {
        console.log(json)
        setWeather(json.weather[0].description);
        setTemperature(json.main.temp);
      });
    }

  function getTime() {
    let date = new Date();
    setTime(date.toLocaleTimeString());
  }

  function getDate() {
    let date = new Date();
    setDate(date.toDateString());
  }

  function getApiKey() {
    fetch(baseUrl + '/credentials', {
      method: 'GET',
    })
    .then(res => res.json())
    .then(json => {
      setApiKey(json.api_key);
    });
  }

  function getStocks() {
    fetch(baseUrl + '/stocks', {
      method: 'GET',
    })
    .then(res => res.json())
    .then(json => {
      setStocks(json);
    });
  }

  function getLocation() {
    fetch(baseUrl + '/location', {
      method: 'GET',
    })
    .then(res => res.json())
    .then(json => {
      setLocation(json);
    });
  }

  function getTracker() {
    fetch(baseUrl + '/tracker', {
      method: 'GET',
    })
    .then(res => res.json())
    .then(json => {
      setTracker(json);
    });
  }

  function goFull() {
    setIsFull(true);
    getWeather();
    setInterval(getWeather, 1800000);
  }

  return (
    <div>
      <button className='submit-button' onClick={goFull}> Launch Application </button>
      <Fullscreen enabled={isFull}onChange={isFull => setIsFull(true)}>
        <div className='full-screenable-node'>
          <Display weather={weather}
            temperature={temperature}
            locationName={location.name}
            date={date}
            time={time}
            stocks={stocks}
            tracker={tracker}
            baseUrl={baseUrl}
            locationId={location.location} />
        </div>
      </Fullscreen>
    </div>
  );
}
