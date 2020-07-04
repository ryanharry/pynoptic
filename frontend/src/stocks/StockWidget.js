import React from 'react';
import Stock from './Stock';

export default function StockWidget(props) {
  return (
    <div className='ticker-container'>
      <div className='ticker-wrap'>
        <div className='ticker-wrap ticker'>
          <div className='ticker-wrap ticker item'>
            {props.stocks.map(item => (
              <Stock key={item.id} item={item} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
