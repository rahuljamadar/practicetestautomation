import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { useMemo, useState } from 'react'
import { COLUMNS } from '../constants'
import JobCard from './JobCard'
import PlusIcon from './PlusIcon'

function Column({ column, jobs, onEdit, onDelete, onAdd }) {
  return (
    <div className="flex min-h-[60vh] flex-1 flex-col rounded-lg bg-slate-100 dark:bg-slate-800/60">
      <div className="flex items-center justify-between px-3 py-3">
        <div className="flex items-center gap-2">
          <span className={`h-2.5 w-2.5 rounded-full ${column.accent}`} />
          <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">
            {column.title}
          </h2>
          <span className="rounded-full bg-white dark:bg-slate-700 px-2 py-0.5 text-[11px] font-medium text-slate-500 dark:text-slate-300">
            {jobs.length}
          </span>
        </div>
        <button
          onClick={onAdd}
          title={`Add to ${column.title}`}
          className="text-slate-400 hover:text-sky-500 transition-colors"
        >
          <PlusIcon />
        </button>
      </div>

      <SortableContext items={jobs.map((j) => j.id)} strategy={verticalListSortingStrategy}>
        <div className="flex flex-1 flex-col gap-2 overflow-y-auto px-2 pb-2">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} onEdit={onEdit} onDelete={onDelete} />
          ))}
          {jobs.length === 0 && (
            <div className="rounded-lg border border-dashed border-slate-300 dark:border-slate-600 p-4 text-center text-xs text-slate-400">
              No jobs yet
            </div>
          )}
        </div>
      </SortableContext>
    </div>
  )
}

export default function KanbanBoard({ jobs, onEdit, onDelete, onAddJob, onMoveJob }) {
  const [activeId, setActiveId] = useState(null)
  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 6 } }))

  const byStatus = useMemo(() => {
    const map = {}
    for (const c of COLUMNS) map[c.id] = []
    for (const j of jobs) {
      ;(map[j.status] || map.wishlist).push(j)
    }
    return map
  }, [jobs])

  const activeJob = jobs.find((j) => j.id === activeId)

  const handleDragStart = (event) => setActiveId(event.active.id)

  const handleDragOver = (event) => {
    const { active, over } = event
    if (!over) return
    const activeJobData = jobs.find((j) => j.id === active.id)
    const overJobData = jobs.find((j) => j.id === over.id)
    const overColumnId = overJobData ? overJobData.status : over.id

    // Column drop targets are the column id; when dragging onto a column,
    // reassign status optimistically.
    if (activeJobData && overColumnId && activeJobData.status !== overColumnId) {
      onMoveJob(active.id, overColumnId)
    }
  }

  const handleDragEnd = (event) => {
    const { active, over } = event
    if (over && active.id !== over.id) {
      const activeJobData = jobs.find((j) => j.id === active.id)
      const overJobData = jobs.find((j) => j.id === over.id)
      const overColumnId = overJobData ? overJobData.status : over.id
      if (activeJobData && overColumnId && activeJobData.status !== overColumnId) {
        onMoveJob(active.id, overColumnId)
      }
    }
    setActiveId(null)
  }

  const handleDragCancel = () => setActiveId(null)

  return (
    <DndContext
      sensors={sensors}
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
      onDragCancel={handleDragCancel}
    >
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        {COLUMNS.map((column) => (
          <Column
            key={column.id}
            column={column}
            jobs={byStatus[column.id]}
            onEdit={onEdit}
            onDelete={onDelete}
            onAdd={() => onAddJob(column.id)}
          />
        ))}
      </div>

      <DragOverlay>
        {activeJob ? (
          <div className="cursor-grabbing rounded-lg border border-sky-300 bg-white dark:bg-slate-800 p-3 shadow-lg opacity-90">
            <h3 className="truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
              {activeJob.company}
            </h3>
            <p className="truncate text-xs text-slate-500 dark:text-slate-400">{activeJob.role}</p>
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  )
}