import { useState } from 'react'
import { COLUMNS, DEFAULT_RESUMES } from '../constants'
import { CloseIcon } from './icons'

const inputCls =
  'w-full rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-3 py-2 text-sm text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500'

export default function JobForm({ initial, onSubmit, onClose }) {
  const [job, setJob] = useState(() => ({
    company: initial?.company || '',
    role: initial?.role || '',
    url: initial?.url || '',
    resume: initial?.resume || '',
    dateApplied: initial?.dateApplied || new Date().toISOString().slice(0, 10),
    salary: initial?.salary || '',
    notes: initial?.notes || '',
    status: initial?.status || 'wishlist',
  }))
  const [errors, setErrors] = useState({})

  const set = (key, value) => setJob((prev) => ({ ...prev, [key]: value }))

  const validate = () => {
    const errs = {}
    if (!job.company.trim()) errs.company = 'Company name is required'
    if (!job.role.trim()) errs.role = 'Job role is required'
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validate()) return
    onSubmit({
      ...job,
      company: job.company.trim(),
      role: job.role.trim(),
      url: job.url.trim(),
    })
  }

  const existingResumes = [...new Set([...DEFAULT_RESUMES, job.resume].filter(Boolean))]

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div
        className="w-full max-w-lg rounded-xl bg-white dark:bg-slate-900 shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 px-5 py-4">
          <h2 className="text-base font-semibold text-slate-800 dark:text-slate-100">
            {initial ? 'Edit Job' : 'Add Job'}
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
            <CloseIcon />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 px-5 py-5 max-h-[70vh] overflow-y-auto">
          <div>
            <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              Company name *
            </label>
            <input
              className={inputCls}
              value={job.company}
              onChange={(e) => set('company', e.target.value)}
              placeholder="e.g. Accenture"
              autoFocus
            />
            {errors.company && <p className="mt-1 text-xs text-rose-500">{errors.company}</p>}
          </div>

          <div>
            <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              Job title / role *
            </label>
            <input
              className={inputCls}
              value={job.role}
              onChange={(e) => set('role', e.target.value)}
              placeholder="e.g. Senior Software Engineer"
            />
            {errors.role && <p className="mt-1 text-xs text-rose-500">{errors.role}</p>}
          </div>

          <div>
            <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              LinkedIn job URL
            </label>
            <input
              className={inputCls}
              type="url"
              value={job.url}
              onChange={(e) => set('url', e.target.value)}
              placeholder="https://www.linkedin.com/jobs/view/..."
            />
          </div>

          <div>
            <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              Resume used
            </label>
            <input
              list="resumes-list"
              className={inputCls}
              value={job.resume}
              onChange={(e) => set('resume', e.target.value)}
              placeholder="Search or type a resume name"
            />
            <datalist id="resumes-list">
              {existingResumes.map((r) => (
                <option key={r} value={r} />
              ))}
            </datalist>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
                Date applied
              </label>
              <input
                className={inputCls}
                type="date"
                value={job.dateApplied}
                onChange={(e) => set('dateApplied', e.target.value)}
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
                Salary range
              </label>
              <input
                className={inputCls}
                value={job.salary}
                onChange={(e) => set('salary', e.target.value)}
                placeholder="₹25-30 LPA"
              />
            </div>
          </div>

          <div>
            <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              Notes
            </label>
            <textarea
              className={inputCls}
              rows={3}
              value={job.notes}
              onChange={(e) => set('notes', e.target.value)}
              placeholder="Recruiter name, referral info, interview tips..."
            />
          </div>

          <div>
            <label className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              Status
            </label>
            <select
              className={inputCls}
              value={job.status}
              onChange={(e) => set('status', e.target.value)}
            >
              {COLUMNS.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </select>
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-md border border-slate-300 dark:border-slate-600 px-4 py-2 text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700"
            >
              {initial ? 'Save changes' : 'Add job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}