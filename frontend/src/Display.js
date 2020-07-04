import React from 'react';
import DateDisplay from './date/DateDisplay';
import StockWidget from './stocks/StockWidget';
import Time from './time/Time';
import TrackerWidget from './tracker/TrackerWidget';
import Weather from './weather/Weather';

export default function Display(props) {
  return (
    <div className='app-grid'>
      <div className='weather'>
        <Weather weather={props.weather}
          temperature={props.temperature}
          locationName={props.locationName}/>
      </div>
      <div className='date'>
        <DateDisplay date={props.date}/>
      </div>
      <div className='time'>
        <Time time={props.time}/>
      </div>
      <div className='stocks'>
        <StockWidget stocks={props.stocks}/>
      </div>
      <div className='tracker-header'>
        <div>
          Lifestyle
        </div>
        <div>
          Tracker
        </div>
      </div>
      <div className='tracker'>
        <TrackerWidget tracker={props.tracker}
          baseUrl={props.baseUrl}
          locationId={props.locationId}/>
      </div>
    </div>
  );
}
