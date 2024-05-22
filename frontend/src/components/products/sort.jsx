import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import { useStore } from "../../store/use-store";

export const Sort = () => {
  const { sortValue, setSortValue } = useStore();

  const options = [
    {
      value: "cenaAugosa",
      label: "Kārtot pēc €/gab augošā secībā",
    },
    {
      value: "cenaDilstosa",
      label: "Kārtot pēc €/gab dilstošā secībā",
    },
    {
      value: "cenaKgAugosa",
      label: "Kārtot pēc €/kg augošā secībā",
    },
    {
      value: "cenaKgDilstosa",
      label: "Kārtot pēc €/kg dilstošā secībā",
    },
  ];

  const handleSortingChange = (event) => {
    setSortValue(event.target.value);
  };

  return (
    <FormControl sx={{ margin: 1, minWidth: 240, maxWidth: 300 }}>
      <InputLabel>Izvēlies kārtošanas opciju</InputLabel>
      <Select
        value={sortValue}
        label="Izvēlies kārtošanas opciju"
        onChange={handleSortingChange}
      >
        {options.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};
