import './App.css';
import React, { useState, useEffect } from 'react';
import dayjs from 'dayjs';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import Switch from '@mui/material/Switch';
import SimpleImageSlider from 'react-simple-image-slider';
import axios from 'axios';

function App() {
  const [statusText, setStatusText] = useState('設定してください。');
  setInterval(async () => {
    const response00 = await axios.get('http://ec2-34-224-4-175.compute-1.amazonaws.com:5000/get-status');
    setStatusText(response00.data.status_text)
  }, 5000)
  const [statusText_rmt, setStatusText_rmt] = useState('設定してください。');
  setInterval(async () => {
    const response10 = await axios.get('http://ec2-34-224-4-175.compute-1.amazonaws.com:5000/get-status_rmt');
    setStatusText_rmt(response10.data.status_text_rmt)
  }, 5000)
  const start_gameclub = async () => {
    const response01 = await fetch('http://ec2-34-224-4-175.compute-1.amazonaws.com:5000/gameclub', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ flag_gameclub: true, mode: mode_gameclub, startTime: starTime1, endTime: endTime1, select: isSwitchChecked1, play_startTime: wait_starTime1, play_endTime: wait_endTime1 })
    });
    // const json = await response01.json();
    // console.log(json);
  }
  const close_gameclub = async () => {
    const response02 = await fetch('http://ec2-34-224-4-175.compute-1.amazonaws.com:5000/gameclub_close', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ flag_gameclub: false })
    });
    // const json = await response02.json();
    // console.log(json);
  }


  const start_rmt = async () => {
    const response11 = await fetch('http://ec2-34-224-4-175.compute-1.amazonaws.com:5000/rmt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ flag_rmt: true, mode: mode_rmt, startTime: starTime2, endTime: endTime2, select: isSwitchChecked2, play_startTime: wait_starTime2, play_endTime: wait_endTime2 })
    });
    // const json1 = await response11.json();
    // console.log(json1);
  }
  const close_rmt = async () => {
    const response12 = await fetch('http://ec2-34-224-4-175.compute-1.amazonaws.com:5000/rmt_close', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ flag_rmt: false })
    });
    // const json = await response12.json();
    // console.log(json);
  }

  const [isSwitchChecked1, setIsSwitchChecked1] = useState(true);

  const handleSwitchChange1 = (event) => {
    setIsSwitchChecked1(event.target.checked);
  };

  const [isSwitchChecked2, setIsSwitchChecked2] = useState(true);

  const handleSwitchChange2 = (event) => {
    setIsSwitchChecked2(event.target.checked);
  };

  const [wait_starTime1, setWait_StartTime1] = React.useState(20);
  const [wait_endTime1, setWait_EndTime1] = React.useState(35);
  const [wait_starTime2, setWait_StartTime2] = React.useState(20);
  const [wait_endTime2, setWait_EndTime2] = React.useState(35);

  const [starTime1, setStartTime1] = React.useState(dayjs());
  
  const [endTime1, setEndTime1] = React.useState(dayjs().add(parseInt(6), 'hour'));
  const [starTime2, setStartTime2] = React.useState(dayjs());
  const [endTime2, setEndTime2] = React.useState(dayjs().add(parseInt(6), 'hour'));

  const [imageNum, setImageNum] = useState(1);
  const sliderImages_gameclub = [
    {
      url: "https://gameclub.jp/img/sliders/113.png?1685685721",
    },
    {
      url: "https://gameclub.jp/img/sliders/68.png?1671497722",
    },
    {
      url: "https://gameclub.jp/img/sliders/175.png?1694672727",
    },
    {
      url: "https://gameclub.jp/img/sliders/77.png?1694149235",
    },
  ];

  const sliderImages_rmt = [
    {
      url: "https://assets.rmt.club/img/bnr_trade%20example%20frow.png"
    },
    {
      url: "https://assets.rmt.club/img/bnr_top_payment.png"
    },
    {
      url: "https://assets.rmt.club/img/bnr_review_transfer.png"
    },
    {
      url: "https://assets.rmt.club/img/bnr_realtime_trade.png"
    },
  ]

  const [mode_gameclub, setValue] = useState('automate');
  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const [mode_rmt, setValue1] = useState('automate');
  const handleChange1 = (event) => {
    setValue1(event.target.value);
  };

  return (
    <>
      <div className='header'>
        <div className='header_content'>自    動    出    品    ツ    ー    ル</div>
      </div>
      <div className='contents'>
        <div className='frame_gameclub'>
          {/* <div> */}
          <SimpleImageSlider

            style={{ position: 'relative', borderRadius: '0.5cm' }}
            width={'100%'}
            height={'240px'}
            images={sliderImages_gameclub}
            showBullets={true}
            showNavs={true}
            autoPlay={true}
            onStartSlide={(index, length) => {
              setImageNum(index);
            }}
            autoPlayDelay={3}
          />
          {/* </div> */}
          <div className='gameclub' style={{ marginTop: '10px' }}>
            <div>
              <FormControl style={{ padding: '5px 20px 5px 20px' }}>
                <FormLabel id="mode">モード</FormLabel>
                <RadioGroup
                  row
                  aria-labelledby="mode"
                  name="row-radio-buttons-group"
                  value={mode_gameclub}
                  onChange={handleChange}
                >
                  <FormControlLabel value="automate" control={<Radio />} label="自動" style={{ marginRight: '20rem' }} />
                  <FormControlLabel value="handle" control={<Radio />} label="手動" />
                </RadioGroup>
              </FormControl>
            </div>
            <FormControl style={{ border: '#cfdcdf', borderColor: '#cfdcdf', borderStyle: 'dotted', padding: '0.5rem 1rem 0.5rem', width: '100%' }}>
              <FormLabel id='interval'>出品時間の間隔</FormLabel>
              <div style={{ display: 'flex', }}>
                <TextField
                  row
                  style={{ margin: '20px', marginBottom: '5px', width: '50%' }}
                  aria-labelledby='interval'
                  id="wait_time_start1"
                  label="分から"
                  type="number"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  value={wait_starTime1}
                  onChange={(e) => setWait_StartTime1(e.target.value)}
                />
                <TextField
                  row
                  style={{ margin: '20px', marginBottom: '5px', width: '50%' }}
                  aria-labelledby="interval"
                  id="wait_time_end1"
                  label="分まで"
                  type="number"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  value={wait_endTime1}
                  onChange={(e) => setWait_EndTime1(e.target.value)}
                />
              </div>
            </FormControl>
            <div className={isSwitchChecked1 ? 'switch_setting1 checked' : 'switch_setting1'}>
              <FormControl>
                <FormControlLabel control={<Switch checked={isSwitchChecked1} onChange={handleSwitchChange1} />} label="ツール稼働時間を設定する" labelPlacement="start" />
              </FormControl>
            </div>
            <div className={!isSwitchChecked1 ? 'set_play_time1 hidden' : 'set_play_time1'} style={{ width: '100%' }}>
              <FormControl style={{ width: '100%' }}>
                <FormLabel id='interval'>ツール稼働時間</FormLabel>
                <div style={{ padding: '20px 20px 10px 20px', display: 'flex', rowGap: '20px', flexDirection: 'column' }}>
                  <LocalizationProvider dateAdapter={AdapterDayjs} >
                    <DemoContainer components={['DateTimePicker']} >
                      <DateTimePicker
                        label="開始時間"
                        sx={{ m: '20px' }}
                        value={starTime1}
                        onChange={(newValue) => setStartTime1(newValue)}
                      />
                    </DemoContainer>
                  </LocalizationProvider>
                  <LocalizationProvider dateAdapter={AdapterDayjs} >
                    <DemoContainer components={['DateTimePicker']} >
                      <DateTimePicker
                        label="終了時間"
                        sx={{ m: '20px' }}
                        value={endTime1}
                        onChange={(newValue) => setEndTime1(newValue)}
                      />
                    </DemoContainer>
                  </LocalizationProvider>
                </div>
              </FormControl>
            </div>
            <div style={{ marginTop: '20px', display: 'flex', columnGap: '20px', flexDirection: 'row-reverse' }}>
              <button className="button button2" style={{}} onClick={close_gameclub}>　完　　了　</button>
              <button className="button button2" style={{}} onClick={start_gameclub}>　開　　始　</button>
            </div>
          </div>
          <statusbar className='status'> {statusText}</statusbar>
        </div>
        <div className='frame_rmt'>
          <SimpleImageSlider
            style={{ position: 'relative', borderRadius: '0.5cm' }}
            width={'100%'}
            height={'240px'}
            images={sliderImages_rmt}
            showBullets={true}
            showNavs={true}
            autoPlay={true}
            onStartSlide={(index, length) => {
              setImageNum(index);
            }}
            autoPlayDelay={3}
          />
          <div className='rmt' style={{ marginTop: '10px' }}>
            <FormControl style={{ padding: '5px 20px 5px 20px' }}>
              <FormLabel id="mode">モード</FormLabel>
              <RadioGroup
                row
                aria-labelledby="mode"
                name="row-radio-buttons-group"
                value={mode_rmt}
                onChange={handleChange1}
              >
                <FormControlLabel value="automate" control={<Radio />} label="自動" style={{ marginRight: '20rem' }} />
                <FormControlLabel value="handle" control={<Radio />} label="手動" />
              </RadioGroup>
            </FormControl>

            <FormControl style={{ border: '#cfdcdf', borderColor: '#cfdcdf', borderStyle: 'dotted', padding: '0.5rem 1rem 0.5rem', width: '100%' }}>
              <FormLabel id='interval'>出品時間の間隔</FormLabel>
              <div style={{ display: 'flex' }}>
                <TextField
                  row
                  style={{ margin: '20px', marginBottom: '5px', width: '50%' }}
                  aria-labelledby='interval'
                  id="wait_time_start"
                  label="分から"
                  type="number"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  value={wait_starTime2}
                  onChange={(e) => setWait_StartTime2(e.target.value)}
                />
                <TextField
                  row
                  style={{ margin: '20px', marginBottom: '5px', width: '50%' }}
                  aria-labelledby="interval"
                  id="wait_time_endt"
                  label="分まで"
                  type="number"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  value={wait_endTime2}
                  onChange={(e) => setWait_EndTime2(e.target.value)}
                />
              </div>
            </FormControl>
            <div className={isSwitchChecked2 ? 'switch_setting2 checked' : 'switch_setting2'}>
              <FormControl>
                <FormControlLabel control={<Switch checked={isSwitchChecked2} onChange={handleSwitchChange2} />} label="ツール稼働時間を設定する" labelPlacement="start" />
              </FormControl>
            </div>
            <div className={!isSwitchChecked2 ? 'set_play_time2 hidden' : 'set_play_time2'} style={{ width: '100%' }}>
              <FormControl style={{ width: '100%' }}>
                <FormLabel id='interval'>ツール稼働時間</FormLabel>
                <div style={{ padding: '20px 20px 10px 20px', display: 'flex', rowGap: '20px', flexDirection: 'column' }}>
                  <LocalizationProvider dateAdapter={AdapterDayjs} >
                    <DemoContainer components={['DateTimePicker']} >
                      <DateTimePicker
                        label="開始時間"
                        sx={{ m: '20px' }}
                        value={starTime2}
                        onChange={(newValue) => setStartTime2(newValue)}
                      />
                    </DemoContainer>
                  </LocalizationProvider>
                  <LocalizationProvider dateAdapter={AdapterDayjs} >
                    <DemoContainer components={['DateTimePicker']} >
                      <DateTimePicker
                        label="終了時間"
                        sx={{ m: '20px' }}
                        value={endTime2}
                        onChange={(newValue) => setEndTime2(newValue)}
                      />
                    </DemoContainer>
                  </LocalizationProvider>
                </div>
              </FormControl>
            </div>
            <div style={{ marginTop: '20px', display: 'flex', columnGap: '20px', flexDirection: 'row-reverse' }}>
              <button className="button button2" onClick={close_rmt}>　完　　了　</button>
              <button className="button button2" onClick={start_rmt}>　開　　始　</button>
            </div>
          </div>
          <statusbar className='status'> {statusText_rmt}</statusbar>
        </div>
      </div>
    </>
  );

}
export default App;
