/*
This is a React component that renders a basic date picker using MUI X Date Pickers which allows users to select the
start and end dates for a date range of publications.
*/

"use client";
import * as React from "react";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

export default function BasicDatePicker({onChange}) {
  const [selectedDate, setSelectedDate] = React.useState(null); // Store date
  const updateDate = (newValue) => {
    setSelectedDate(newValue);
    onChange(newValue);
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DemoContainer components={["DatePicker"]}>
        <DatePicker
          label="Date picker"
          value={selectedDate}
          onChange={updateDate} // Update state
        />{" "}
      </DemoContainer>
    </LocalizationProvider>
  );
}
