import { useCallback, useEffect, useState } from 'react'
import {
  bulkPutJobs,
  clearAllJobs,
  deleteJob,
  generateId,
  getAllJobs,
  putJob,
} from './db'

export function useJobs() {
  const [jobs, setJobs] = useState([])
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    let cancelled = false
    getAllJobs().then((rows) => {
      if (!cancelled) {
        setJobs(rows)
        setLoaded(true)
      }
    })
    return () => {
      cancelled = true
    }
  }, [])

  // A job here always has an id. We re-read from DB to keep state in sync
  // with what was actually persisted, so nothing is lost on reload.
  const persist = useCallback(async (mutator) => {
    let result
    setJobs((prev) => {
      result = mutator(prev)
      return result
    })
    return result
  }, [])

  const addJob = useCallback(
    async (job) => {
      const id = generateId()
      const fullJob = { ...job, id, dateApplied: job.dateApplied || new Date().toISOString().slice(0, 10) }
      await putJob(fullJob)
      await persist((prev) => [...prev, fullJob])
      return fullJob
    },
    [persist],
  )

  const updateJob = useCallback(
    async (job) => {
      await putJob(job)
      await persist((prev) => prev.map((j) => (j.id === job.id ? job : j)))
    },
    [persist],
  )

  const removeJob = useCallback(
    async (id) => {
      await deleteJob(id)
      await persist((prev) => prev.filter((j) => j.id !== id))
    },
    [persist],
  )

  // Set status optimistically in state, and persist to IndexedDB. We look up
  // the updated job from the DB after writing so state matches persistence.
  const moveJob = useCallback(async (id, status) => {
    setJobs((prev) => prev.map((j) => (j.id === id ? { ...j, status } : j)))
    const stored = await getAllJobs()
    const target = stored.find((j) => j.id === id)
    if (target) await putJob({ ...target, status })
  }, [])

  const replaceAll = useCallback(async (jobs) => {
    await clearAllJobs()
    const withIds = jobs.map((j) => ({
      ...j,
      id: j.id || generateId(),
      dateApplied: j.dateApplied || new Date().toISOString().slice(0, 10),
      status: j.status || 'wishlist',
    }))
    await bulkPutJobs(withIds)
    setJobs(withIds)
  }, [])

  return {
    jobs,
    loaded,
    addJob,
    updateJob,
    removeJob,
    moveJob,
    replaceAll,
  }
}