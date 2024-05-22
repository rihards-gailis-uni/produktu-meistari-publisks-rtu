import { useState, useEffect } from "react";
import axios from "axios";

const fetchSubSubcategory = (subCategoryName) => {
  return axios
    .get("http://localhost:5000/category/sub_category/sub_sub_category", {
      params: { subcategory_name: subCategoryName },
    })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.error("Error fetching subsubcategories:", error);
    });
};

export const useGetSubSubCategory = (subCategoryName) => {
  const [subSubCategory, setSubSubcategory] = useState([]);

  useEffect(() => {
    fetchSubSubcategory(subCategoryName).then(setSubSubcategory);
  }, [subCategoryName]);

  return subSubCategory;
};
