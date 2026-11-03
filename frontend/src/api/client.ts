export type Priority = "low" | "medium" | "high";
export type Status = "open" | "in_progress" | "done";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  due_date: string | null;
  priority: Priority;
  status: Status;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.status === 204 ? (undefined as T) : res.json();
}

export const api = {
  listTasks: (status?: string) => request<Task[]>(`/tasks${status ? `?status=${status}` : ""}`),
  createTask: (body: Partial<Task> & { title: string; ai_action_id?: string }) =>
    request<Task>("/tasks", { method: "POST", body: JSON.stringify(body) }),
  completeTask: (id: number) => request<Task>(`/tasks/${id}/complete`, { method: "POST" }),
  reopenTask: (id: number) => request<Task>(`/tasks/${id}/reopen`, { method: "POST" }),
};
