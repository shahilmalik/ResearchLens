/*
This is a React component that renders an information text and a button to start processing data.
*/

import React from "react";
import { Box, Typography, TextField, Button, Paper } from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import MultipleSelectChip from './MultiSelectChip'
import DownloadIcon from '@mui/icons-material/Download';

function StartProcessingBox({onChange, onEnter}) {
  const [numberOfArticles, setNumberOfArticles] = React.useState(10);
  const [categories, setCategories] = React.useState([]);

  // Map of categories to their corresponding arXiv identifiers
  const ARXIV_CATEGORY_MAP = {
    'Computer Science': 'cs',
    'Mathematics': 'math',
    'Statistics': 'stat',
    'Economics': 'econ',
    'Physics': 'physics',
    'Quantitative Biology': 'q-bio',
    'Quantitative Finance': 'q-fin'
  }

  // Start processing with the given number of articles by calling the backend API
  const load = () => {
    // Construct the URL parameters for the API call
    const params = new URLSearchParams({"number_articles": numberOfArticles})
    if (categories.length > 0) params.append('categories', categories.map(cat => ARXIV_CATEGORY_MAP[cat]).join(','))
    
    fetch(`http://localhost:8000/api/start-preprocess/?${params.toString()}`, {
      method: "POST",
    }).then((res) => res.json())
      .then((data) => {
        console.log("Processing started:", data);
    })
  }

  return (
    <Box>
      { /* Information text about the scaping and processing steps */ }
      <Paper
        elevation={3}
        sx={{
          display: "flex",
          alignItems: "center",
          padding: 2,
          marginBottom: 2,
          backgroundColor: "#e3f2fd",
        }}
      >
        <InfoOutlinedIcon color="info" sx={{ marginRight: 1 }} />
        <Typography variant="body1">
          To use the application, you have to either manually import data to the database using the provided SQL files
          or start the collection and preparing process with the application. The collection and preparing process can
          take a while because the preparing step involves computing keywords and embeddings for each abstract, which
          uses deep learning models that run on the CPU. Additionally, the application will download the model's weights
          during the first call which also takes some time. Our application uses SentenceTransformers to compute embeddings
          and KeyBERT to compute keywords.
        </Typography>
      </Paper>
      { /* Form with number of articles and categories */ }
      <div className='flex items-center gap-4'>
        <MultipleSelectChip categoryChange={(e) => setCategories(e)}/>
        <TextField
            value={numberOfArticles}
            id="outlined-number"
            label="Number of articles"
            type="number"
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
            onChange={(e) => setNumberOfArticles(e.target.value)}
          />
        <Button variant="contained" color="primary" onClick={load} endIcon={<DownloadIcon />}>
          Scrape and Prepare
        </Button>
      </div>
    </Box>
  );
}

export default StartProcessingBox;
