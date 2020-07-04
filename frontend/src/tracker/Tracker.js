import React, {useState, useEffect} from 'react';

export default function Tracker(props) {

  const [css, setCss] = useState('submit-tracker');

  useEffect(() => {
    checkStatus();
    setInterval(checkStatus, 100000);
  });

  function checkStatus() {
    const rawDate = new Date();
    fetch(props.baseUrl + '/tracker/status', {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        item_id: props.item.id,
        date: rawDate.toDateString(),
        location_id: props.locationId
      })
    }).then(res => res.json())
    .then(json => {
      setCssOnStatus(json.status);
    });
  }

  function setCssOnStatus(status) {
    if (status) {
      setCss('submit-tracker-complete');
    }
    else {
      setCss('submit-tracker');
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    const rawDate = new Date();
    fetch(props.baseUrl + '/tracker/log', {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        item_id: props.item.id,
        date: rawDate.toDateString(),
        location_id: props.locationId
      })
    }).then(res => res.json())
    .then(json => {
      setCssOnStatus(json.status);
    });
  }

  return (
    <div className='tracker-item'>
      <form onSubmit={handleSubmit}>
        <div>
          <input className={css} type="submit" value={props.item.name} />
        </div>
      </form>
    </div>
  );
}
