import { LinkIcon } from './icons'
import { COLUMN_MAP } from '../constants'
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

function daysSince(dateStr) {
  if (!dateStr) return 0
  const applied = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now - applied) / (1000 * 60 * 60 * 24))
  return Math.max(diff, 0)
}

export default function JobCard({ job, onEdit, onDelete }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: job.id })
  const column = COLUMN_MAP[job.status] || COLUMN_MAP.wishlist
  const days = daysSince(job.dateApplied)

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.4 : 1,
  }

  const stopProp = (e) => {
    e.stopPropagation()
    e.preventDefault()
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="group relative cursor-grab rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 shadow-sm hover:shadow-md transition-shadow"
    >
      <span className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-lg ${column.accent}`} />

      <div className="flex items-start justify-between gap-2 pl-2">
        <div className="min-w-0">
          <h3 className="truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
            {job.company}
          </h3>
          <p className="truncate text-xs text-slate-500 dark:text-slate-400">{job.role}</p>
        </div>
        <div
          className="flex items-center gap-1"
          onPointerDown={stopProp}
          onClick={stopProp}
          onKeyDown={stopProp}
        >
          {job.url && (
            <a
              href={job.url}
              target="_blank"
              rel="noopener noreferrer"
              title="Open LinkedIn posting"
              className="text-slate-400 hover:text-sky-500 transition-colors"
            >
              <LinkIcon />
            </a>
          )}
          <button
            onClick={() => onDelete(job)}
            title="Delete"
            className="text-slate-300 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <TrashIcon />
          </button>
          <button
            onClick={() => onEdit(job)}
            title="Edit"
            className="text-slate-300 hover:text-slate-600 dark:hover:text-slate-200 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <PencilIcon />
          </button>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-2 pl-2 text-xs">
        {job.resume && (
          <span className="rounded bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 text-[11px] text-slate-600 dark:text-slate-300">
            {job.resume}
          </span>
        )}
        {job.dateApplied && (
          <span className="text-slate-400 dark:text-slate-500">{days}d ago</span>
        )}
        {job.status === 'wishlist' && !job.dateApplied && (
          <span className="text-slate-400 dark:text-slate-500">Saved</span>
        )}
      </div>
    </div>
  )
}

function TrashIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M3 6h18M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
    </svg>
  )
}

function PencilIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M17 3a2.83 2.83 0 0 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />
    </svg>
  )
}