import { css } from "@emotion/css";
import FoodBankIcon from "@mui/icons-material/FoodBank";

const useStyles = () => {
  return {
    wrapper: css({
      display: "flex",
      width: "100%",
      alignItems: "flex-end",
      height: 64,
      backgroundColor: "#00007d ",
    }),
    leftSide: css({
      display: "flex",
      width: "100%",
      padding: "0px 10px",
    }),
    title: css({
      display: "flex",
      alignItems: "flex-end",
      fontSize: 36,
      color: "white",
      padding: "0px 10px",
      "@media (max-width: 600px)": {
        fontSize: 24,
      },
    }),
  };
};

export const Header = () => {
  const style = useStyles();

  return (
    <div className={style.wrapper}>
      <div className={style.leftSide}>
        <FoodBankIcon sx={{ color: "white", fontSize: 54 }} />
        <div className={style.title}>Produktu Meistari</div>
      </div>
    </div>
  );
};
