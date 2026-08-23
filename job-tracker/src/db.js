import { openDB } from 'idb'

const DB_NAME = 'job-tracker'
const DB_VERSION = 1
const STORE = 'jobs'

let dbPromise

function getDB() {
  if (!dbPromise) {
    dbPromise = openDB(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains(STORE)) {
          db.createObjectStore(STORE, { keyPath: 'id' })
        }
      },
    })
  }
  return dbPromise
}

export function generateId() {
  // crypto.randomUUID is available in modern browsers.
  return crypto.randomUUID()
}

export async function getAllJobs() {
  return (await getDB()).getAll(STORE)
}

export async function putJob(job) {
  return (await getDB()).put(STORE, job)
}

export async function deleteJob(id) {
  return (await getDB()).delete(STORE, id)
}

export async function clearAllJobs() {
  const tx = (await getDB()).transaction(STORE, 'readwrite')
  await tx.objectStore(STORE).clear()
  await tx.done
}

export async function bulkPutJobs(jobs) {
  const tx = (await getDB()).transaction(STORE, 'readwrite')
  for (const job of jobs) await tx.objectStore(STORE).put(job)
  await tx.done
}