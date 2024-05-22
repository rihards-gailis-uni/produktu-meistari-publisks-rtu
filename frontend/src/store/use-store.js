import { create } from "zustand";

export const useStore = create((set) => ({
  category: "",
  setCategory: (category) => set({ category }),
  subCategory: "",
  setSubCategory: (subCategory) => set({ subCategory }),
  subSubCategory: "",
  setSubSubCategory: (subSubCategory) => set({ subSubCategory }),
  sortValue: "",
  setSortValue: (sortValue) => set({ sortValue }),
}));
