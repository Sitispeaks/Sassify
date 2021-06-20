import { Container } from "react-bootstrap";
import { BrowserRouter as Router, Route } from 'react-router-dom'
import Header from "./components/Header";
import Footer from "./components/Footer";
// import './App.css';
import Homescreen from "./screens/Homescreen";
import ProductScreen from "./screens/ProductScreen";
import CartScreen from "./screens/CartScreen";
import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from './screens/RegisterScreen';
import ProfileScreen from './screens/ProfileScreen';
import ShippingScreen from './screens/ShippingScreen';
import PaymentScreen from './screens/PaymentScreen';
import PlaceOrderScreen from './screens/PlaceOrderScreen';
import OrderScreen from './screens/OrderScreen';
import UserListScreen from './screens/UserListScreen';
import UserEditScreen from './screens/UserEditScreen';
import ProductListScreen from './screens/ProductListScreen';
import ProductEditScreen from './screens/ProductEditScreen';
import OrderListScreen from './screens/OrderListScreen';


function App() {
  return (
    <Router>
     
        <Header />
        <main className="py-4">
          <Container>
            <h1 className="text-center">Welcome to my app</h1>
            <Route path='/' component={Homescreen} exact />
            <Route path='/login' component={LoginScreen}  />
            <Route path='/register' component={RegisterScreen}  />
            <Route path='/profile' component={ProfileScreen}  />
            <Route path='/product/:id' component={ProductScreen} />
            <Route path='/cart/:id?' component={CartScreen} />
            <Route path='/shipping' component={ShippingScreen} />
            <Route path='/payment' component={PaymentScreen} />
            <Route path='/placeorder' component={PlaceOrderScreen} />
            <Route path='/order/:id' component={OrderScreen} />


            <Route path='/admin1/userlist' component={UserListScreen} />
            <Route path='/admin1/user/:id/edit' component={UserEditScreen} />


            <Route path='/admin1/productlist' component={ProductListScreen} />
            <Route path='/admin1/product/:id/edit' component={ProductEditScreen} />

            <Route path='/admin1/orderList' component={OrderListScreen} />


          </Container>
        </main>
        <Footer />
      
    </Router>

  );
}

export default App;
