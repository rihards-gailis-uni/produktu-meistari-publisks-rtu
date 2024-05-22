import { css } from "@emotion/css";
import { Typography } from "@mui/material";
import { ProductCard } from "./product-card";
import { Sort } from "./sort";
import { useStore } from "../../store/use-store";
import { useGetSubProductInfo } from "../../api/sub-product-info";
import { useGetSubSubProductInfo } from "../../api/sub-sub-product-info";

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
        padding: 5,
      },
    }),
    productWrapper: css({
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr 1fr 1fr 1fr",
      gap: 20,
      "@media (max-width: 768px)": {
        gridTemplateColumns: "1fr 1fr",
        rowGap: 20,
        columnGap: 5,
      },
    }),
    top: css({
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      paddingBottom: 10,
      "@media (max-width: 768px)": {
        alignItems: "flex-start",
        flexDirection: "column",
        padding: 10,
      },
    }),
  };
};

export const Products = () => {
  const style = useStyles();

  const { subCategory, subSubCategory, sortValue } = useStore();

  let products = [];

  if (!subSubCategory) {
    products = useGetSubProductInfo({
      subcategoryName: subCategory,
      sortType: sortValue || "",
    });
  } else {
    products = useGetSubSubProductInfo({
      subCategoryName: subCategory,
      subSubCategoryName: subSubCategory,
      sortType: sortValue || "",
    });
  }
  console.log(sortValue);

  if (!products || products?.length === 0) {
    return null;
  }

  return (
    <div className={style.wrapper}>
      <div className={style.top}>
        <Typography variant="h5">Atrastie produkti</Typography>
        <Sort />
      </div>
      <div className={style.productWrapper}>
        {products.map((product) => (
          <ProductCard
            key={product.link}
            name={product.name}
            link={product.link}
            image={product.image}
            priceRegular={product.price_regular}
            measurment={product.measurment}
            priceIn={product.price_in}
            measurmentIn={product.measurment_in}
            priceInWithDiscount={product.price_in_with_discount}
            priceInWithDiscountCard={product.price_in_with_discount_card}
            priceRegularWithDiscount={product.price_regular_with_discount}
            priceRegularWithDiscountCard={
              product.price_regular_with_discount_card
            }
            retailStore={product.retail_store}
          />
        ))}
      </div>
    </div>
  );
};
