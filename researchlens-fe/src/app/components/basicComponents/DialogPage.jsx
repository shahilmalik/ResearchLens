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

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

export default function Dialogs({ open, setOpen }) {
  //   const [open, setOpen] = React.useState(false);

  //   const handleClickOpen = () => {
  //     setOpen(true);
  //   };

  const handleClose = () => {
    setOpen(false);
  };

  console.log("Dialog component render - open state:", open);
  const data = {
    status: "success",
    current_page: 1,
    total_pages: 3,
    total_items: 6,
    results: [
      {
        id: 1,
        title: "Deep Learning for NLP",
        abstract:
          "This paper explores the use of deep learning methods for NLP tasks.",
        keywords: "deep learning, NLP, neural networks",
        authors: ["Alice Smith", "Bob Johnson"],
        link: "https://arxiv.org/abs/1234.5678",
        categories: "cs.CL",
        published_date: "2023-08-14",
      },
      {
        id: 2,
        title: "Quantum Algorithms in Practice",
        abstract: "A practical approach to quantum algorithms with examples.",
        keywords: "quantum computing, algorithms",
        authors: ["Carol Davis"],
        link: "https://arxiv.org/abs/2345.6789",
        categories: "quant-ph",
        published_date: "2023-08-15",
      },
    ],
  };
  return (
    <>
      <Dialog
        PaperProps={{
          sx: {
            width: "80%", // ✅ Set custom width here
            maxWidth: "none", // ✅ Prevent MUI's default max-width limit
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
          <div className="flex gap-4 p-4">
            {data.results.map((data, index) => (
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
