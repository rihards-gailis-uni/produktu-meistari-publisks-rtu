import { Header } from "../components/header/header";
import { Products } from "../components/products/products";
import { Search } from "../components/search/search";

export const Main = () => {
  return (
    <div>
      <Header />
      <Search />
      <Products />
    </div>
  );
};
