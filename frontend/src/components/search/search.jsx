import { css } from "@emotion/css";
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import { useGetCategories } from "../../api/categories";
import { useGetSubCategory } from "../../api/sub-categories";
import { useGetSubSubCategory } from "../../api/sub-sub-categories";
import { useStore } from "../../store/use-store";

const useStyles = () => {
  return {
    wrapper: css({
      margin: 20,
      padding: 20,
      border: "2px solid #a5a5a5",
      borderRadius: 8,
      backgroundColor: "rgb(245, 245, 245)",
      "@media (max-width: 768px)": {
        margin: 5,
      },
    }),
    searchWrapper: css({
      display: "flex",
      flexDirection: "column",
    }),
  };
};

export const Search = () => {
  const style = useStyles();
  const {
    category,
    setCategory,
    subCategory,
    setSubCategory,
    subSubCategory,
    setSubSubCategory,
  } = useStore();

  const categoryItems = useGetCategories();
  const subcategoryItems = useGetSubCategory(category);
  const subSubCategoryItems = useGetSubSubCategory(subCategory);

  const handleCategoryChange = (event) => {
    setCategory(event.target.value);

    if (category !== "") {
      setSubCategory("");
      setSubSubCategory("");
    }
  };

  const handleSubcategoryChange = (event) => {
    setSubCategory(event.target.value);
    setSubSubCategory("");
  };

  const handleSubSubCategoryChange = (event) => {
    setSubSubCategory(event.target.value);
  };

  return (
    <div className={style.wrapper}>
      <Typography variant="h5" pb={2}>
        Atrodi produktu
      </Typography>

      <div className={style.searchWrapper}>
        <FormControl fullWidth sx={{ margin: 1 }}>
          <InputLabel>Izvēlēties kategoriju</InputLabel>
          <Select
            value={category}
            label="Izvēlēties kategoriju"
            onChange={handleCategoryChange}
          >
            {categoryItems.map((item) => (
              <MenuItem key={item.value} value={item.value}>
                {item.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth sx={{ margin: 1 }}>
          <InputLabel>Izvēlēties apakškategoriju</InputLabel>
          <Select
            label="Izvēlēties apakškategoriju"
            value={subCategory}
            disabled={!category}
            onChange={handleSubcategoryChange}
          >
            {subcategoryItems.map((item) => (
              <MenuItem key={item.sub_category} value={item.sub_category}>
                {item.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth sx={{ margin: 1 }}>
          <InputLabel>Izvēlēties apakšapakškategoriju</InputLabel>
          <Select
            label="Izvēlēties apakšapakškategoriju"
            value={subSubCategory}
            disabled={!subCategory || subSubCategoryItems?.length === 0}
            onChange={handleSubSubCategoryChange}
          >
            {subSubCategoryItems &&
              subSubCategoryItems.map((item) => (
                <MenuItem
                  key={item.sub_sub_category}
                  value={item.sub_sub_category}
                >
                  {item.label}
                </MenuItem>
              ))}
          </Select>
        </FormControl>
      </div>
    </div>
  );
};
