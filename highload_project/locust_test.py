from locust import HttpUser, task, between

class HighLoadTestUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post(
            "/api/token/",
            json={"username": "admin", "password": "admin"},
        )
        self.token = response.json().get("access")

    @task
    def test_home_page(self):
        self.client.get("/", headers={"Authorization": f"Bearer {self.token}"})

    @task
    def test_send_email(self):
        payload = {
            "recipient": "arystanbekovas2004@gmail.com",
            "subject": "Test Email",
            "body": "This is a test email."
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.client.post("/tasks/send-email/", json=payload, headers=headers)
