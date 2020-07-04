import React from 'react';

export default function Stock(props) {
  return (
    <div className='stock-item'>
      <div className='stock-ticker'>
        {props.item.ticker}
      </div>
      <div className='stock-price'>
        {props.item.current}
      </div>
      <div className='stock-change'>
        {props.item.change} %
      </div>
    </div>
  );
}
