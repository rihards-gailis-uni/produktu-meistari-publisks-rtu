import { useState, useEffect } from "react";
import axios from "axios";

const fetchSubProductsInfo = ({ subcategoryName, sortType }) => {
  return axios
    .get("http://localhost:5000/category/products/info", {
      params: {
        subcategory_name: subcategoryName,
        sort_type: sortType,
      },
    })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.error("Error fetching products:", error);
    });
};

export const useGetSubProductInfo = ({ subcategoryName, sortType }) => {
  const [productsInfo, setProductsInfo] = useState([]);

  useEffect(() => {
    fetchSubProductsInfo({ subcategoryName, sortType }).then(setProductsInfo);
  }, [sortType, subcategoryName]);

  return productsInfo;
};
