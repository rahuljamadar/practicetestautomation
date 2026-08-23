import { useCallback, useEffect, useMemo, useState } from 'react'
import KanbanBoard from './components/KanbanBoard'
import JobForm from './components/JobForm'
import ConfirmModal from './components/ConfirmModal'
import { useJobs } from './useJobs'
import { COLUMNS, EMPTY_JOB } from './constants'
import { CloseIcon } from './components/icons'

function MoonIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  )
}

function SunIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
    </svg>
  )
}

const btnOutline =
  'flex items-center gap-1.5 rounded-md border border-slate-300 dark:border-slate-600 px-3 py-2 text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors'

export default function App() {
  const { jobs, loaded, addJob, updateJob, removeJob, moveJob, replaceAll } = useJobs()
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem('jt-dark')
    if (saved !== null) return saved === 'true'
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  })
  const [search, setSearch] = useState('')
  const [sort, setSort] = useState('newest')
  const [statusFilter, setStatusFilter] = useState('all')
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [initialStatus, setInitialStatus] = useState('wishlist')
  const [toDelete, setToDelete] = useState(null)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
    localStorage.setItem('jt-dark', String(dark))
  }, [dark])

  const filteredJobs = useMemo(() => {
    let list = jobs
    if (statusFilter !== 'all') list = list.filter((j) => j.status === statusFilter)
    if (search.trim()) {
      const q = search.toLowerCase()
      list = list.filter(
        (j) =>
          (j.company || '').toLowerCase().includes(q) || (j.role || '').toLowerCase().includes(q),
      )
    }
    // Sort within the whole list; the board groups by status so per-column
    // ordering is preserved from this sorted order.
    const sorted = [...list].sort((a, b) => {
      const da = a.dateApplied ? new Date(a.dateApplied).getTime() : 0
      const db = b.dateApplied ? new Date(b.dateApplied).getTime() : 0
      return sort === 'newest' ? db - da : da - db
    })
    return sorted
  }, [jobs, search, sort, statusFilter])

  const openAdd = (status = 'wishlist') => {
    setEditing(null)
    setInitialStatus(status)
    setShowForm(true)
  }

  const openEdit = (job) => {
    setEditing(job)
    setInitialStatus(job.status)
    setShowForm(true)
  }

  const handleSubmit = (data) => {
    if (editing) {
      updateJob({ ...editing, ...data, id: editing.id })
    } else {
      addJob({ ...EMPTY_JOB, ...data, status: initialStatus })
    }
    setShowForm(false)
    setEditing(null)
  }

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(jobs, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'job-tracker-backup.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleImport = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      try {
        const data = JSON.parse(reader.result)
        if (!Array.isArray(data)) throw new Error('expected array')
        // Sanitize to known fields.
        const sanitized = data.map((j) => ({
          company: String(j.company || ''),
          role: String(j.role || ''),
          url: String(j.url || ''),
          resume: String(j.resume || ''),
          dateApplied: String(j.dateApplied || ''),
          salary: String(j.salary || ''),
          notes: String(j.notes || ''),
          status: COLUMNS.some((c) => c.id === j.status) ? j.status : 'wishlist',
        }))
        replaceAll(sanitized)
      } catch (err) {
        alert('Import failed: invalid JSON file')
      }
    }
    reader.readAsText(file)
    e.target.value = ''
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <header className="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <div className="mx-auto max-w-screen-2xl px-4 py-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <h1 className="text-xl font-bold tracking-tight">Job Tracker</h1>

          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search company or role..."
                className="w-56 rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-3 py-2 pl-8 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
              <SearchIcon />
            </div>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-2 py-2 text-sm"
            >
              <option value="all">All</option>
              {COLUMNS.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </select>

            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-2 py-2 text-sm"
            >
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
            </select>

            <button onClick={() => openAdd()} className="rounded-md bg-sky-600 px-3 py-2 text-sm font-medium text-white hover:bg-sky-700">
              + Add Job
            </button>

            <button onClick={handleExport} className={btnOutline}>
              Export
            </button>

            <label className={btnOutline}>
              Import
              <input type="file" accept="application/json" onChange={handleImport} className="hidden" />
            </label>

            <button
              onClick={() => setDark((d) => !d)}
              className={btnOutline}
              title="Toggle theme"
            >
              {dark ? <SunIcon /> : <MoonIcon />}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-screen-2xl px-4 py-6">
        {!loaded ? (
          <div className="py-20 text-center text-sm text-slate-400">Loading...</div>
        ) : (
          <KanbanBoard
            jobs={filteredJobs}
            onEdit={openEdit}
            onDelete={setToDelete}
            onAddJob={openAdd}
            onMoveJob={moveJob}
          />
        )}
      </main>

      {showForm && (
        <JobForm
          initial={editing}
          onClose={() => {
            setShowForm(false)
            setEditing(null)
          }}
          onSubmit={handleSubmit}
        />
      )}

      <ConfirmModal
        open={!!toDelete}
        title="Delete job?"
        message={`This will permanently remove ${toDelete?.company || 'this job'}. This cannot be undone.`}
        onCancel={() => setToDelete(null)}
        onConfirm={() => {
          removeJob(toDelete.id)
          setToDelete(null)
        }}
      />
    </div>
  )
}

function SearchIcon() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      className="pointer-events-none absolute left-2.5 top-2.5 text-slate-400"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.35-4.35" />
    </svg>
  )
}