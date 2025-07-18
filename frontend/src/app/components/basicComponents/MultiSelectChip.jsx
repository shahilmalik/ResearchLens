/*
This is a React component that renders a multi-select dropdown with chips for selecting categories.
*/

"use client";
import * as React from "react";
import { useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Chip from "@mui/material/Chip";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const names = [
  "Computer Science",
  "Mathematics",
  "Statistics",
  "Economics",
  "Physics",
  "Quantitative Biology",
  "Quantitative Finance",
];

function getStyles(name, categoryName, theme) {
  return {
    fontWeight: categoryName.includes(name)
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}

export default function MultipleSelectChip({categoryChange}) {
  const theme = useTheme();
  const [categoryName, setCategoryName] = React.useState([]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setCategoryName(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
    categoryChange(value); // Call the onChange prop with the selected values
  };

  return (
    <div>
      <FormControl
        sx={{
          m: 1,
          width: 300,
          "& .MuiOutlinedInput-root": {
            borderRadius: "10px",
            "& fieldset": {
              borderRadius: "10px",
            },
            "&:hover fieldset": {
              borderColor: "black",
            }
          },
        }}
      >
        <InputLabel
          id="demo-multiple-chip-label"
          sx={{
            color: "black",
            "&.Mui-focused": { color: "black" },
          }}
        >
          Category
        </InputLabel>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={categoryName}
          onChange={handleChange}
          input={<OutlinedInput id="select-multiple-chip" label="Category" />}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {names.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, categoryName, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}
