import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import Product from './Product';
import useStyles from './prdstyles';


// class Search extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       value: 'Please write an essay about your favorite DOM element.'
//     };

//     this.handleChange = this.handleChange.bind(this);
//     this.handleSubmit = this.handleSubmit.bind(this);
//   }

//   useEffect(() => {
//     fetch('http://127.0.0.1:8000/recommend')
//       .then(response => response.json())
//       .then(json => setData(json))
//       .catch(error => console.error(error));
//   }, []);


//   handleChange(event) {
//     this.setState({value: event.target.value});
//   }

//   handleSubmit(event) {
//     alert('An essay was submitted: ' + this.state.value);
//     event.preventDefault();
//   }

//   render() {
//     return (
//       <form onSubmit={this.handleSubmit}>
//         <label>
//           Essay:
//           <textarea value={this.state.value} onChange={this.handleChange} />
//         </label>
//         <input type="submit" value="Submit" />
//       </form>
//       <div>
//       {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
//     </div>
//     );
//   }
// }

// function Search() {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetch('http://127.0.0.1:8000/recommend')
//       .then(response => response.json())
//       .then(json => setData(json))
//       .catch(error => console.error(error));
//   }, []);

//   return (
//     <div>
//       {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
//     </div>
//   );
// }

// function Search() {
//   const [data, setData] = useState(null);

//   function handleClick() {
//     const xhr = new XMLHttpRequest();
//     xhr.open('GET', 'http://127.0.0.1:8000/recommend');
//     xhr.onload = function() {
//       if (xhr.status === 200) {
//         console.log(xhr.status);
//         console.log(xhr.responseText)
//         setData(JSON.parse(xhr.responseText));
//       }
//     };
//     xhr.send();
//   }

//   const response = fetch('http://127.0.0.1:8000/recommend', {
//     method: 'GET',
//     mode: 'cors'
//   })
//   console.log(response.json())


//   return (
//     <div>
//       <button onClick={handleClick}>Get Data</button>
//       {data ? <div>{JSON.stringify(data)}</div> : <div>Loading...</div>}
//     </div>
//   );
// }


function Search() {
  const [products1, setProducts1] = useState([]);
  const [products2, setProducts2] = useState([]);
  const [products3, setProducts3] = useState([]);
  const [searchres, setSearchProducts] = useState([]);

  useEffect(() => {
    // axios.get('http://127.0.0.1:8000/recommend')
    axios
      .get("http://127.0.0.1:8000/recommend", {
        headers: { 
          'Access-Control-Allow-Origin' : '*'
        },
        responseType: "json",
      })
      .then(response => {
        console.log(response.data);
        setProducts1(response.data[0]);
        setProducts2(response.data[1]);
        setProducts3(response.data[2]);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target;
    const formData = new FormData(form);

    // You can pass formData as a fetch body directly:
    // fetch('/some-api', { method: form.method, body: formData });

    console.log(form);
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson);
    console.log('http://127.0.0.1:8000/search?text='+formJson.postContent);
    // fetch('http://127.0.0.1:8000/search?text='+formJson.postContent)
    //   .then(response => {
    //     console.log(response.data);
    //     setSearchProducts(response.data);
    //   })
    //   .catch(error => console.error(error));

    axios
      .get("http://127.0.0.1:8000/search?text="+formJson.postContent, {
        headers: { 
          'Access-Control-Allow-Origin' : '*'
        },
        responseType: "json",
      })
      .then(response => {
        console.log(response.data);
        setSearchProducts(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  
    console.log("DONE");
    return (
      <div>
      <div>
        <h3>Search Results</h3>
        <Grid container justify="center" spacing={4}>
          {searchres.map((product) => (
            <Grid key={product.pid} item xs={12} sm={6} md={4} lg={3}>
              <Product product={product} />
            </Grid>
          ))}
        </Grid>
      </div>
      </div>
      );
  }


  // return (
  //   <div>
  //     {products ? <pre>{JSON.stringify(products, null, 2)}</pre> : 'Loading...'}
  //   </div>

    return (
      <div>
      <div>
        <h3>User Behaviour Based Recommendations</h3>
        <Grid container justify="center" spacing={4}>
          {products1.map((product) => (
            <Grid key={product.pid} item xs={12} sm={6} md={4} lg={3}>
              <Product product={product} />
            </Grid>
          ))}
        </Grid>
      </div>
      <div>
        <h3>Trending Product Recommendations</h3>
        <Grid container justify="center" spacing={4}>
          {products3.map((product) => (
            <Grid key={product.pid} item xs={12} sm={6} md={4} lg={3}>
              <Product product={product} />
            </Grid>
          ))}
        </Grid>
      </div>
      <div>
        <h3>Similar Buys</h3>
        <Grid container justify="center" spacing={4}>
          {products2.map((product) => (
            <Grid key={product.pid} item xs={12} sm={6} md={4} lg={3}>
              <Product product={product} />
            </Grid>
          ))}
        </Grid>
      </div>
      
      

      

      <form method="get" onSubmit={handleSubmit}>
      <input type="text" class="form-control" name="postContent" id="postc" placeholder="Describe your product" />
      <span class="input-group-btn">
       <button class="btn btn-default" type="submit">
         <span class="glyphicon glyphicon-search">
         </span>
       </button>
       </span>
      </form>

      <div>
      <div>
        <h3>Search Results</h3>
        <Grid container justify="center" spacing={4}>
          {searchres.map((product) => (
            <Grid key={product.pid} item xs={12} sm={6} md={4} lg={3}>
              <Product product={product} />
            </Grid>
          ))}
        </Grid>
      </div>
      </div>
      </div>
  );
};


export default Search;