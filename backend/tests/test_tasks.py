from app.models import AiAction


def test_task_lifecycle(client):
    r = client.post("/api/tasks", json={"title": "foo", "priority": "high"})
    assert r.status_code == 201
    tid = r.json()["id"]
    assert client.patch(f"/api/tasks/{tid}", json={"title": "bar"}).json()["title"] == "bar"
    done = client.post(f"/api/tasks/{tid}/complete").json()
    assert done["status"] == "done" and done["completed_at"]
    assert client.post(f"/api/tasks/{tid}/reopen").json()["completed_at"] is None
    assert client.get("/api/tasks?status=open").json()[0]["id"] == tid
    assert client.delete(f"/api/tasks/{tid}").status_code == 204
    assert client.get("/api/tasks").json() == []


def test_title_validation(client):
    assert client.post("/api/tasks", json={"title": "x" * 201}).status_code == 422


def test_ai_action_audit(client):
    s = client.session_factory()
    s.add(AiAction(id="foo-1", action_type="create_task", proposed={"title": "baz"}))
    s.commit()
    r = client.post("/api/tasks", json={"title": "baz", "ai_action_id": "foo-1"})
    assert r.status_code == 201
    a = client.get("/api/ai-actions").json()[0]
    assert a["status"] == "approved" and a["after"]["title"] == "baz"
    # already decided -> cannot be reused
    assert client.post("/api/tasks", json={"title": "baz", "ai_action_id": "foo-1"}).status_code == 409


def test_reject(client):
    s = client.session_factory()
    s.add(AiAction(id="foo-2", action_type="delete_task", task_id=1))
    s.commit()
    assert client.post("/api/ai-actions/foo-2/reject").json()["status"] == "rejected"
    assert client.post("/api/ai-actions/foo-2/reject").status_code == 409


def test_settings_profile(client):
    assert client.get("/api/settings").json()["phone"] is True
    client.put("/api/settings", json={"phone": False})
    assert client.get("/api/settings").json()["phone"] is False
    client.put("/api/profile", json={"name": "foo", "business": "bar"})
    assert client.get("/api/profile").json()["business"] == "bar"
