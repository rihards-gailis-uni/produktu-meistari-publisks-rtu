import Typography from "@mui/material/Typography";
import { css } from "@emotion/css";

const useStyles = () => {
  return {
    productWrapper: css({
      padding: 10,
      borderRadius: 8,
      backgroundColor: "rgb(245, 245, 245)",
      "@media (max-width: 768px)": {
        padding: 5,
      },
    }),
  };
};

export const PriceWrapper = ({
  name,
  priceReg,
  measurment,
  priceIn,
  measurmentIn,
  textColor,
}) => {
  const style = useStyles();
  return (
    <>
      <Typography variant="body2" color={textColor} fontWeight={600} pt={1}>
        {name}
      </Typography>
      <div className={style.productWrapper}>
        <Typography variant="body2" color={textColor} fontWeight={600}>
          {priceReg}
          {measurment !== "not_applicable" ? ` - ${measurment}` : ""}
        </Typography>

        <Typography variant="body2" color={textColor}>
          {priceIn} - {measurmentIn}
        </Typography>
      </div>
    </>
  );
};
