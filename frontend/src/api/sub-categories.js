import { useState, useEffect } from "react";
import axios from "axios";

const fetchCategorySubcategory = (categoryName) => {
  return axios
    .get("http://localhost:5000/category/products", {
      params: { category_name: categoryName },
    })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.error("Error fetching subcategories:", error);
    });
};

export const useGetSubCategory = (categoryName) => {
  const [subcategory, setSubcategory] = useState([]);

  useEffect(() => {
    fetchCategorySubcategory(categoryName).then(setSubcategory);
  }, [categoryName]);

  return subcategory;
};
