import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { CardActionArea } from "@mui/material";
import backupImage from "../../assets/image-placeholder.png";
import { capitalizeFirstLetter } from "../../helpers/capitalize-first-letter";
import { css } from "@emotion/css";
import { PriceWrapper } from "./price-wrapper";

const useStyles = () => {
  return {
    wrapper: css({
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-around",
      padding: 10,
      minHeight: 100,
      borderRadius: 8,
      backgroundColor: "rgb(245, 245, 245)",
      "@media (max-width: 768px)": {
        padding: 0,
      },
    }),
  };
};

export const ProductCard = ({
  image,
  link,
  measurment,
  measurmentIn,
  name,
  priceIn,
  priceInWithDiscount,
  priceInWithDiscountCard,
  priceRegular,
  priceRegularWithDiscount,
  priceRegularWithDiscountCard,
  retailStore,
}) => {
  const style = useStyles();
  const handleOpenLink = () => {
    window.open(link, "_blank");
  };

  if (priceIn === "nav_pieejams" || priceRegular === "nav_pieejams") {
    return null;
  }

  return (
    <Card>
      <CardActionArea
        onClick={handleOpenLink}
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          height: "100%",
        }}
      >
        <CardMedia
          component="img"
          image={image ? image : backupImage}
          alt="image"
        />

        <CardContent sx={{ width: "90%" }}>
          <div className={style.wrapper}>
            <Typography
              gutterBottom
              variant="body1"
              component="div"
              fontWeight={600}
            >
              {name}
            </Typography>

            <Typography gutterBottom variant="body2" component="div">
              {capitalizeFirstLetter(retailStore)}
            </Typography>
          </div>

          <PriceWrapper
            name="Standarta cena"
            priceReg={priceRegular}
            measurment={measurment}
            priceIn={priceIn}
            measurmentIn={measurmentIn}
            textColor="text.secondary"
          />

          {priceRegularWithDiscount && (
            <PriceWrapper
              name="Ar atlaidi"
              priceReg={priceRegularWithDiscount}
              measurment={measurment}
              priceIn={priceInWithDiscount}
              measurmentIn={measurmentIn}
              textColor="red"
            />
          )}

          {priceRegularWithDiscountCard && (
            <PriceWrapper
              name="Ar atlaižu karti"
              priceReg={priceRegularWithDiscountCard}
              measurment={measurment}
              priceIn={priceInWithDiscountCard}
              measurmentIn={measurmentIn}
              textColor="orange"
            />
          )}
        </CardContent>
      </CardActionArea>
    </Card>
  );
};
