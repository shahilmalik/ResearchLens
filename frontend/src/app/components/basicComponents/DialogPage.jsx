/*
This is a React component that renders a dialog to display related articles for a given paper. It uses the
same styling and structure as the MediaCard component, but fetches related articles from an API endpoint.
*/

"use client";
import * as React from "react";
import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import Typography from "@mui/material/Typography";
import MediaCard from "./Card";
import { useState, useEffect } from 'react'
import CircularProgress from '@mui/material/CircularProgress';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

export default function Dialogs({ open, setOpen, paperId}) {
  //   const [open, setOpen] = React.useState(false);

  //   const handleClickOpen = () => {
  //     setOpen(true);
  //   };

  const handleClose = () => {
    setOpen(false);
  };

  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(true)
  
  useEffect(() => {
    fetch(`http://localhost:8000/api/related/${paperId}/`, {method: 'GET'})
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
  }, [])

  // show spinner while loading
  if (isLoading){
    return (
    <>
      <Dialog
        PaperProps={{
          sx: {
            width: "80%",
            maxWidth: "none",
            height: "80%",
          },
        }}
        sx={{ width: "100vw" }}
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
          Related Articles
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={(theme) => ({
            position: "absolute",
            right: 8,
            top: 8,
            color: theme.palette.grey[500],
          })}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <div className="flex flex-col items-center gap-4">
            <div className="flex flex-1 items-center justify-center min-h-[60vh]">
              <div className="flex flex-col items-center gap-4">
                <CircularProgress size={100} thickness={2.0} />
                <span className="text-lg text-gray-600">Loading related articles...</span>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
  // no data found
  } else if (!data){
    return (
    <>
      <Dialog
        PaperProps={{
          sx: {
            width: "80%",
            maxWidth: "none",
            height: "80%",
          },
        }}
        sx={{ width: "100vw" }}
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
          Related Articles
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={(theme) => ({
            position: "absolute",
            right: 8,
            top: 8,
            color: theme.palette.grey[500],
          })}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <div className="flex flex-col items-center gap-4">
            <div className="flex flex-1 items-center justify-center min-h-[60vh]">
              <div className="flex flex-col items-center gap-4">
                <span className="text-lg text-gray-600">No related articles available :(</span>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
    );
  }
  return (
    <>
      <Dialog
        PaperProps={{
          sx: {
            width: "80%",
            maxWidth: "none",
            height: "80%",
          },
        }}
        sx={{ width: "100vw" }}
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
          Related Articles
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={(theme) => ({
            position: "absolute",
            right: 8,
            top: 8,
            color: theme.palette.grey[500],
          })}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <div className="gap-4 p-4">
            {data.map((data, index) => (
              // <div  >
              <MediaCard key={index} data={data} />
              // </div>
            ))}
          </div>{" "}
        </DialogContent>
      </Dialog>
    </>
  );
}
