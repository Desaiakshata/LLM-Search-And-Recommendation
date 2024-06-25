import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Typewriter from "./typewriter";
import { useNavigate, Routes, Route, NavLink, HashRouter } from 'react-router-dom';
import Search from "./Search";


// const loginelement = (
//   <div id="base">
//     <div id="block1">
//       <h1>L<Typewriter text="ogin to SHOP...." delay={250} infinite/></h1>
//       <button class="button-46" role="button">Login</button>
//     </div>
//     <div id="block2">
//       <img src="rakuten-bg.png" id="logo" />
//     </div>
//   </div>
//   )

// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(loginelement);



export default function Login() {

  // const navigate = useNavigate();

  // function handleClick(event) {
  //   navigate('/target-route');
  // }

  

  // const loginelement = (
  // <div id="base">
  //   <div id="block1">
  //     <h1>L<Typewriter text="ogin to SHOP...." delay={250} infinite/></h1>
  //     <button onClick={this.handleClick} class="button-46" role="button">Login</button>
  //   </div>
  //   <div id="block2">
  //     <img src="rakuten-bg.png" id="logo" />
  //   </div>
  // </div>
  // )

    return (
      <HashRouter>
        <div id="base">
          <div id="block1">
            <h1>L<Typewriter text="ogin to SHOP...." delay={250} infinite /></h1>
            <NavLink id="nav_link" to="/Search">Login</NavLink>
          </div>
          <div id="block2">
            <img src="rakuten-bg.png" id="logo" />
          </div>
          <div id="search">
            <Routes>
              <Route exact path="/Search" element={<Search />}/>
            </Routes>
          </div>
        </div>
      </HashRouter>
    );

}



const root = ReactDOM.createRoot(document.getElementById('root'));
const element = <Login isToggleOn="true" />;
root.render(element);
