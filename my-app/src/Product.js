import React from 'react';
import { Card, CardMedia, CardContent, CardActions, Typography, IconButton } from '@material-ui/core';
import { AddShoppingCart } from '@material-ui/icons';
import axios from 'axios';


import useStyles from './prdsstyles';

const Product = ({ product}) => {
  const classes = useStyles();
  
  const handleAddToCart = () => {
    console.log("Clicked CART--------------")
    console.log(product.pid);
    axios
      .get("http://127.0.0.1:8000/clicked?itemid="+product.pid, {
        headers: { 
          'Access-Control-Allow-Origin' : '*'
        },
        responseType: "json",
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  };

  return (
    <Card className={classes.root}>
      <CardMedia component="img" width="50" height="200" className="img" image={product.purl} title={product.pname} sx={{ padding: "1em 1em 0 1em", objectFit: "contain" }}/>
      <CardContent>
        <div className={classes.cardContent}>
          <Typography gutterBottom variant="h6" component="h2">
            {product.pname}
          </Typography>
        </div>
      </CardContent>
      <CardActions disableSpacing className={classes.cardActions}>
        <IconButton aria-label="Add to Cart" onClick={handleAddToCart}>
          <AddShoppingCart />
        </IconButton>
      </CardActions>
    </Card>
  );
};

export default Product;

