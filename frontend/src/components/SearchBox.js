import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
// import axios from 'axios'
function SearchBox() {
    const [keyword, setKeyword] = useState('')

    let history = useHistory()

    const submitHandler = (e) => {
        e.preventDefault()
        // console.log(keyword)
        if (keyword) { 
            history.push(`/?search=${keyword}`)
        } else {
            history.push(history.push(history.location.pathname))
        }
    }
    return (
        <Form onSubmit={submitHandler} inline>
            <Form.Control
                type='text'
                name='q'
                onChange={(e) => setKeyword(e.target.value)}
                className='mr-sm-2 ml-sm-5'
            ></Form.Control>

            <Button
                type='submit'
                variant='outline-success'
                className='p-2'
            >
                Submit
            </Button>
        </Form>
    )
}

export default SearchBox