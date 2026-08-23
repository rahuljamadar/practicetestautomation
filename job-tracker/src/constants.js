// Column definitions and constants shared across the app.

export const COLUMNS = [
  { id: 'wishlist', title: 'Wishlist', accent: 'bg-slate-400' },
  { id: 'applied', title: 'Applied', accent: 'bg-sky-500' },
  { id: 'follow-up', title: 'Follow-up', accent: 'bg-amber-500' },
  { id: 'interview', title: 'Interview', accent: 'bg-violet-500' },
  { id: 'offer', title: 'Offer', accent: 'bg-emerald-500' },
  { id: 'rejected', title: 'Rejected', accent: 'bg-rose-500' },
]

export const COLUMN_MAP = Object.fromEntries(COLUMNS.map((c) => [c.id, c]))

// Previously used resume names suggested in the dropdown (editable via the form).
export const DEFAULT_RESUMES = [
  'SDE_Resume_v3',
  'QA_Lead_Resume',
  'Senior_Engineer_Resume',
  'Resume_Generic',
]

export const EMPTY_JOB = {
  id: undefined,
  company: '',
  role: '',
  url: '',
  resume: '',
  dateApplied: '',
  salary: '',
  notes: '',
  status: 'wishlist',
}