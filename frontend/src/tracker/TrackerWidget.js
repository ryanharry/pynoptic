import React from 'react';
import Tracker from './Tracker.js'

export default function TrackerWidget(props) {
  return (
    <div className='tracker-container'>
      {props.tracker.map(item => (
        <Tracker key={item.id}
          item={item}
          baseUrl={props.baseUrl}
          locationId={props.locationId} />
      ))}
    </div>
  );
}
