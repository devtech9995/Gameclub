import * as React from 'react';
import dayjs from 'dayjs';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';

export default function Datetime(props) {
  const { label, style, dealt} = props;
  const [value, setValue] = React.useState(dayjs().add(parseInt(dealt), 'hour'));

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      {/* <DemoContainer components={['DateTimePicker']} sx={{ '&>.MuiTextField-root': {  minWidth: '100% !important' }}}> */}
      <DemoContainer components={['DateTimePicker']} >
        <DateTimePicker
          label={label}
          sx={{m:'20px'}}
          value={value}
          onChange={(newValue) => setValue(newValue)}
        />
      </DemoContainer>
    </LocalizationProvider>
  );
}