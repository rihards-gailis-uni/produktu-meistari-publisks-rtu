import { useState, useEffect } from "react";
import axios from "axios";

const fetchSubSubProductsInfo = ({
  subSubCategoryName,
  subCategoryName,
  sortType,
}) => {
  return axios
    .get("http://localhost:5000/category/sub_category/sub_sub_category/info", {
      params: {
        subsubcategory_name: subSubCategoryName,
        subcategory_name: subCategoryName,
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

export const useGetSubSubProductInfo = ({
  subSubCategoryName,
  subCategoryName,
  sortType,
}) => {
  const [productsInfo, setProductsInfo] = useState([]);

  useEffect(() => {
    fetchSubSubProductsInfo({
      subSubCategoryName,
      subCategoryName,
      sortType,
    }).then(setProductsInfo);
  }, [sortType, subSubCategoryName]);

  return productsInfo;
};
