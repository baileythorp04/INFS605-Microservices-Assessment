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

  /* #### Catalog API Access #### */

  const fetchFeedback = () => {
    fetch(`${FEEDBACK_API}/feedback`)
      .then(r => r.json())
      .then(setFeedback)
  }

  useEffect(() => { fetchFeedback() }, [])



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
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
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
        <button onClick={toggleCatalogCollapse}>
          {catalogOpen ? 'Λ' : 'V'}
        </button>
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
        {feedback.map(f => (
          <div key={f.id} className="grid-row">
            <div>
              <div style={{ fontWeight: 'bold', color: '#212121' }}>{f.student_name}</div>
              <div style={{ color: '#616161' }}>{f.text}</div>
            </div>
          </div>
        ))}
      </div>}
    </div>
  )
}