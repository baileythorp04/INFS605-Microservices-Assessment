import React, { useEffect, useMemo, useState } from 'react'
import './index.css' 

const FEEDBACK_API = 'http://localhost:5003'

export default function Feedback() {

      const [name, setName] = useState('')
    

    return (
        <div className="container">
            <h1>Feedback</h1>
            <p>Provide feedback as a student.</p>
        </div>
    )

}