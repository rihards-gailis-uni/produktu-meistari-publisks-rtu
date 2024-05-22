import { useState, useEffect } from "react";
import axios from "axios";

const fetchCategories = () => {
  return axios
    .get("http://localhost:5000/category")
    .then((response) => response.data)
    .catch((error) => {
      console.error("Error fetching categories:", error);
      throw error;
    });
};

export const useGetCategories = () => {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories()
      .then((data) => setCategories(data))
      .catch((error) => console.error(error));
  }, []);

  return categories;
};
