import React, { useState, useEffect } from 'react'
import { Form, Button } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import FormContainer from '../components/FormContainer'
import CheckoutSteps from '../components/Checkoutsteps'
import { saveShippingAddress } from '../actions/cartActions'
import {CountryDropdown} from "react-country-region-selector";
import  '../App.css'





function ShippingScreen({ history }) {

    const cart = useSelector(state => state.cart)
    const { shippingAddress } = cart
    const dispatch = useDispatch()
    const [address, setAddress] = useState(shippingAddress.address)
    const [city, setCity] = useState(shippingAddress.city)
    const [postalCode, setPostalCode] = useState(shippingAddress.postalCode)
    const [country, setCountry] = useState(shippingAddress.country)

    const submitHandler=(e)=>{
        e.preventDefault()
        dispatch(saveShippingAddress({ address, city, postalCode, country }))
        history.push('/payment')
    }

    return (
        <FormContainer>
          <CheckoutSteps step1 step2/>
            <h1>Shipping</h1>
            <Form onSubmit={submitHandler}>

                <Form.Group controlId='address'>
                    <Form.Label>Address</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter address'
                        value={address ? address : ''}
                        onChange={(e) => setAddress(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId='city'>
                    <Form.Label>City</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter city'
                        value={city ? city : ''}
                        onChange={(e) => setCity(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId='postalCode'>
                    <Form.Label>Postal Code</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter postal code'
                        value={postalCode ? postalCode : ''}
                        onChange={(e) => setPostalCode(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId='country'>
                    <Form.Label>Country</Form.Label>
                   
                        <CountryDropdown className='new'
                            value={country}
                            onChange={(val) => setCountry(val)}
                        />
                    
                </Form.Group>

                <Button type='submit' variant='primary'>
                    Continue
                </Button>



            </Form>
        </FormContainer>

                


                



/* 
export class App extends Component {
  constructor(props) {
    super(props);
    this.state = { country: "" };
  }

  selectCountry(val) {
    this.setState({ country: val });
  }

  render() {
    const { country } = this.state;
    return (
      <div>
        <CountryDropdown
          value={country}
          onChange={(val) => this.selectCountry(val)}
        />
      </div>
    );
  }
} */




        
    )
}

export default ShippingScreen