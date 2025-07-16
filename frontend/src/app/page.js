/*
This file contains the main page of the frontend application. It includes components for searching, filtering, and displaying articles.
*/

'use client'
import React, { useState, useEffect, useRef } from 'react'
import MediaCard from './components/basicComponents/Card'
import BasicDatePicker from './components/basicComponents/DateRange'
import Search from './components/basicComponents/Search'
import MultipleSelectChip from './components/basicComponents/MultiSelectChip'
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';
import SearchIcon from '@mui/icons-material/Search';
import StartProcessingBox from './components/basicComponents/StartProcessing';

// Needed for pagination
import Pagination from '@mui/material/Pagination';
import PaginationItem from '@mui/material/PaginationItem';
import Stack from '@mui/material/Stack';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';


function Page() {
  var query = useRef("")
  var categories = useRef([])
  var startDate = useRef(null)
  var endDate = useRef(null)
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(true)

  // Load data from backend on initial render
  useEffect(() => {
    fetch("http://localhost:8000/api/paper/", {method: 'GET'})
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
      .catch(error => {
        setLoading(false)
      })
  }, [])

  // Update query when search input is changed
  function searchChange(e) {
    query.current = e.target.value
  }

  // Update category when category is changed
  function categoryChange(cat) {
    categories.current = cat
  }

  // Update query when date is changed
  function startDateChange(date) {
    startDate.current = date
  }

  // Update query when date is changed
  function endDateChange(date) {
    endDate.current = date
  }

  // Load data from backend with search parameters
  function load(page) {
    // Create search url with parameters
    const params = new URLSearchParams()
    if (page > 0) params.append('page', page)
    if (query.current) params.append('search', query.current)
    if (categories.current.length > 0) params.append('categories', categories.current.join(','))
    if (startDate.current) params.append('start_date', startDate.current.toISOString().split('T')[0])
    if (endDate.current) params.append('end_date', endDate.current.toISOString().split('T')[0])
    if (categories.current.length > 0) params.append('categories', categories.current.join(','))
    const url = `http://localhost:8000/api/paper/${params.toString() ? '?' + params.toString() : ''}`

    // Reset data and loading state
    setLoading(true)
    setData(null)

    // Fetch data from backend
    fetch(url, {method: 'GET'})
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
      .catch(error => {
        setLoading(false)
      })
  }


  return (
    <div className='p-4 flex flex-col gap-4'>
      {/* Start Processing Box */}
      <div>
        <StartProcessingBox/>
      </div>
      <hr className="my-5"/>

      {/* Search and filter components */}
      <div className='flex items-center gap-4 justify-between'>
      <Search onChange={searchChange} onEnter={() => load(0)}/>
      <BasicDatePicker label="From Date" onChange={startDateChange}/>   
      <BasicDatePicker label="To Date" onChange={endDateChange}/>   
      <MultipleSelectChip categoryChange={categoryChange}/>
      <Button
        variant="contained"
        endIcon={<SearchIcon />}
        onClick={load}>
        Search
      </Button>
      </div>
      
      {/* Show loading symbol, error message, or the retrieved papers */}
      {isLoading && !data
      ? <div className="flex flex-1 items-center justify-center min-h-[60vh]">
          <div className="flex flex-col items-center gap-4">
            <CircularProgress size={100} thickness={2.0} />
            <span className="text-lg text-gray-600">Loading articles...</span>
          </div>
        </div>
      : <div>
        {!isLoading && !data
        ? <div className="flex flex-1 items-center justify-center min-h-[60vh]">
            <div className="flex flex-col items-center gap-4">
              <span className="text-lg text-gray-600">Something went wrong. Cloud not fetch data from backend :(</span>
            </div>
          </div>
        : <div>
          <p>Found {data.total_items} articles.</p>
          <div className="gap-4 p-4">
            {data.results.length > 0
            ? data.results.map((data,index)=>(
                  <MediaCard key={index} data={data} learnMore />
            ))
            : <div className="flex flex-1 items-center justify-center min-h-[60vh]">
                <div className="flex flex-col items-center gap-4">
                  <span className="text-lg text-gray-600">No articles to show :(</span>
                </div>
              </div>
            }
          </div>
        </div>
        }
        </div>
      }
      {data
      ? <div className='flex justify-center mb-10'>
      {/* Pagination for the articles */}
      <Stack spacing={2}>
      <Pagination
        count={data.total_pages}
        size={"large"}
        page={data.current_page}
        onChange={(event, value) => load(value)}
        renderItem={(item) => (
          <PaginationItem
            slots={{ previous: ArrowBackIcon, next: ArrowForwardIcon }}
            {...item}
          />
        )}
      />
    </Stack>
    </div>
    : null
      }
    </div>
  )
}

export default Page