import { useEffect, useState } from "react";
import { api, type Task } from "../api/client";

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  useEffect(() => {
    api.listTasks("open,in_progress").then(setTasks).catch(() => setTasks([]));
  }, []);
  return (
    <>
      <h1>לוח משימות</h1>
      {tasks.length === 0 ? (
        <div className="empty">אין משימות פתוחות</div>
      ) : (
        <ul className="tasklist">
          {tasks.map((t) => (
            <li key={t.id} className="task">
              {t.title}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
