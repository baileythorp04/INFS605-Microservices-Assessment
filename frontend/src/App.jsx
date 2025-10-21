import React, { useEffect, useMemo, useState } from 'react'
import './index.css' // Import the new CSS file

const STUDENTS_API = 'http://localhost:5001'
const CATALOG_API = 'http://localhost:5002'
const FEEDBACK_API = 'http://localhost:5003'

export default function App() {

  /* Student variables */
  const [students, setStudents] = useState([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [search, setSearch] = useState('')
  const [attDate, setAttDate] = useState('')
  const [attStatus, setAttStatus] = useState('Present')

  const [studentsOpen, setStudentsOpen] = useState(false)

  /* Course variables */
  const [courses, setCourses] = useState([])
  const [catalogOpen, setCatalogOpen] = useState(false)

  /* Feedback variables */
  const [feedback, setFeedback] = useState([])

  const [feedbackOpen, setFeedbackOpen] = useState(false)

  const [replyText, setReplyText] = useState('')
  const [replyId, setReplyId] = useState(-1)



  /* #### Student API Access #### */

  const fetchStudents = () => {
    fetch(`${STUDENTS_API}/students`)
      .then(r => r.json())
      .then(setStudents)
  }

  useEffect(() => { fetchStudents() }, [])

  const addStudent = async () => {
    if (!name || !email) return
    const res = await fetch(`${STUDENTS_API}/students`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ name, email })
    })
    if (res.ok) {
      setName(''); setEmail('')
      fetchStudents()
    }
  }

  const deleteStudent = async (id) => {
    await fetch(`${STUDENTS_API}/students/${id}`, { method: 'DELETE' })
    fetchStudents()
  }

  const addAttendance = async (id) => {
    if (!attDate) return
    await fetch(`${STUDENTS_API}/students/${id}/attendance`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ date: attDate, status: attStatus })
    })
    setAttDate('')
    fetchStudents()
  }

  const filteredStudents = useMemo(() => students.filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.email.toLowerCase().includes(search.toLowerCase())
  ), [students, search])

  const toggleStudentCollapse = () => {
    setStudentsOpen(!studentsOpen)
  }

  const toggleCatalogCollapse = () => {
    setCatalogOpen(!catalogOpen)
  }

    const toggleFeedbackCollapse = () => {
    setFeedbackOpen(!feedbackOpen)
  }


  /* #### Catalog API Access #### */

  const fetchCourses = () => {
    fetch(`${CATALOG_API}/courses`)
      .then(r => r.json())
      .then(setCourses)
  }

  
  

  useEffect(() => { fetchCourses() }, [])

  /* #### Feedback API Access #### */

  const fetchFeedback = () => {
    console.log("fetched")

    fetch(`${FEEDBACK_API}/feedback`)
      .then(r => r.json())
      .then(setFeedback)
  }

  const deleteFeedback = async (id) => {
    await fetch(`${FEEDBACK_API}/feedback/${id}`, { method: 'DELETE' })
    fetchFeedback()
  }

  const makeReply = async (id) => {
    console.log("reply button pressed")
    if (!replyText) return
    const res = await fetch(`${FEEDBACK_API}/feedback/${id}/reply`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ reply: replyText })
    })
    if (res.ok) {
      setReplyId(-1)
      fetchFeedback()
    }
  }

  const newFeedback = useMemo(() => feedback.filter(f =>
    f.feedback_status == 'open'), [feedback])
  const oldFeedback = useMemo(() => feedback.filter(f =>
    ['replied', 'resolved'].includes(f.feedback_status)), [feedback])

  useEffect(() => { fetchFeedback() }, [])
  useEffect(() => { setReplyText('') }, [replyId])



  return (
    <div className="container">
      <h1>Admin Portal</h1>
      <p>Manage students, search, and record attendance.</p>

      {/* === Add Student + Search Section === */}
      <section className="grid-2">
        <div className="card">
          <h2>Add Student</h2>
          <input placeholder="Full name" value={name} onChange={e=>setName(e.target.value)} />
          <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
          <button className="btn-primary" onClick={addStudent}>Add</button>
        </div>

        <div className="card">
          <h2>Search</h2>
          <input placeholder="Search by name or email" value={search} onChange={e=>setSearch(e.target.value)} />
        </div>
      </section>

      {/* === Student List Section === */}
      <div className='horizontal-container'>
        <h2>Students ({filteredStudents.length})</h2>
        <button onClick={toggleStudentCollapse}>
          {studentsOpen ? 'Λ' : 'V'}
        </button>
      </div>
      {studentsOpen && <div className="grid-gap">
        {filteredStudents.map(s => (
          <div key={s.id} className="grid-row">
            <div>
              <div style={{ fontWeight: 'bold', color: '#212121' }}>{s.name}</div>
              <div style={{ color: '#616161' }}>{s.email}</div>

              <details>
                <summary>Attendance ({(s.attendance || []).length})</summary>
                <ul>
                  {(s.attendance || []).map((a,i) => (
                    <li key={i}>{a.date} – {a.status}</li>
                  ))}
                </ul>
              </details>
            </div>

            <div className="justify-end">
              <div className="horizontal-container">
                <input type="date" value={attDate} onChange={e=>setAttDate(e.target.value)} />
                <select value={attStatus} onChange={e=>setAttStatus(e.target.value)}>
                  <option>Present</option>
                  <option>Absent</option>
                  <option>Late</option>
                  <option>Excused</option>
                </select>
                <button className="btn-secondary" onClick={()=>addAttendance(s.id)}>Record</button>
              </div>
              <button className="btn-danger" onClick={()=>deleteStudent(s.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>}




      {/* === Course List Section === */}
      <div className='horizontal-container'>
        <h2>Course Catalog ({courses.length} courses)</h2>
      <div className="justify-end">
        <button onClick={toggleCatalogCollapse}>
          {catalogOpen ? 'Λ' : 'V'}
        </button>
      </div>
      </div>
      {catalogOpen && <div className="grid-gap">
        {courses.map(c => (
          <div key={c.id} className="grid-row">
            <div>
              <div style={{ fontWeight: 'bold', color: '#212121' }}>{c.name}</div>
              <div style={{ color: '#616161' }}>{c.code}</div>

              <details>
                <summary>Description</summary>
                <p>{c.description}</p>
              </details>
            </div>
          </div>
        ))}
      </div>}


    {/* === Feedback List Section === */}
      <div className='horizontal-container'>
        <h2>Feedback List ({feedback.length})</h2>
        <button onClick={toggleFeedbackCollapse}>
          {feedbackOpen ? 'Λ' : 'V'}
        </button>
      </div>
      {feedbackOpen && <div className="grid-gap">

        <h3>Open Feedback ({newFeedback.length}):</h3>
        {newFeedback.map(f => (
          <div key={f.id} className="grid-row">
            <div>
              <div style={{ fontWeight: 'bold', color: '#212121' }}>Feedback from {f.student_name}:</div>
              <div style={{ color: '#616161' }}>{f.text}</div>
            </div>

            <div className="justify-end">
              <div className='horizontal-container'>
                {replyId == f.id && <textarea onChange={(e) => setReplyText(e.target.value)} cols='50' placeholder='Type reply here...'></textarea>}
                {replyId == f.id && <button onClick={() => makeReply(f.id)} className="btn-info">Send Reply</button>}
                {replyId != f.id && <button onClick={() => setReplyId(f.id)} className="btn-info">Reply</button>}
                <button className="btn-success">Mark as Resolved</button>
              </div>
              <button className="btn-danger" onClick={() => deleteFeedback(f.id)} >Delete</button>
            </div>

            {f.feedback_status == 'replied' &&
            <div>
              <div style={{ textDecoration: 'underline', color: '#212121' }}>Reply:</div>
              <div style={{ color: '#616161' }}>{f.reply}</div>
            </div>}
          </div>
        ))}


        <h3>Closed Feedback ({oldFeedback.length}):</h3>
        {oldFeedback.map(f => (
          <div key={f.id} className="grid-row">
            <div>
              <div style={{ fontWeight: 'bold', color: '#212121' }}>Feedback from {f.student_name}:</div>
              <div style={{ color: '#616161' }}>{f.text}</div>
            </div>

            <div className="justify-end">
              <button className="btn-danger" onClick={() => deleteFeedback(f.id)} >Delete</button>
            </div>

            {f.feedback_status == 'replied' &&
            <div>
              <div style={{ textDecoration: 'underline', color: '#212121' }}>Reply:</div>
              <div style={{ color: '#616161' }}>{f.reply}</div>
            </div>}
          </div>
        ))}
      </div>}
    </div>
  )
}