"""API client for the Code Quest backend."""
import requests
import os
import json as json_lib
from utils.config import API_BASE, TOKEN_FILE, SAMPLE_PROBLEMS, SAMPLE_PROBLEM_DETAIL


class APIClient:
    """Handles all HTTP communication with the C++ backend."""

    def __init__(self):
        self.token = self._load_token()
        self.session = requests.Session()
        self.session.timeout = 8

    # ── Token management ─────────────────────────────────────────────────────

    def _load_token(self):
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE) as f:
                    return f.read().strip() or None
            except Exception:
                pass
        return None

    def _save_token(self, token: str):
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        self.token = token

    def is_logged_in(self) -> bool:
        return bool(self.token)

    # ── HTTP helpers ─────────────────────────────────────────────────────────

    def _get(self, endpoint: str, params: dict = None) -> dict:
        try:
            r = self.session.get(f"{API_BASE}{endpoint}", params=params)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e), "offline": True}

    def _post(self, endpoint: str, data: dict) -> dict:
        try:
            r = self.session.post(f"{API_BASE}{endpoint}", json=data)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e), "offline": True}

    # ── Auth ─────────────────────────────────────────────────────────────────

    def login(self, username: str, password: str) -> dict:
        result = self._post("/auth/login", {"username": username, "password": password})
        if result.get("success"):
            self._save_token(result["token"])
        return result

    def register(self, username: str, password: str) -> dict:
        result = self._post("/auth/register", {"username": username, "password": password})
        if result.get("success"):
            self._save_token(result["token"])
        return result

    def get_profile(self) -> dict:
        return self._get("/auth/profile", {"token": self.token})

    def logout(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        self.token = None

    # ── Problems ─────────────────────────────────────────────────────────────

    def get_problems(self, difficulty: str = None) -> list:
        params = {}
        if difficulty:
            params["difficulty"] = difficulty
        result = self._get("/problems", params)
        if isinstance(result, list):
            return result
        if result.get("offline"):
            if difficulty:
                return [p for p in SAMPLE_PROBLEMS if p["difficulty"] == difficulty]
            return SAMPLE_PROBLEMS
        return SAMPLE_PROBLEMS

    def get_problem(self, problem_id: int) -> dict:
        result = self._get(f"/problems/{problem_id}")
        if result.get("offline") or result.get("error"):
            # Load from backend/problems/problems.json if available
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                json_path = os.path.join(base_dir, "backend", "problems", "problems.json")
                if os.path.exists(json_path):
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json_lib.load(f)
                    for item in data:
                        if item.get("id") == problem_id:
                            from utils.config import LOCAL_TEST_CASES
                            item["visible_tests"] = LOCAL_TEST_CASES.get(problem_id, [])
                            return item
            except Exception:
                pass

            if problem_id == 1:
                return SAMPLE_PROBLEM_DETAIL
            p = next((x for x in SAMPLE_PROBLEMS if x["id"] == problem_id), None)
            if p:
                from utils.config import LOCAL_TEST_CASES
                return {**p,
                        "description": f"Solve challenge #{problem_id}: {p['title']}.",
                        "examples": ["Input: ...\nOutput: ..."],
                        "constraints": ["Check constraints in problem description"],
                        "hints": ["Think of time and space complexity."],
                        "visible_tests": LOCAL_TEST_CASES.get(problem_id, [])}
        return result

    def get_daily(self) -> dict:
        result = self._get("/problems/daily")
        if result.get("offline"):
            return SAMPLE_PROBLEM_DETAIL
        return result

    # ── Judge ─────────────────────────────────────────────────────────────────

    def submit_code(self, problem_id: int, code: str, language: str) -> dict:
        return self._post("/judge/run", {
            "problem_id": problem_id,
            "code": code,
            "language": language,
            "token": self.token or "",
        })

    # ── Leaderboard ──────────────────────────────────────────────────────────

    def get_leaderboard(self) -> list:
        result = self._get("/leaderboard")
        if isinstance(result, list):
            return result
        # Offline sample
        return [
            {"rank": 1, "username": "ninja_coder",  "xp": 850, "level": "Champion", "badge_count": 5, "solved_count": 18},
            {"rank": 2, "username": "algo_wizard",  "xp": 720, "level": "Champion", "badge_count": 4, "solved_count": 15},
            {"rank": 3, "username": "byte_master",  "xp": 580, "level": "Warrior",  "badge_count": 3, "solved_count": 12},
            {"rank": 4, "username": "code_samurai", "xp": 420, "level": "Warrior",  "badge_count": 2, "solved_count": 9},
            {"rank": 5, "username": "debug_hero",   "xp": 310, "level": "Warrior",  "badge_count": 2, "solved_count": 7},
        ]

    def get_user_rank(self) -> dict:
        return self._get("/leaderboard/user", {"token": self.token})

    # ── Health ───────────────────────────────────────────────────────────────

    def check_health(self) -> bool:
        result = self._get("/health")
        return result.get("status") == "ok"
