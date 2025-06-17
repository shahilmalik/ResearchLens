"use client";
import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import BasicChips from "./Chip";
import { Box } from "@mui/material";
import Dialogs from "./DialogPage";

export default function MediaCard({ data, learnMore = false }) {
  const [open, setOpen] = React.useState(false);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const keywordArray = data.keywords.map((k) => k.trim());
  return (
    <Card
      sx={{
        maxWidth: 345,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        backgroundColor: "#EEEEEE",
      }}
    >
      <CardContent className="flex flex-col gap-1">
        <Typography gutterBottom variant="h5" component="div">
          {data.title}
        </Typography>
        <Typography variant="body2" sx={{ color: "text.secondary" }}>
          {data.abstract}
        </Typography>

        <Typography>
          Published on:{" "}
          <span className="font-bold text-sm text-blue-900">
            {data.published_date}
          </span>
        </Typography>
        <Typography>
          Category:{" "}
          <span className="font-bold text-sm text-blue-900">
            {data.categories}
          </span>
        </Typography>
        <Typography className="font-semibold">
          Author:{" "}
          {data.authors.map((author, index) => (
            <span key={index} className="text-sm text-blue-900 font-bold">
              {author}
              {index < data.authors.length - 1 ? ", " : ""}
            </span>
          ))}
        </Typography>
      </CardContent>
      <div className="flex flex-col">
        <div className="flex gap-1 px-4">
          {keywordArray.map((chip, index) => (
            <BasicChips key={index} label={chip} />
          ))}
        </div>
        <div className="flex w-full gap-2 p-4">
          <Button
            size="small"
            sx={{
              color: "#FF9B45",
              fontWeight: "bold",
              width: "100%",
              backgroundColor: "#333446",
            }}
            onClick={() => {
              window.open(data.link);
            }}
          >
            Learn More
          </Button>
          {learnMore && (
            <Button
              size="small"
              sx={{
                color: "#FF9B45",
                fontWeight: "bold",
                width: "100%",
                backgroundColor: "#333446",
              }}
              onClick={handleClickOpen}
            >
              Show Related
            </Button>
          )}
        </div>
      </div>
      <Dialogs open={open} setOpen={setOpen} paperId={data.id}/>
    </Card>
  );
}
