import React from 'react';

export default function Weather(props) {
  return (
    <div>
      <div className='temperature-display'>
        {props.locationName}
      </div>
      <div className='weather-display'>
        {props.weather}
      </div>
      <div className='temperature-display'>
        {props.temperature}°F
      </div>
    </div>
  );
}
