import React, { useState, useEffect } from 'react'
import { Button,ButtonGroup, Row, Col, ListGroup, Image, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { PayPalButton } from 'react-paypal-button-v2'
import Message from '../components/Message'
import Loader from '../components/Loader'
import { getOrderDetails, payOrder, deliverOrder,statusOrder } from '../actions/orderActions'
import { ORDER_PAY_RESET, ORDER_DELIVER_RESET,ORDER_STATUS_RESET } from '../constants/orderConstants'
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown'

function OrderScreen({ match, history }) {

    const orderId = match.params.id
    const dispatch = useDispatch()

    const [sdkReady, setSdkReady] = useState(false)

    const orderDetails = useSelector(state => state.orderDetails)
    const { order, error, loading } = orderDetails

    const orderPay = useSelector(state => state.orderPay)
    const { loading: loadingPay, success: successPay } = orderPay

    // const orderDeliver = useSelector(state => state.orderDeliver)
    // const { loading: loadingDeliver, success: successDeliver } = orderDeliver

    const orderStatus=useSelector(state=>state.orderStatus)
    const { loading:lodingStatus, success: successStatus } = orderStatus

    const userLogin = useSelector(state => state.userLogin)
    const { userInfo } = userLogin

    if (!loading && !error) {
        order.itemsPrice = order.orderItems.reduce((acc, item) => acc + item.price * item.qty, 0).toFixed(2)
    }

    // """add paypal script tag to react"""
    const addPayPalScript = () => {
        const script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = 'https://www.paypal.com/sdk/js?client-id=AQNOIjWOYlVdSgcfLGmh6bwc586haW_9wl3yF8PPoCxLnqgLzNXjV2s8cy95px6mRPw-tM9mUFcaTVto'
        script.async = true
        script.onload = () => {
            setSdkReady(true)
        }
        document.body.appendChild(script)
    }



    useEffect(() => {

        if (!order || successPay || order._id !== Number(orderId) || successStatus ) {
            dispatch({ type: ORDER_PAY_RESET })
            dispatch({ type: ORDER_STATUS_RESET })
            dispatch(getOrderDetails(orderId))

        } else if (!order.isPaid) {
            if (!window.paypal) {
                addPayPalScript()
            } else {
                setSdkReady(true)
            }
        }

    }, [dispatch, order, orderId, successPay,successStatus])


    const successPaymentHandler = (paymentResult) => {
        dispatch(payOrder(orderId, paymentResult))
    }

    // const deliverHandler = () => {
    //     dispatch(deliverOrder(order))
    // }

    const [value,setValue]=useState('');
    const handleSelect=(e)=>{
        setValue(e)
        // console.log(e);
        console.log(e)
        dispatch(statusOrder(orderId,e))

    }

    return loading ? (
        <Loader />
    ) : error ? (
        <Message variant='danger'>{error}</Message>
    ) : (
        <div>
            <h1>Order: {order._id}</h1>
            <Row>
                <Col md={8}>
                    <ListGroup variant='flush'>


                        <ListGroup.Item>
                            <h2>Shipping</h2>
                            <p><strong>Name: </strong> {order.user.name}</p>
                            <p><strong>Email: </strong><a href={`mailto:${order.user.email}`}>{order.user.email}</a></p>

                            <p>
                                <strong>Shipping: </strong>
                                {order.shippingAddress.address},  {order.shippingAddress.city}
                                {'  '}
                                {order.shippingAddress.postalCode},
                                {'  '}
                                {order.shippingAddress.country}
                            </p>
                            {order.isDelivered ||  order.order_status === "delivered" ? (
                                <Message variant='success'>Delivered on {order.deliveredAt.substring(0, 10)}</Message>
                            ) : (
                                <Message variant='warning'>{order.order_status}</Message>
                            )}
                        </ListGroup.Item>


                        <ListGroup.Item>
                            <h2>Payment Method</h2>
                            <p>
                                <strong>Method: </strong>
                                {order.paymentMethod}
                            </p>
                            {order.isPaid ? (
                                <Message variant='success'>Paid on {order.paidAt.substring(0, 10)}</Message>
                            ) : (
                                <Message variant='warning'>Not Paid</Message>
                            )}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Order Items</h2>
                            {order.orderItems.length === 0 ? <Message variant='info'>
                                Order is empty
                            </Message> : (
                                <ListGroup variant='flush'>
                                    {order.orderItems.map((item, index) => (
                                        <ListGroup.Item key={index}>
                                            <Row>
                                                <Col md={1}>
                                                    <Image src={item.image} ClassName="photo" alt={item.name} fluid rounded />
                                                </Col>

                                                <Col>
                                                    <Link to={`/product/${item.product}`}>{item.name}</Link>
                                                </Col>

                                                <Col md={4}>
                                                    {item.qty} X ₹{item.price} = ₹{(item.qty * item.price).toFixed(2)}
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            )}
                        </ListGroup.Item>
                    </ListGroup>
                </Col>
                <Col md={4}>
                    <Card>
                        <ListGroup variant='flush'>
                            <ListGroup.Item>
                                <h2>Order Summary</h2>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Items:</Col>
                                    <Col>₹{order.itemsPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Shipping:</Col>
                                    <Col>₹{order.shippingPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Tax:</Col>
                                    <Col>₹{order.taxPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Total:</Col>
                                    <Col>₹{order.totalPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            {!order.isPaid && (
                                <ListGroup.Item>
                                    {loadingPay && <Loader />}

                                    {!sdkReady ? (
                                        <Loader />
                                    ) : (
                                        <PayPalButton
                                            amount={order.totalPrice}
                                            onSuccess={successPaymentHandler}
                                        />
                                    )}
                                </ListGroup.Item>
                            )}
                        </ListGroup>
                        {lodingStatus && <Loader />}
                        {userInfo && userInfo.isAdmin && order.isPaid && !order.isDelivered && (
                            // <ListGroup.Item>
                            //     <Button
                            //         type='button'
                            //         className='btn btn-block'
                            //         onClick={deliverHandler}
                            //     >
                            //         Mark As Delivered
                            //             </Button>
                            // </ListGroup.Item>
                            <ListGroup.Item>
                                    
                                <DropdownButton
                                    // alignRightg: "left"|"right" }
                                    as={ButtonGroup}
                                    menuAlign={{ xl: 'right' }}
                                    title="ORDER STATUS"
                                    size="md"
                                    // id="dropdown-menu-align-right"
                                    id="dropdown-item-button"
                                    onSelect={handleSelect}

                                >
                                        <Dropdown.Item eventKey="packaged">packaged</Dropdown.Item>
                                        <Dropdown.Item eventKey="shipped">shipped</Dropdown.Item>
                                        <Dropdown.Item eventKey="delivered">delivered</Dropdown.Item>
                                </DropdownButton>
                            </ListGroup.Item>
                        )}

                    </Card>
                </Col>
            </Row>

        </div >


    )
}

export default OrderScreen

