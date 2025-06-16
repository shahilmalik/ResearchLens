'use client'
import React, { useState } from 'react'
import FreeSolo from './components/basicComponents/Search'
import MediaCard from './components/basicComponents/Card'
import BasicDateRangePicker from './components/basicComponents/DateRange'
import BasicDatePicker from './components/basicComponents/DateRange'
import Search from './components/basicComponents/Search'
import MultipleSelectChip from './components/basicComponents/MultiSelectChip'
import Dialogs from './components/basicComponents/DialogPage'

function page() {
 const data={
    "status": "success",
    "current_page": 1,
    "total_pages": 3,
    "total_items": 6,
    "results": [
      {
        "id": 1,
        "title": "Deep Learning for NLP",
        "abstract": "This paper explores the use of deep learning methods for NLP tasks.",
        "keywords": "deep learning, NLP, neural networks",
        "authors": ["Alice Smith", "Bob Johnson"],
        "link": "https://arxiv.org/abs/1234.5678",
        "categories": "cs.CL",
        "published_date": "2023-08-14"
      },
      {
        "id": 2,
        "title": "Quantum Algorithms in Practice",
        "abstract": "A practical approach to quantum algorithms with examples.",
        "keywords": "quantum computing, algorithms",
        "authors": ["Carol Davis"],
        "link": "https://arxiv.org/abs/2345.6789",
        "categories": "quant-ph",
        "published_date": "2023-08-15"
      }
    ]
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

export default page