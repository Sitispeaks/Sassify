import React, { useState, useEffect } from 'react'
import { Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'

import { listProducts } from '../actions/productActions'
import Product from '../components/Product'

import Loader from '../components/Loader'
import Message from '../components/Message'
import ProductCarousel from '../components/ProductCarousel'




function Homescreen({ history }) {

    const dispatch = useDispatch()

    const productList = useSelector(state => state.productList)
    const { error, loading, products, page, pages } = productList

    let keyword = history.location.search

   

    useEffect(() => {
        dispatch(listProducts(keyword))
    
    }, [dispatch, keyword])

   

    return (
        <div>
            {!keyword && <ProductCarousel/>}
            <h1 className="">Latest products</h1>
            {loading ? <Loader />
                : error ? <Message variant='danger'>{error}</Message>
                    :
                    <div>
                        <Row>
                            {products.map(product => (
                                <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                                    <Product product={product} />
                                </Col>
                            ))}
                        </Row>
                    </div>
            }
        </div>
    )
}

export default Homescreen
