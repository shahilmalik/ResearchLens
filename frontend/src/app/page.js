'use client'
import React, { useState, useEffect } from 'react'
import FreeSolo from './components/basicComponents/Search'
import MediaCard from './components/basicComponents/Card'
import BasicDateRangePicker from './components/basicComponents/DateRange'
import BasicDatePicker from './components/basicComponents/DateRange'
import Search from './components/basicComponents/Search'
import MultipleSelectChip from './components/basicComponents/MultiSelectChip'
import Dialogs from './components/basicComponents/DialogPage'
import CircularProgress from '@mui/material/CircularProgress';

function Page() {
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(true)
 
  useEffect(() => {
    fetch("http://localhost:8000/api/paper/", {method: 'GET'})
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
        console.log(data)
      })
  }, [])

  // show spinner while loading
  if (isLoading){
    return (
      <div className='p-4 flex flex-col gap-4'>
      <div className='flex items-center gap-4 justify-between'>
      <Search/>   
      <BasicDatePicker label="From Date"/>   
      <BasicDatePicker label="To Date"/>
      <MultipleSelectChip/>
      </div>
      <div className="flex flex-1 items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-4">
          <CircularProgress size={100} thickness={2.0} />
          <span className="text-lg text-gray-600">Loading articles...</span>
        </div>
      </div>
      </div>
    )
  // no data found
  } else if (!data){
    return (
      <div className='p-4 flex flex-col gap-4'>
      <div className='flex items-center gap-4 justify-between'>
      <Search/>   
      <BasicDatePicker label="From Date"/>   
      <BasicDatePicker label="To Date"/>
      <MultipleSelectChip/>
      </div>
      <div className="flex flex-1 items-center justify-center min-h-[60vh]">
      <div className="flex flex-col items-center gap-4">
        <span className="text-lg text-gray-600">No articles to show :(</span>
      </div>
      </div>
      </div>
    )
  }

  return (
    <div className='p-4 flex flex-col gap-4'>
      <div className='flex items-center gap-4 justify-between'>
      <Search/>   
      <BasicDatePicker label="From Date"/>   
      <BasicDatePicker label="To Date"/>   
      {/* <BasicDatePicker/> */}
      <MultipleSelectChip/>
      </div>
      <div className='flex gap-4 p-4' >
        {data.results.map((data,index)=>(
          // <div  >
            <MediaCard key={index} data={data} learnMore />
          // </div>
        ))}
      </div>
        {/* <Dialogs open={open} setOpen={setOpen} /> */}
    </div>
  )
}

export default Page